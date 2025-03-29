import mss
import numpy as np
import cv2
from collections import deque


DOWNSCALE_WIDTH = 160
DOWNSCALE_HEIGHT = 90

ROLLING_AVG_WINDOW = 50
SEIZURE_VAR_THRESHOLD = 3000

def compute_fft_energy(frame: cv2.typing.MatLike) -> float:
    """
    Compute the energy of high frequencies in a frame using FFT.
    """
    # Convert frame to grayscale (FFT works on single-channel images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Fast Fourier Transform (FFT)
    f_transform = np.fft.fft2(gray)
    
    # Shift the zero-frequency component to the center
    f_shift = np.fft.fftshift(f_transform)
    
    # Compute the magnitude spectrum (log-scaled for visibility)
    magnitude = np.abs(f_shift)
    
    # Sum high-frequency energy (excluding low-frequency center)
    rows, cols = magnitude.shape
    center_x, center_y = cols // 2, rows // 2
    high_freq_energy = np.sum(magnitude) - np.sum(magnitude[center_y-10:center_y+10, center_x-10:center_x+10])

    return high_freq_energy


def capture_screen_frame() -> cv2.typing.MatLike:
    """
    Captures the entire screen and returns it as a numpy array.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary screen
        screenshot = sct.grab(monitor)  # Take a screenshot
        frame = np.array(screenshot)

        # Resize for faster processing
        frame_resized = cv2.resize(frame, (DOWNSCALE_WIDTH, DOWNSCALE_HEIGHT))
        
        return frame_resized


def run():
    rolling_queue = deque(maxlen=ROLLING_AVG_WINDOW)  # Initialize a deque for rolling average

    while True:
        frame = capture_screen_frame()
        frame_energy = compute_fft_energy(frame)  # Compute FFT energy
        rolling_queue.append(frame_energy)  # Append current energy to the deque
        rolling_var = np.var(rolling_queue) / 1e10  # Calculate rolling variance and scale it

        if rolling_var > SEIZURE_VAR_THRESHOLD:
            print("seizure")

run()



