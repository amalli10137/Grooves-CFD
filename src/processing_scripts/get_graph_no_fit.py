import csv
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import sys


def plot_y_velocity_from_csv(csv_file, output_file, re_file, max_time=None):
    times = []
    y_velocities = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        # Extract cell columns
        cell_columns = [header for header in headers if header.startswith('U_')]
        
        for row in reader:
            time = float(row['time'])
            if max_time is not None and time > max_time:
                continue
            
            y_components = []

            for cell_column in cell_columns:
                velocity_str = row[cell_column].strip('()')
                if velocity_str:
                    x, y, z = map(float, velocity_str.split())
                    y_components.append(y)
            
            if y_components:
                avg_y_velocity = sum(y_components) / len(y_components)
                times.append(time)
                y_velocities.append(avg_y_velocity)

    times = np.array(times)
    y_velocities = np.array(y_velocities)

    # Read the RE.txt file for the title
    with open(re_file, 'r') as file:
        re_lines = file.readlines()
        re_title = f"{re_lines[0].strip()}, {re_lines[1].strip()}"

    # Plotting the average y-component of velocity over time
    plt.figure(figsize=(10, 6))
    plt.plot(times, y_velocities, label='Average y-component of velocity')
    plt.xlabel('Time')
    plt.ylabel('Average y-component of velocity')
    plt.title(f'Uy vs Time ({re_title})')
    plt.legend()

    # Adding the equation and parameters to the plot
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    
    csv_file = "data/"+sys.argv[2]+"/cases/" + sys.argv[3] + "/" + sys.argv[1] + "/U_vs_time.csv"
    output_file = "data/"+sys.argv[2]+"/cases/" + sys.argv[3] + "/" + sys.argv[1] + "/Uy_vs_time_no_fit.png"
    re_file = "data/"+sys.argv[2]+"/cases/" + sys.argv[3] + "/" + sys.argv[1] + "/RE.txt"
    max_time = None  # Set the maximum time to be plotted, or None to plot all data
    plot_y_velocity_from_csv(csv_file, output_file, re_file, max_time)
