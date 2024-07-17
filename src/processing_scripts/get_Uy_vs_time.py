import csv
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import sys

def simple_exponential_decay(t, A, b):
    return A * np.exp(-b * t)

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

    # Calculate the average y-velocity at t=0
    y_offset = y_velocities[0]

    # Center the y-velocities around zero
    centered_y_velocities = y_velocities - y_offset

    # Find the global maximum and include it for fitting
    global_max_index = np.argmax(centered_y_velocities)
    fit_times = times[global_max_index:]
    fit_centered_y_velocities = centered_y_velocities[global_max_index:]

    # Find the local maxima in the fitting data
    peaks, _ = find_peaks(fit_centered_y_velocities)

    # Include the global maximum in the list of peaks
    peaks = np.insert(peaks, 0, 0)

    peak_times = fit_times[peaks]
    peak_y_velocities = fit_centered_y_velocities[peaks]

    # Fit the data to the simple exponential decay function
    initial_guess = [peak_y_velocities[0], 0.1]
    popt, pcov = curve_fit(simple_exponential_decay, peak_times, peak_y_velocities, p0=initial_guess)

    # Generate fitted values for the time range after the global maximum
    fitted_times = fit_times
    fitted_y_velocities = simple_exponential_decay(fitted_times, *popt) + y_offset

    # Read the RE.txt file for the title
    with open(re_file, 'r') as file:
        re_lines = file.readlines()
        re_title = f"{re_lines[0].strip()}, {re_lines[1].strip()}"

    # Plotting the average y-component of velocity over time
    plt.figure(figsize=(10, 6))
    plt.plot(times, y_velocities, label='Average y-component of velocity')
    plt.plot(peak_times, peak_y_velocities + y_offset, 'bo', label='Local maxima (including global)')
    plt.plot(fitted_times, fitted_y_velocities, 'r--', label='Fitted curve')
    plt.xlabel('Time')
    plt.ylabel('Average y-component of velocity')
    plt.title(f'Uy vs Time ({re_title})')
    plt.legend()

    # Adding the equation and parameters to the plot
    equation_text = f"Fit: A * exp(-b * t)\nA = {popt[0]:.3f}\nb = {popt[1]:.3f}"
    plt.text(0.95, 0.05, equation_text, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='bottom', horizontalalignment='right', bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    
    csv_file = "cases/" + sys.argv[1] + "e-6/U_vs_time.csv"
    output_file = "cases/" + sys.argv[1] + "e-6/Uy_vs_time.png"
    re_file = "cases/" + sys.argv[1] + "e-6/RE.txt"
    max_time = 200  # Set the maximum time to be plotted, or None to plot all data
    plot_y_velocity_from_csv(csv_file, output_file, re_file, max_time)
