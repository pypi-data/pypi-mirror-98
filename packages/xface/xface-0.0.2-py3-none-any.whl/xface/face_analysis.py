# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import os

import numpy as np

from xface.core.image_cropper import crop_image_by_mat
from xface.model import FaceAlignment, FaceDetector, FaceRecognition


class Face:
    def __init__(self, *, bbox, det_score, landmarks, feature, sim_face_ids):
        """
        :param bbox: 脸部范围
        :param landmarks: 关键点位置
        :param det_score: 检测分数
        :param feature: 特征
        :param sim_face_ids: 相似人脸
        """
        self.bbox = bbox
        self.det_score = det_score
        self.landmarks = landmarks
        self.feature = feature
        self.sim_face_ids = sim_face_ids

    @classmethod
    def compute_sim(cls, face1, face2):
        feature1 = face1.feature if isinstance(face1, Face) else face1
        feature2 = face2.feature if isinstance(face2, Face) else face2
        return np.dot(feature1, feature2)


class FaceAnalysis:
    def __init__(self, *, model_path=None, with_mask=False, lock=False, load_alignment=True, load_recognition=True):
        """
        :param model_path: 模型路径
        :param with_mask: 是否使用口罩模型
        :param lock: get_faces是否加锁
        :param load_alignment: 是否加载关键点模型
        :param load_recognition: 是否加载人脸识别模型
        """
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'models')
        mask_flag = '2.0' if with_mask else '1.0'

        self.face_detector = FaceDetector(model_path, 'face_detection', 'face_detection_' + mask_flag)
        if load_alignment:
            self.face_alignment = FaceAlignment(model_path, 'face_alignment', 'face_alignment_' + mask_flag)
        else:
            self.face_alignment = None
        if load_recognition:
            self.face_recognition = FaceRecognition(model_path, 'face_recognition', 'face_recognition_' + mask_flag)
        else:
            self.face_recognition = None
        self.registered_faces = list()
        if lock:
            import threading
            self.lock = threading.Lock()
        else:
            class NoLock:

                def __enter__(self):
                    pass

                def __exit__(self, exc_type, exc_val, exc_tb):
                    pass

            self.lock = NoLock()

    def register_face(self, face_id, face):
        """
        注册人脸

        :param face_id: 唯一标识
        :param face: Face 或 Face.feature
        """
        self.registered_faces.append((face_id, face))

    def check_face(self, face, min_sim=0.6, max_count=1):
        """

        :param face: Face
        :param min_sim: 相似度下限
        :param max_count: 返回数量
        :return:
        """
        ret = list()
        for face_id, reg_face in self.registered_faces:
            sim = Face.compute_sim(face, reg_face)
            if sim > min_sim:
                ret.append((face_id, sim))
        ret = list(sorted(ret, key=lambda x: -x[1]))
        if max_count > 0:
            return ret[:max_count]
        else:
            return ret

    def load(self, device=None):
        self.face_detector.load(device)
        if self.face_alignment is not None:
            self.face_alignment.load(device)
        if self.face_recognition is not None:
            self.face_recognition.load(device)

    def get_faces(
            self,
            image,
            *,
            img_scaled=1.0,
            max_num=0,
            get_landmarks=True,
            get_feature=True,
            min_sim=0.6,
            match_num=1
    ):
        """

        :param image: 图片
        :param img_scaled: 图片已缩放比例（返回缩放前坐标）
        :param max_num: 最大返回人脸数（0为全部）
        :param get_landmarks: 是否返回关键点
        :param get_feature: 是否返回人脸识别相关参数
        :param min_sim: 人脸识别相似度下限
        :param match_num: 人脸识别匹配返回数量
        """
        with self.lock:
            dets = self.face_detector.detect(image)
            ret = list()
            if dets.shape[0] == 0:
                return ret
            if 0 < max_num < dets.shape[0]:
                area = (dets[:, 2] - dets[:, 0]) * (dets[:, 3] - dets[:, 1])
                img_center = image.shape[0] // 2, image.shape[1] // 2
                offsets = np.vstack([
                    (dets[:, 0] + dets[:, 2]) / 2 - img_center[1],
                    (dets[:, 1] + dets[:, 3]) / 2 - img_center[0]
                ])
                offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
                values = area - offset_dist_squared * 2.0  # some extra weight on the centering
                bindex = np.argsort(values)[::-1]  # some extra weight on the centering
                bindex = bindex[0:max_num]
                dets = dets[bindex, :]

            for det in dets:
                landmarks = None
                feature = None
                sim_face_ids = None
                if (get_landmarks or get_feature) and self.face_alignment is not None:
                    landmarks = self.face_alignment.get(image, det)
                    landmarks_list = []
                    for (x, y) in landmarks.astype(np.int32):
                        landmarks_list.extend((x, y))
                    cropped_image = crop_image_by_mat(image, landmarks_list)
                    if get_feature and self.face_recognition is not None:
                        feature = self.face_recognition.get(cropped_image)
                        sim_face_ids = self.check_face(feature, min_sim=min_sim, max_count=match_num)
                ret.append(Face(
                    bbox=(det[:4] / img_scaled).astype(np.int).tolist(),
                    det_score=float(det[4]),
                    landmarks=(landmarks / img_scaled).astype(np.int).tolist(),
                    feature=feature,
                    sim_face_ids=sim_face_ids
                ))
            return ret
