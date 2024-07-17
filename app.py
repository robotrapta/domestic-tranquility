#!/usr/bin/env python3
import time
import traceback

from groundlight import Groundlight
from imgcat import imgcat
import cv2
import framegrab


class KitchenWatcher():

    def __init__(self):
        self.camera = framegrab.FrameGrabber.from_yaml("./framegrab.yaml")[0]
        self.motdet = framegrab.MotionDetector(pct_threshold=3, val_threshold=50)
        self.gl = Groundlight()
        self.detector = self.gl.get_or_create_detector(
            name="counter-clear",
            query="Are there any dirty dishes on the counter?",
        )

    def run(self):
        while True:
            try:
                self.process_frame()
            except Exception as e:
                traceback.print_exc()
                time.sleep(60)
    
    def process_frame(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        big_img = self.camera.grab()  # big_img is a numpy array
        img = cv2.resize(big_img, (800, 600))  # smaller for preview and motdet
        if not self.motdet.motion_detected(img):
            print(f"no motion at {now}")
        else:
            imgcat(img)
            img_query = self.gl.ask_ml(detector=self.detector, image=big_img)
            if img_query.result.label == "YES":
                print(f"Dirty dishes detected at {now}")
            else:
                print(f"No dirty dishes found at {now}")
        time.sleep(60)

if __name__ == "__main__":
    KitchenWatcher().run()
