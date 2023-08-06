import cv2
import numpy as np


def draw_rectangles(rect, img, line_size=3):
    for (x, y, w, h) in rect:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)

    return img
