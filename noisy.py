#!/usr/bin/env python3
import time
from gtts import gTTS
import os
import tempfile

class VoiceAlerts():
    """Plays sounds of a TTS voice reading messages.
    """

    def __init__(self, cooldown=30, message:str="voice alert"):
        self.message = message
        self.cooldown = cooldown
        self.last_sound_played_at = 0  # start at 0 so that sound always plays first time
        self.temp_dir = tempfile.TemporaryDirectory()
        self.sound_path = os.path.join(self.temp_dir.name, "alert.mp3")
        self._generate_sound()

    def _generate_sound(self):
        """Generates the TTS sound file from the message."""
        tts = gTTS(text=self.message, lang='en')
        tts.save(self.sound_path)

    def alert(self):
        """Plays a sound if the last time it was played was more than `cooldown` seconds ago.
        """
        elapsed = time.time() - self.last_sound_played_at
        if elapsed > self.cooldown:
            print(f"Playing voice alert: {self.message}")
            os.system(f"mpg321 {self.sound_path}")
            self.last_sound_played_at = time.time()
        else:
            print(f"Last sound was played {elapsed:.1f} seconds ago - too recent to play again")

    def __del__(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()


if __name__ == "__main__":
    print("Testing voice alert...")
    alert = VoiceAlerts(message="Voice alert test")
    alert.alert()
