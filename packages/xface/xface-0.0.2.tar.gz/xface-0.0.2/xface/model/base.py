# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import json
import os
import sys

import torch


class Config(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class Base:
    def __init__(self, model_path, model_category, model_name, meta_file='model_meta.json'):
        model_root_dir = os.path.join(model_path, model_category, model_name)
        meta_file_path = os.path.join(model_root_dir, meta_file)
        with open(meta_file_path, 'r') as f:
            self.meta_conf = json.load(f)
        model_root = os.path.dirname(model_path)
        if model_root not in sys.path:
            sys.path.append(model_root)
        self.model_path = model_path
        self.model_category = model_category
        self.model_name = model_name
        self.model_file_path = os.path.join(model_root_dir, self.meta_conf['model_file'])
        self.model_type = self.meta_conf['model_type']
        self.model_info = self.meta_conf['model_info']
        self.release_date = self.meta_conf['release_date']
        self.input_height = self.meta_conf['input_height']
        self.input_width = self.meta_conf['input_width']
        self.device = None
        self.model = None

    def load(self, device=None):
        assert self.model is None
        if device is None:
            if torch.cuda.is_available():
                device = "cuda:%d" % torch.cuda.current_device()
            else:
                device = "cpu"
        self.device = torch.device(device)
        self.model = torch.load(self.model_file_path, map_location=self.device)
        self.model.eval()
