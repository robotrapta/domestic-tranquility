#! /usr/bin/env python3
from imgcat import imgcat

from app import KitchenWatcher

if __name__ == "__main__":
    gw = KitchenWatcher()
    print("Testing camera...")
    img = gw.camera.grab()
    print(f"Full image shape: {img.shape}.  Sending to iTerm2...")
    imgcat(img)
    print("Done.")
