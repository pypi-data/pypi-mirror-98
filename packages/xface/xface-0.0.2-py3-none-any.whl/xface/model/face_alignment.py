# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import cv2
import torch
import numpy as np

import torch.backends.cudnn as cudnn
from torchvision import transforms

from .base import Base


class FaceAlignment(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_size = self.meta_conf['input_width']

    def get(self, image, det):
        cudnn.benchmark = True
        assert isinstance(image, np.ndarray)
        img = image.copy()
        img = np.float32(img)

        xy = np.array([det[0], det[1]])
        zz = np.array([det[2], det[3]])
        wh = zz - xy + 1
        center = (xy + wh / 2).astype(np.int32)
        boxsize = int(np.max(wh) * 1.2)
        xy = center - boxsize // 2
        x1, y1 = xy
        x2, y2 = xy + boxsize
        height, width, _ = img.shape
        dx = max(0, -x1)
        dy = max(0, -y1)
        x1 = max(0, x1)
        y1 = max(0, y1)
        edx = max(0, x2 - width)
        edy = max(0, y2 - height)
        x2 = min(width, x2)
        y2 = min(height, y2)
        imageT = image[y1:y2, x1:x2]
        if dx > 0 or dy > 0 or edx > 0 or edy > 0:
            imageT = cv2.copyMakeBorder(imageT, dy, edy, dx, edx, cv2.BORDER_CONSTANT, 0)

        imageT = cv2.resize(imageT, (self.img_size, self.img_size))
        t = transforms.Compose([transforms.ToTensor()])
        img_after = t(imageT)
        self.model = self.model.to(self.device)
        img_after = img_after.unsqueeze(0)
        with torch.no_grad():
            image_pre = img_after.to(self.device)
            _, landmarks_normal = self.model(image_pre)
        landmarks_normal = landmarks_normal.cpu().numpy()
        landmarks_normal = landmarks_normal.reshape(landmarks_normal.shape[0], -1, 2)
        landmarks = landmarks_normal[0] * [boxsize, boxsize] + xy
        return landmarks
