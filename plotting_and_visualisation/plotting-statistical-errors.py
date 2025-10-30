import matplotlib.pyplot as plt
import pandas as pd

# File path to the CSV file
file_path = "k_point_error_statistics.csv"

# Load the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)

# Extract data for plotting
k_points = data['K-Point']
mean_signed_error = data['Mean Signed Error']
mean_absolute_error = data['Mean Absolute Error']
max_absolute_error = data['Max Absolute Error']

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each statistical value against k-points
plt.plot(k_points, mean_signed_error, marker='o', label='Mean Signed Error', color='blue')
plt.plot(k_points, mean_absolute_error, marker='o', label='Mean Absolute Error', color='green')
plt.plot(k_points, max_absolute_error, marker='o', label='Max Absolute Error', color='red')

# Add labels, title, and legend
plt.xlabel('Target K-Point distance (Å⁻¹)')
plt.ylabel('Error Value')
plt.title('Statistical Analysis of Errors at Each K-Point')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
output_plot_path = "error_statistics_plot.png"
plt.savefig(output_plot_path)

# Show the plot (optional)
plt.show()

print(f"Plot saved to: {output_plot_path}")
