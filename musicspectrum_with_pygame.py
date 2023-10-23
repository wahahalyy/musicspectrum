import pygame
import pyaudio
import numpy as np
import scipy.signal as signal

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 # Frames per second
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CLOCK_RADIUS = 200 # Radius of the clock face
CLOCK_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # Center of the clock face
HOUR_LENGTH = 100 # Length of the hour hand
MINUTE_LENGTH = 150 # Length of the minute hand
SECOND_LENGTH = 180 # Length of the second hand
SPECTRUM_RADIUS = CLOCK_RADIUS + 50 # Radius of the spectrum circle
SPECTRUM_BINS = 32 # Number of frequency bins for
# Define some functions
def draw_clock_face(screen):
    # Draw the clock face as a white circle
    pygame.draw.circle(screen, WHITE, CLOCK_CENTER, CLOCK_RADIUS, 0)
    # Draw the clock ticks as black lines
    for angle in range(0, 360, 6):
        # Convert angle to radians
        rad = np.radians(angle)
        # Calculate the start and end points of the line
        x1 = int(CLOCK_CENTER[0] + np.cos(rad) * (CLOCK_RADIUS - 10))
        y1 = int(CLOCK_CENTER[1] - np.sin(rad) * (CLOCK_RADIUS - 10))
        x2 = int(CLOCK_CENTER[0] + np.cos(rad) * CLOCK_RADIUS)
        y2 = int(CLOCK_CENTER[1] - np.sin(rad) * CLOCK_RADIUS)
        # Draw the line
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)

def draw_clock_hand(screen, angle, length, color):
    # Convert angle to radians
    rad = np.radians(angle)
    # Calculate the end point of the line
    x = int(CLOCK_CENTER[0] + np.cos(rad) * length)
    y = int(CLOCK_CENTER[1] - np.sin(rad) * length)
    # Draw the line
    pygame.draw.line(screen, color, CLOCK_CENTER, (x, y), 4)

def draw_spectrum_bar(screen, angle, length, color):
    # Convert angle to radians
    rad = np.radians(angle)
    # Calculate the start and end points of the line
    x1 = int(CLOCK_CENTER[0] + np.cos(rad) * CLOCK_RADIUS)
    y1 = int(CLOCK_CENTER[1] - np.sin(rad) * CLOCK_RADIUS)
    x2 = int(CLOCK_CENTER[0] + np.cos(rad) * (CLOCK_RADIUS + length))
    y2 = int(CLOCK_CENTER[1] - np.sin(rad) * (CLOCK_RADIUS + length))
    # Draw the line
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 4)

def get_audio_spectrum(stream):
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)
    # Convert data to numpy array
    data = np.frombuffer(data, dtype=np.int16)
    # Apply a window function to reduce spectral leakage
    data = data * signal.windows.hann(CHUNK_SIZE)
    # Compute the power spectrum using FFT
    spectrum = np.abs(np.fft.rfft(data)) ** 2
    # Normalize the spectrum by the chunk size
    spectrum = spectrum / CHUNK_SIZE
    # Return the spectrum as a list
    return spectrum.tolist()
# Initialize pygame and pyaudio modules
pygame.init()
pyaudio = pyaudio.PyAudio()

# Create a screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clock and Spectrum")

# Create a clock object
clock = pygame.time.Clock()

# Create a stream object
CHUNK_SIZE = 1024 # Number of samples per chunk
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 1 # Number of channels
RATE = 44100 # Sampling rate
stream = pyaudio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Define some variables
running = True # Flag for the main loop
time = pygame.time.get_ticks() # Current time in milliseconds
spectrum = [0] * SPECTRUM_BINS # Current spectrum data

# Enter the main loop
while running:
    # Limit the frame rate
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        # Quit if the user closes the window or presses ESC
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update the time and spectrum variables every 100 milliseconds
    if pygame.time.get_ticks() - time >= 100:
        time = pygame.time.get_ticks()
        spectrum = get_audio_spectrum(stream)

    # Clear the screen with black color
    screen.fill(BLACK)

    # Draw the clock face
    draw_clock_face(screen)

    # Get the current hour, minute and second
    hour = pygame.time.localtime().tm_hour % 12
    minute = pygame.time.localtime().tm_min
    second = pygame.time.localtime().tm_sec

    # Calculate the angles of the clock hands in degrees
    hour_angle = (hour + minute / 60) * 30 - 90
    minute_angle = (minute + second / 60) * 6 - 90
    second_angle = second * 6 - 90

    # Draw the clock hands
    draw_clock_hand(screen, hour_angle, HOUR_LENGTH, RED)
    draw_clock_hand(screen, minute_angle, MINUTE_LENGTH, GREEN)
    draw_clock_hand(screen, second_angle, SECOND_LENGTH, BLUE)

    # Calculate the angles of the spectrum bars in degrees
    spectrum_angles = np.linspace(-90, 270, SPECTRUM_BINS + 1)

    # Draw the spectrum bars with different colors based on their intensity
    for i in range(SPECTRUM_BINS):
        # Map the spectrum intensity to a length between 0 and 50 pixels
        length = int(np.interp(spectrum[i], [0, max(spectrum)], [0, 50]))
        # Map the spectrum intensity to a color between black and white
        color = int(np.interp(spectrum[i], [0, max(spectrum)], [0, 255]))
        color = (color, color, color)
        # Draw the spectrum bar
        draw_spectrum_bar(screen, spectrum_angles[i], length, color)

    # Update the display
    pygame.display.flip()

# Close the stream and terminate the modules
stream.stop_stream()
stream.close()
pyaudio.terminate()
pygame.quit()
