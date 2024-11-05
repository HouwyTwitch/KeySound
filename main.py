import numpy as np
import pyaudio
from pynput import keyboard
import random
import threading
import queue

class KeyboardSoundPlayer:
    """Class to play sounds corresponding to keyboard events."""

    def __init__(self, sample_rate=44100, volume=0.05):
        """Initialize the sound player with specified sample rate and volume.

        Args:
            sample_rate (int): The sample rate for audio playback.
            volume (float): The volume level for the sound playback.
        """
        self.sample_rate = sample_rate
        self.volume = volume
        self.p = pyaudio.PyAudio()

        # Open a single stream for all sounds
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sample_rate,
                                  output=True)

        # Define frequencies for various key sounds
        self.key_sounds = {
            "letter": 400,      # Frequency for letter keys
            "enter": 350,       # Frequency for Enter key
            "space": 320,       # Frequency for Spacebar
            "backspace": 450,   # Frequency for Backspace key
            "shift": 370,       # Frequency for Shift key
        }

        # Queue for sound playback
        self.sound_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.playback_thread = threading.Thread(target=self._play_sounds)
        self.playback_thread.start()

    def play_key_sound(self, key_type):
        """Queue a sound corresponding to a specific key type.

        Args:
            key_type (str): The type of key that was pressed.
        """
        frequency = self.key_sounds.get(key_type, 400)  # Default to "letter" frequency if key_type not found

        # Add a small random variation to the frequency
        frequency += random.uniform(-3, 3)  # Small random frequency variation

        # Short duration for snappy response
        duration = 0.05  # 50 ms for a shorter sound
        self.sound_queue.put((frequency, duration))  # Queue the sound with a short duration

    def _play_sounds(self):
        """Play sounds from the queue."""
        while not self.stop_event.is_set():
            try:
                frequency, duration = self.sound_queue.get(timeout=0.05)  # Wait for a sound to be queued
                self._play_sound(frequency, duration)
                self.sound_queue.task_done()  # Mark the sound as processed
            except queue.Empty:
                continue  # Continue if the queue is empty

    def _play_sound(self, frequency, duration):
        """Generate and play a sound with a smooth envelope effect.

        Args:
            frequency (float): Frequency of the sound to be played.
            duration (float): Duration of the sound in seconds.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

        # Create the waveform
        waveform = np.sin(2 * np.pi * frequency * t)

        # Apply a smooth envelope (attack-decay) for a gentle sound
        attack_duration = int(0.01 * len(t))  # First 10 ms for attack
        decay_duration = len(t) - attack_duration  # Remaining for decay

        # Create an attack and decay envelope
        attack_envelope = np.linspace(0, 1, attack_duration)  # Attack phase
        decay_envelope = np.linspace(1, 0, decay_duration)    # Decay phase
        envelope = np.concatenate([attack_envelope, decay_envelope])

        # Adjust the waveform with volume and envelope
        waveform = self.volume * waveform * envelope

        # Ensure the waveform starts at zero
        waveform[0] = 0.0  # Prevent click sound at the beginning

        # Write to the audio stream
        self.stream.write(waveform.astype(np.float32).tobytes())

    def close(self):
        """Close the audio stream and terminate PyAudio."""
        self.stop_event.set()  # Signal the playback thread to stop
        self.playback_thread.join()  # Wait for the thread to finish
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


# Initialize the player and a set to keep track of currently pressed keys
player = KeyboardSoundPlayer()
pressed_keys = set()

# Define a function to handle key press events
def on_press(key):
    """Handle key press events to play corresponding sounds.

    Args:
        key (Key): The key that was pressed.
    """
    global pressed_keys  # Access the outer scope's pressed_keys variable
    key_str = str(key)  # Convert key to string to make it hashable
    pressed_keys.add(key_str)  # Add to the set of pressed keys

    # Check for Ctrl + Shift + Q to quit the program
    if ('Key.ctrl_l' in pressed_keys and 
        'Key.shift' in pressed_keys and 
        "'\\x11'" in pressed_keys):
        # Close the player and stop the listener
        player.close()
        return False  # Stop the listener

    try:
        # Map different key types to the corresponding sounds
        if key == keyboard.Key.enter:
            player.play_key_sound("enter")
        elif key == keyboard.Key.space:
            player.play_key_sound("space")
        elif key == keyboard.Key.backspace:
            player.play_key_sound("backspace")
        elif key == keyboard.Key.shift:
            player.play_key_sound("shift")
        else:
            player.play_key_sound("letter")  # For all other keys
    except Exception as e:
        print(f"Error playing sound: {e}")

# Define a function to handle key release events
def on_release(key):
    """Handle key release events.

    Args:
        key (Key): The key that was released.
    """
    global pressed_keys  # Access the outer scope's pressed_keys variable
    key_str = str(key)  # Convert key to string to make it hashable
    if key_str in pressed_keys:
        pressed_keys.remove(key_str)  # Remove from the set of pressed keys

# Start listening to keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Press keys to hear sounds. Press Ctrl + Shift + Q to exit.")
    listener.join()

# Cleanup when the listener stops
player.close()
