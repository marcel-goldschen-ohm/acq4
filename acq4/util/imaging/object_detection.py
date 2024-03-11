from threading import RLock

import numpy as np
import scipy.stats
from PIL import Image
from typing import Optional

from acq4.devices.Camera.frame import Frame
from acq4.util.future import Future
from pyqtgraph import SRTTransform3D
from teleprox import ProcessSpawner
from teleprox.shmem import SharedNDArray

from yolo import YOLO  # todo put this someplace

_lock = RLock()
_remote_process: Optional[ProcessSpawner] = None
_shared_array: Optional[SharedNDArray] = None
_yolo: Optional[YOLO] = None


def _get_yolo() -> YOLO:
    global _yolo
    if _yolo is None:
        _yolo = YOLO()
    return _yolo


def normalize(image: Image, min_in=None, max_in=None):
    # TODO reimplement it with no-copy, maybe?
    if min_in is None:
        # min_in = scipy.stats.scoreatpercentile(image, 5)
        min_in = np.min(image)
        # min_in = 0
    if max_in is None:
        # max_in = scipy.stats.scoreatpercentile(image, 90)
        max_in = np.max(image)
        # max_in = 65535
    min_out = 0
    max_out = 255  # maxmimum intensity (output)
    image = (image - np.uint16(min_in)) * (
            ((max_out - min_out) / (max_in - min_in)) + min_out
    )
    # image = (image - np.uint16(min_in)) * (
    #     (max_out / (max_in - min_in))
    # )
    image = scipy.ndimage.zoom(image, 3)
    offset_w = int(image.shape[0] * 0.3)
    offset_h = int(image.shape[1] * 0.3)
    margin_w = int(image.shape[0] * 0.4)
    margin_h = int(image.shape[1] * 0.4)
    image = image[offset_w:offset_w + margin_w, offset_h:offset_h + margin_h]
    return Image.fromarray(image.astype(np.uint8))


def _get_shared_array(data: np.ndarray) -> SharedNDArray:
    global _shared_array
    # TODO what if someone else is using it?!
    if _shared_array is not None and _shared_array.data.shape != data.shape:
        # it might still be in use, so just let the normal shared memory cleanup do unlink
        _shared_array.shmem.close()
        _shared_array = None
    if _shared_array is None:
        _shared_array = SharedNDArray.copy(data)
    else:
        _shared_array.data[:] = data
    return _shared_array


def _get_remote_process():
    global _remote_process
    # TODO what if someone else is using it?!
    # TODO how does cleanup happen?
    if _remote_process is None:
        # no local server forces no proxies, only serialization and shared mem
        _remote_process = ProcessSpawner(name="ACQ4 Object Detection", start_local_server=False)
    return _remote_process


@Future.wrap
def detect_neurons(frame: Frame, _future: Future):
    shared_array = _get_shared_array(frame.data())
    transform = frame.globalTransform()
    _future.checkStop()
    with _lock:
        remote_process = _get_remote_process()
        rmt_array = remote_process.client.transfer(shared_array)
        rmt_this = remote_process.client._import("acq4.util.imaging.object_detection")
        _future.checkStop()
        return rmt_this._do_neuron_detection(rmt_array.data, transform)


def _do_neuron_detection(data: np.ndarray, transform: SRTTransform3D) -> list:
    image = Image.fromarray(data)
    image = normalize(image)
    my_yolo = _get_yolo()
    boxes = list(my_yolo.get_boxes(image).keys())

    # for _ in range(3):
    #     start_x = np.random.randint(0, 236)
    #     start_y = np.random.randint(0, 236)
    #     boxes.append((
    #         start_x,
    #         start_y,
    #         start_x + np.random.randint(12, 22),
    #         start_y + np.random.randint(12, 22)))

    def xyxy_to_rect(box: tuple):
        start_x, start_y, end_x, end_y = box
        start = transform.map((start_x, start_y))
        end = transform.map((end_x, end_y))
        return start, end
    return [xyxy_to_rect(box) for box in boxes]  # TODO filter by class? score?
