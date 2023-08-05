#!/usr/bin/env python

import numpy as np
import cv2
from edgeimpulse.runner import ImpulseRunner

class CameraImpulseRunner(ImpulseRunner):
    def __init__(self, model_path: str):
        super(CameraImpulseRunner, self).__init__(model_path)
        self.closed = True
        self.labels = []
        self.dim = (0, 0)
        self.videoCapture = None

    def init(self):
        model_info = super(CameraImpulseRunner, self).init()

        width = model_info['model_parameters']['image_input_width'];
        height = model_info['model_parameters']['image_input_height'];

        if width == 0 or height == 0:
            raise Exception('Model file "' + self._model_path + '" is not suitable for image recognition')

        self.dim = (width, height)
        self.labels = model_info['model_parameters']['labels']
        self.videoCapture = cv2.VideoCapture(0)
        return model_info

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True

    def classify(self):
        while not self.closed:
            # Capture frame-by-frame
            ret, brg = self.videoCapture.read()
            if ret:
                resizedImg = cv2.resize(brg, self.dim, interpolation = cv2.INTER_AREA)
                features = np.array(resizedImg).flatten().tolist()
                res = super(CameraImpulseRunner, self).classify(features)
                yield res, brg
