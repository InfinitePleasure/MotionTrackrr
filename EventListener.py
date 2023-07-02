class EventListener:
    tracked: bool = False
    index = 0
    x, y, w, h = 0, 0, 0, 0
    max_x, max_y, max_w, max_h, fps = 0, 0, 0, 0, 30
    current_frames = []
    current_bbox = []
