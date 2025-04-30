import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create a uniform array 'x' with 100 points between 0 and 1
x = np.linspace(0, 1, 100)

# Step 2: Compute 'y' as the sum of the sine functions
y = np.sin(10 * np.pi * x) + np.sin(20 * np.pi * x)

# Step 3: Initialize a 100x100 array to store noisy data
noisy_data = np.zeros((100, 100))

# Step 4: Add Gaussian noise to 'y' and store the result in the 'noisy_data' array
for i in range(100):
    noise = np.random.normal(0, np.abs(y) / 2)
    noisy_y = y + noise
    noisy_data[i, :] = noisy_y

# Step 5: Plot the noisy data as individual lines
plt.figure(figsize=(10, 6))
for i in range(100):
    plt.plot(x, noisy_data[i, :], linewidth=0.5)

plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Noisy Data Visualization')
plt.show()

# Calculate the mean and standard deviation for each x-value
mean_y = np.mean(noisy_data, axis=0)
std_y = np.std(noisy_data, axis=0)

# Plot the noisy data as individual lines (optional)
plt.figure(figsize=(10, 6))

# Plot the mean curve
plt.plot(x, mean_y, linewidth=2, label='Mean')

# Plot the mean curve with +/- one standard deviation as shaded regions
plt.fill_between(x, mean_y - std_y, mean_y + std_y, alpha=0.3, label='1 Standard Deviation')

plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Mean and Standard Deviation of Noisy Data')
plt.legend()
plt.show()

from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt

# Compute the FFT of the mean noisy data
y_fft = fft(mean_y)
freqs = fftfreq(len(mean_y), x[1] - x[0])

# Normalize the magnitude by the number of points
y_magnitude = np.abs(y_fft) / np.max(np.abs(y_fft))

# Plot the magnitude vs. frequency
plt.figure(figsize=(10, 6))
plt.plot(freqs[:len(freqs)//2], y_magnitude[:len(freqs)//2])
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Magnitude vs. Frequency')
plt.show()

# Design a bandpass Butterworth filter and apply it to the mean noisy data
lowcut, highcut = 4, 6
nyquist = 0.5 * (1 / (x[1] - x[0]))
low = lowcut / nyquist
high = highcut / nyquist
b, a = butter(2, [low, high], btype='band')

filtered_mean_y = filtfilt(b, a, mean_y)

# Plot the denoised/filtered data and the exact sin(10πx) function
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(10 * np.pi * x), label='Exact: sin(10πx)')
plt.plot(x, -filtered_mean_y[::-1], label='De-noised / Filtered Data')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Filtered Data and Exact sin(10πx) Function')
plt.legend()
plt.show()