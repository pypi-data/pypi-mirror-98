# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import numpy as np
import torch

from .base import Base


class FaceRecognition(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mean = self.meta_conf['mean']
        self.std = self.meta_conf['std']

    def load(self, device=None):
        super().load(device)
        if self.device.type == "cpu":
            self.model = self.model.module.cpu()

    def get(self, image):
        assert isinstance(image, np.ndarray)
        height, width, channels = image.shape
        assert height == self.input_height and width == self.input_width
        if image.ndim == 2:
            image = image[:, :, np.newaxis]
        if image.ndim == 4:
            image = image[:, :, :3]
        assert image.ndim <= 4
        image = (image.transpose((2, 0, 1)) - self.mean) / self.std
        image = image.astype(np.float32)
        image = torch.from_numpy(image)
        image = torch.unsqueeze(image, 0)
        image = image.to(self.device)
        with torch.no_grad():
            feature = self.model(image).cpu().numpy()
        feature = np.squeeze(feature)
        return feature
