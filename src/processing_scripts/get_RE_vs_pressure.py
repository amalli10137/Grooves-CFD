import os
import subprocess
import sys


import matplotlib.pyplot as plt
import numpy as np

# Define the directory structure
base_dir = "cases"
output_dir = "RE_vs_pressure.png"
cases = ["5e-6", "10e-6", "15e-6", "20e-6", "25e-6", "30e-6", "35e-6", "40e-6", "45e-6", "50e-6", "55e-6", "60e-6", "65e-6", "70e-6", "75e-6"]

pressure_drops = []
reynolds_numbers = []

# Loop through each case directory and read the RE.txt file
for case in cases:
    file_path = os.path.join(base_dir, case, "RE.txt")
    with open(file_path, 'r') as file:
        reynolds_number = float(file.readline().strip())
        pressure_drop = float(case.rstrip('e-6'))
        
        reynolds_numbers.append(reynolds_number)
        pressure_drops.append(pressure_drop)

# Convert to numpy arrays for convenience
pressure_drops = np.array(pressure_drops)
reynolds_numbers = np.array(reynolds_numbers)

# Calculate the linear fit
coefficients = np.polyfit(pressure_drops, reynolds_numbers, 1)
linear_fit = np.poly1d(coefficients)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(pressure_drops, reynolds_numbers, 'o', label='Data Points')

# Plot the linear fit
plt.plot(pressure_drops, linear_fit(pressure_drops), '-', label=f'Linear Fit: y={coefficients[0]:.2f}x + {coefficients[1]:.2f}')

# Label the axes
plt.xlabel("Pressure Drop in *10⁻⁶ Pa")
plt.ylabel("Reynolds Number")
plt.title("Reynolds Number vs Pressure Drop")

# Add a legend
plt.legend()

# Save the plot as an image file
plt.savefig(output_dir)

# Show the plot
plt.grid(True)
plt.show()
