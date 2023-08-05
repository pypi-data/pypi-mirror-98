# Edge Impulse Linux SDK for Python

This library lets you run machine learning models and collect sensor data on Linux machines using Python. This SDK is part of [Edge Impulse](https://www.edgeimpulse.com) where we enable developers to create the next generation of intelligent device solutions with embedded machine learning. [Start here to learn more and train your first model](https://docs.edgeimpulse.com).


`pip install edgeimpulse`

## runner.py

Implements the `ImpulseRunner`

## use:

```
from edgeimpulse.runner import ImpulseRunner
import signal
runner = None

def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

...
runner = ImpulseRunner(modelfile)
model_info = runner.init()
...
res = runner.classify(features[:window_size].tolist())
```


## Classify from microphone in real-time

```
from edgeimpulse.audio import AudioImpulseRunner
...
with AudioImpulseRunner('/path/to/your/model') as runner:
    runner.init()
    for res in runner.classify():
        print(res)

```

## Classify from camera in real-time

```
from edgeimpulse.camera import CameraImpulseRunner
import cv2

with CameraImpulseRunner('/path/to/your/model') as runner:
    runner.init()
    for res, img in runner.classify():
        print(res)
        cv2.imshow('frame',img)
```


## examples:

```
/camera
/microphone
```


### camera
Classifies frames grabbed directly from the webcam.

### microphone
Classifies audio acquired directly from the audio interface.
