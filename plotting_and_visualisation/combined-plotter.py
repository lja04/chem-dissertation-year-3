import pandas as pd
import matplotlib.pyplot as plt
import os  # Import the os module

# Read the CSV file
df = pd.read_csv('combined_timing_data.csv')

# Extract k-value and total run time
df['k_value'] = df['crystal name'].apply(lambda x: float(x.split('k-value-')[1].split('_')[0]))
df['total_run_time'] = df['total run time']

# Calculate average total run time for each k-value
avg_times = df.groupby('k_value')['total_run_time'].mean().reset_index()

# Sort k-values in descending order
avg_times = avg_times.sort_values('k_value', ascending=False)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(avg_times['k_value'], avg_times['total_run_time'], marker='o')

# Set axis labels
plt.xlabel(r'K-point Value ($\mathrm{\AA}^{-1}$)')
plt.ylabel('Average Total Run Time (s)')

# Invert the x-axis
plt.gca().invert_xaxis()

# Add grid for better readability
plt.grid(True)

# Save the plot
output_dir = "average-time-per-k-points-plots"
os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
plot_filename = "overall_avg_time_vs_kpoint.png"
plot_path = os.path.join(output_dir, plot_filename)
plt.savefig(plot_path)

plt.close()

print("Overall average time plot has been generated and saved.")
