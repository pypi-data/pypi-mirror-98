# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from itertools import product
from math import ceil

import numpy as np
import torch
import torch.backends.cudnn as cudnn

from .base import Base


class FaceDetector(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_sizes = self.meta_conf['min_sizes']
        self.steps = self.meta_conf['steps']
        self.variance = self.meta_conf['variance']
        self.in_channel = self.meta_conf['in_channel']
        self.out_channel = self.meta_conf['out_channel']
        self.confidence_threshold = self.meta_conf['confidence_threshold']

    def detect(self, image):
        cudnn.benchmark = True
        assert isinstance(image, np.ndarray)
        input_height, input_width, _ = image.shape
        img = np.float32(image)
        scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
        img -= (104, 117, 123)
        img = img.transpose(2, 0, 1)
        self.model = self.model.to(self.device)
        img = torch.from_numpy(img).unsqueeze(0)
        with torch.no_grad():
            img = img.to(self.device)
            scale = scale.to(self.device)
            loc, conf, landms = self.model(img)
        priors = self.priorbox_forward(height=input_height, width=input_width)
        priors = priors.to(self.device)
        prior_data = priors.data
        boxes = self.decode(loc.data.squeeze(0), prior_data, self.variance)
        boxes = boxes * scale
        boxes = boxes.cpu().numpy()
        scores = conf.squeeze(0).data.cpu().numpy()[:, 1]

        # ignore low scores
        inds = np.where(scores > self.confidence_threshold)[0]
        boxes = boxes[inds]
        scores = scores[inds]

        # keep top-K before NMS
        order = scores.argsort()[::-1]
        boxes = boxes[order]
        scores = scores[order]

        # do NMS
        nms_threshold = 0.2
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
        keep = self.py_cpu_nms(dets, nms_threshold)
        dets = dets[keep, :]
        return dets

    def py_cpu_nms(self, dets, thresh):
        """
        Python version NMS.
        Returns:
            The kept index after NMS.
        """
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= thresh)[0]
            order = order[inds + 1]
        return keep

    def decode(self, loc, priors, variances):
        """Decode locations from predictions using priors to undo
        the encoding we did for offset regression at train time.
        Args:
            loc (tensor): location predictions for loc layers,
                Shape: [num_priors,4]
            priors (tensor): Prior boxes in center-offset form.
                Shape: [num_priors,4].
            variances: (list[float]) Variances of priorboxes

        Return:
            decoded bounding box predictions
        """
        boxes = torch.cat((priors[:, :2], priors[:, 2:]), 1)
        boxes[:, :2] = priors[:, :2] + loc[:, :2] * variances[0] * priors[:, 2:]
        boxes[:, 2:] = priors[:, 2:] * torch.exp(loc[:, 2:] * variances[1])
        boxes[:, :2] -= boxes[:, 2:] / 2
        boxes[:, 2:] += boxes[:, :2]
        return boxes

    def priorbox_forward(self, height, width):
        feature_maps = [[ceil(height/step), ceil(width/step)] for step in self.steps]
        anchors = []
        for k, f in enumerate(feature_maps):
            min_sizes = self.min_sizes[k]
            for i, j in product(range(f[0]), range(f[1])):
                for min_size in min_sizes:
                    s_kx = min_size / width
                    s_ky = min_size / height
                    dense_cx = [x * self.steps[k] / width for x in [j + 0.5]]
                    dense_cy = [y * self.steps[k] / height for y in [i + 0.5]]
                    for cy, cx in product(dense_cy, dense_cx):
                        anchors += [cx, cy, s_kx, s_ky]

        return torch.Tensor(anchors).view(-1, 4)