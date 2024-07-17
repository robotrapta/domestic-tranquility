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
        # Timing constants
        self.exception_backoff_s = 60
        self.motion_interval_s = 60
        self.no_motion_post_anyway_s = 3600
        self.last_motion_post = time.time() - self.no_motion_post_anyway_s

    def run(self):

        while True:
            try:
                self.process_frame()
            except Exception as e:
                traceback.print_exc()
                time.sleep(self.exception_backoff_s)
    
    def process_frame(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        big_img = self.camera.grab()  # big_img is a numpy array
        img = cv2.resize(big_img, (800, 600))  # smaller for preview and motdet
        motion_detected = self.motdet.motion_detected(img)
        if not motion_detected:
            print(f"no motion at {now}")
            if time.time() - self.last_motion_post > self.no_motion_post_anyway_s:
                print(f"No motion detected for {self.no_motion_post_anyway_s}s, posting anyway")
                motion_detected = True
        if motion_detected:
            self.last_motion_post = time.time()
            imgcat(img)
            img_query = self.gl.ask_ml(detector=self.detector, image=big_img)
            if img_query.result.label == "YES":
                print(f"Dirty dishes detected at {now}")
            else:
                print(f"No dirty dishes found at {now}")
        time.sleep(self.motion_interval_s)

if __name__ == "__main__":
    KitchenWatcher().run()
