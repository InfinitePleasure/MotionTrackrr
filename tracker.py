import time

import cv2

import EventListener


def track(img, bboxx):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(img, bboxx)

    frames_len = len(EventListener.EventListener.current_frames)

    for index, frame in enumerate(EventListener.EventListener.current_frames):
        ok, bbox = tracker.update(frame)
        if ok:
            EventListener.EventListener.current_bbox.append(bbox)

        print((index/frames_len) * 100)

        K = cv2.waitKey(1)
        if (K == 27):
            break

    cv2.destroyAllWindows()



