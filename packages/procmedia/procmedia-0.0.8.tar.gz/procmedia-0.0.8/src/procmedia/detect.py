import numpy as np
import cv2
from . import utils
import magic


class Detector:
    def __init__(self, file_path: str, haar_path: str, out_path=""):
        self.file_path = file_path
        self.haar_path = haar_path

        self._type = self._check_file_type()
        print(self._type + " detected!")

        if out_path == "":
            if self._type == "video/mp4":
                self.out_path = "./detected/"
            else:
                self.out_path = "detected.jpg"
        else:
            self.out_path = out_path

    def detect(self):
        if self._type == "video/mp4":
            self._process_video()
        else:
            cv2.imwrite(self.out_path, self._process_image())

    def _process_video(self, scale_factor=1.2, min_neighbours=5):
        cascade = cv2.CascadeClassifier(self.haar_path)
        cap = cv2.VideoCapture(self.file_path)

        frame = 0
        print("Video processing")
        i = 0
        while not (frame is None):
            _, frame = cap.read()
            rect = cascade.detectMultiScale(frame,
                                            scaleFactor=scale_factor,
                                            minNeighbors=min_neighbours)
            frame = utils.draw_rectangles(rect, frame)
            cv2.imwrite(self.out_path + str(i) + ".jpg", frame)
            i += 1
        print("Video processing end")

    def _process_image(self, scale_factor=1.2, min_neighbours=5) -> np.array:
        cascade = cv2.CascadeClassifier(self.haar_path)
        img = cv2.imread(self.file_path)
        rect = cascade.detectMultiScale(img,
                                        scaleFactor=scale_factor,
                                        minNeighbors=min_neighbours)
        img = utils.draw_rectangles(rect, img)
        return img

    def _check_file_type(self) -> str:
        return magic.from_file(self.file_path, mime=True)
