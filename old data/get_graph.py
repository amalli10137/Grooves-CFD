import matplotlib.pyplot as plt

# Sample data
subx = [0.55, 0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
y = [306.235, 302.325, 294.035, 292.194, 292.258, 295.495, 297.783, 300.074, 308.139, 306.882]

x = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

# Create a figure and axes
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, y, **{'marker': 'o'})

# Add labels and title
ax.set_xlabel('Normalized Groove Height (groove height / channel height)')
ax.set_ylabel('Critical Reynolds Number')
ax.set_title('Normalized Groove Height vs Critical Reynolds Number')

# Show the plot
plt.show()