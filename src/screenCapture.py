import mss
import numpy as np
import cv2
from collections import deque


DOWNSCALE_WIDTH = 160
DOWNSCALE_HEIGHT = 90
ROLLING_AVG_WINDOWS = 20

def compute_fft_energy(frame):
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



def capture_screen():
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
    

prev_energy = 0
rolling = deque(maxlen=ROLLING_AVG_WINDOWS)  # Initialize a deque for rolling average

# Example usage: Capture and display frames
while True:
    start_time = cv2.getTickCount()  # Start time for performance measurement
    frame = capture_screen()

    
    # cv2.imshow("Screen Capture", frame)  # Show the captured frame
    current_energy = compute_fft_energy(frame)  # Compute FFT energy
    rolling.append(current_energy)  # Append current energy to the deque
    rolling_var = np.var(rolling) / 1e10  # Calculate rolling variance
    print(f"Rolling Variance: {rolling_var}")  # Print the rolling variance
    # print(f"Rolling Average Energy: {rolling_avg}")  # Print the rolling average
    change = abs(current_energy - prev_energy) / 1e6
    # print(f"High Frequency Energy: {change}")  # Print the energy value
    end_time = cv2.getTickCount()  # End time for performance measurement
    time_taken = (end_time - start_time) / cv2.getTickFrequency()  # Calculate time taken
    # print(f"Time taken for FFT: {time_taken:.4f} seconds")  # Print time taken



