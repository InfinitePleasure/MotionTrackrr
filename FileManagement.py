import time

import cv2
import numpy as np
from PyQt5.QtWidgets import QMessageBox

import EventListener


class FileManagement:
    files = []


def get_frames() -> np.ndarray:
    if len(FileManagement.files) > 0 and (len(FileManagement.files) > 0 and FileManagement.files[0] != ''):
        for file in FileManagement.files:
            cap = cv2.VideoCapture(file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            frames = []
            i = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
                time.sleep(0.01)
                i += 1
            cap.release()
            return frames, fps


def extract(extract_dir, name):
    img = EventListener.EventListener.current_frames[EventListener.EventListener.index]
    height, width, layers = img.shape
    size = (width, height)

    out = cv2.VideoWriter(str(extract_dir) + '/' + str(name) + '.mp4', -1, EventListener.EventListener.fps, size)

    for frame in EventListener.EventListener.current_frames:
        frame2 = cv2.resize(frame, size)
        out.write(frame2)

    out.release()
