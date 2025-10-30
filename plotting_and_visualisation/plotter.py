import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the timing data CSV file
df_timing = pd.read_csv('combined_timing_data.csv')

# Read the energy data CSV file
df_energy = pd.read_csv('combined-raw-energy-data.csv')

# Extract k-value and total run time from timing data
df_timing['k_value'] = df_timing['crystal name'].apply(lambda x: float(x.split('k-value-')[1].split('_')[0]))
df_timing['total_run_time'] = df_timing['total run time']

# Calculate average total run time for each k-value
avg_times = df_timing.groupby('k_value')['total_run_time'].mean().reset_index()

# Calculate average number of unique k-points for each k-value
avg_unique_kpoints = df_energy.groupby('k_point')['Total number of sampled unique k-points'].mean().reset_index()

# Sort k-values in descending order
avg_times = avg_times.sort_values('k_value', ascending=False)
avg_unique_kpoints = avg_unique_kpoints.sort_values('k_point', ascending=False)

# Create the plot with two y-axes
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# Plot average run time
line1 = ax1.plot(avg_times['k_value'], avg_times['total_run_time'], marker='o', color='blue', label='Avg Run Time')
ax1.set_xlabel(r'K-point Value ($\mathrm{\AA}^{-1}$)')
ax1.set_ylabel('Average Total Run Time (s)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Plot average number of unique k-points
line2 = ax2.plot(avg_unique_kpoints['k_point'], avg_unique_kpoints['Total number of sampled unique k-points'], marker='s', color='red', label='Avg Unique K-points')
ax2.set_ylabel('Average Number of Unique K-points', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Invert the x-axis
plt.gca().invert_xaxis()

# Add grid for better readability
ax1.grid(True)

# Add legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# Save the plot
output_dir = "average-time-per-k-points-plots"
os.makedirs(output_dir, exist_ok=True)
plot_filename = "overall_avg_time_and_kpoints_vs_kpoint.png"
plot_path = os.path.join(output_dir, plot_filename)
plt.savefig(plot_path)

plt.close()

print("Overall average time and unique k-points plot has been generated and saved.")
