#!/usr/bin/env python

import numpy as np
import cv2
from edgeimpulse.runner import ImpulseRunner
import time

class CameraImpulseRunner(ImpulseRunner):
    def __init__(self, model_path: str):
        super(CameraImpulseRunner, self).__init__(model_path)
        self.closed = True
        self.labels = []
        self.dim = (0, 0)
        self.videoCapture = cv2.VideoCapture()
        self.isGrayscale = False

    def init(self):
        model_info = super(CameraImpulseRunner, self).init()

        width = model_info['model_parameters']['image_input_width'];
        height = model_info['model_parameters']['image_input_height'];

        if width == 0 or height == 0:
            raise Exception('Model file "' + self._model_path + '" is not suitable for image recognition')

        self.dim = (width, height)
        self.labels = model_info['model_parameters']['labels']
        self.isGrayscale =  model_info['model_parameters']['input_features_count'] == width * height
        return model_info

    def __enter__(self):
        self.videoCapture.open(0)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.videoCapture.release()
        self.closed = True

    def classify(self, data):
        return super(CameraImpulseRunner, self).classify(data)

    def classifier(self):
        while not self.closed and self.videoCapture.isOpened():
            ret, img = self.videoCapture.read()
            print(ret)
            if ret:
                if self.isGrayscale:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                resizedImg = cv2.resize(img, self.dim, interpolation = cv2.INTER_AREA)
                features = np.array(resizedImg).flatten().tolist()
                res = self.classify(features)
                yield res, img
