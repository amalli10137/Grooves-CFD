import os
import re
import matplotlib.pyplot as plt
import sys

# Directory structure

base_dir = sys.argv[1]

# Initialize lists for x and y values
groove_heights = []
decay_rates = []

# Iterate through each subfolder in the cases directory
for subfolder in os.listdir(base_dir):
    subfolder_path = os.path.join(base_dir, subfolder)
    # Ensure the subfolder name follows the pattern of scientific notation (e.g., 5e-6)
    if os.path.isdir(subfolder_path): #and re.match(r'^\d+e-\d+$', subfolder):
        re_file_path = os.path.join(subfolder_path, 'RE.txt')
        if os.path.isfile(re_file_path):
            with open(re_file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    try:
                        groove_height = float(lines[1].strip())
                        decay_rate = -float(lines[2].strip())
                        groove_heights.append(groove_height)
                        decay_rates.append(decay_rate)
                    except ValueError:
                        # Handle cases where the conversion to float fails
                        continue

# Plotting the data
plt.figure(figsize=(10, 6))
plt.scatter(groove_heights, decay_rates, color='blue', label='Data points')
plt.xlabel('Groove Height (cm)')
plt.ylabel('Decay Rate (Ae^-bt: value of b)')
plt.title('Groove Height vs Decay Rate')
plt.legend()
plt.grid(True)

# Save the plot as RE_vs_decay.png in the cases folder
output_path = os.path.join(base_dir, 'Groove_height_vs_decay.png')
plt.savefig(output_path)

# Show the plot
