import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the CSV file
df = pd.read_csv('combined_timing_data.csv')

# Extract crystal name, crystal ID, k-value, and ld number
df['crystal'] = df['crystal name'].apply(lambda x: '_'.join(x.split('_')[:2]))
df['k_value'] = df['crystal name'].apply(lambda x: float(x.split('k-value-')[1].split('_')[0]))
df['ld'] = df['crystal name'].apply(lambda x: int(x.split('ld-')[1]))

# Calculate average total run time for each crystal and k-value
avg_times = df.groupby(['crystal', 'k_value'])['total run time'].mean().reset_index()

# Get unique crystal types (including IDs)
crystal_types = avg_times['crystal'].unique()

# Create a plot for each crystal type
output_dir = "average-time-per-k-points-plots"
os.makedirs(output_dir, exist_ok=True)

for crystal in crystal_types:
    # Filter data for the current crystal type
    crystal_data = avg_times[avg_times['crystal'] == crystal]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(crystal_data['k_value'], crystal_data['total run time'], marker='o')
    
    # Set axis labels
    plt.xlabel('K-point Value')
    plt.ylabel('Average Total Run Time (s)')
    
    # Invert the x-axis so it goes from 0.40 to 0.10
    plt.gca().invert_xaxis()
    
    # Add grid for better readability
    plt.grid(True)
    
    # Save the plot to the specified directory
    plot_filename = f'{crystal}_avg_time_vs_kpoint.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    
    # Close the plot to free memory
    plt.close()

print("Plots have been generated and saved.")
