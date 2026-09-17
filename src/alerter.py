import pygame
import threading
import os

class AudioAlerter:
    """
    Cross-platform audio alerter using pygame. 
    Runs in a separate thread so it doesn't block the main CV loop.
    """
    
    def __init__(self, sound_file="assets/alert.wav"):
        self.sound_file = sound_file
        # Initialize pygame mixer only
        pygame.mixer.init()
        self.is_playing = False
        
        # We need a generic alert sound if one doesn't exist
        self._ensure_sound_file()
        self.sound = pygame.mixer.Sound(self.sound_file)
        
    def _ensure_sound_file(self):
        """Creates a dummy sound file if it doesn't exist for the purpose of the project."""
        os.makedirs(os.path.dirname(self.sound_file), exist_ok=True)
        if not os.path.exists(self.sound_file):
            # Create a simple beep sound using numpy and scipy if needed,
            # or just rely on the user to put an alert.wav there.
            # We'll generate a simple 440Hz beep using scipy here to be perfectly self-contained.
            try:
                import numpy as np
                from scipy.io import wavfile
                sample_rate = 44100
                t = np.linspace(0, 1.0, sample_rate, False)
                tone = np.sin(440 * t * 2 * np.pi)
                audio = np.int16(tone * 32767)
                wavfile.write(self.sound_file, sample_rate, audio)
            except ImportError:
                print("Warning: Could not generate alert sound. Please place an 'alert.wav' in 'assets/'")

    def _play_sound(self):
        self.is_playing = True
        self.sound.play()
        pygame.time.wait(int(self.sound.get_length() * 1000))
        self.is_playing = False

    def trigger_alert(self):
        """Triggers the alert sound if it's not already playing."""
        if not self.is_playing:
            threading.Thread(target=self._play_sound, daemon=True).start()
            
    def release(self):
        """Cleans up pygame mixer."""
        pygame.mixer.quit()
