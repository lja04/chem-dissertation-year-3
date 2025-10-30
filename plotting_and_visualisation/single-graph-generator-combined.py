import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Read the data from the CSV file
input_file = 'energy_summary.csv'
data = pd.read_csv(input_file)

# Create a directory for saving graphs if it doesn't exist
output_directory = 'single-energy-graphs'
os.makedirs(output_directory, exist_ok=True)

# Print unique crystal types for debugging
print("Unique Crystal Types:", data['Crystal Type'].unique())

# Create a 2x6 subplot figure
fig, axs = plt.subplots(6, 2, figsize=(20, 30))
# Remove the suptitle line
# fig.suptitle('Energy vs K-Point for Different Crystal Types', fontsize=16)

# Get unique base crystal types
base_crystal_types = sorted(set(ct.split('_')[0] for ct in data['Crystal Type'].unique()))

# Function to create a single subplot
def create_subplot(ax, crystal_data, crystal_type):
    # Ensure 'K-Point' is treated as a string and replace '-' with '.'
    crystal_data['K-Point'] = crystal_data['K-Point'].astype(str).str.replace('-', '.', regex=False)
    
    # Convert to numeric, coercing errors to NaN
    crystal_data['K-Point'] = pd.to_numeric(crystal_data['K-Point'], errors='coerce')

    # Drop rows with NaN values in 'K-Point' after conversion
    crystal_data = crystal_data.dropna(subset=['K-Point'])

    # Sort by k-point
    crystal_data = crystal_data.sort_values(by='K-Point')

    # Prepare k-points and energy values for plotting
    k_points = crystal_data['K-Point']
    energy_no_debye = crystal_data['Energy without Debye or KDE']
    energy_debye = crystal_data['Energy with only Debye']
    energy_debye_kde = crystal_data['Energy with Debye and KDE']

    # Create the plot
    ax.plot(k_points, energy_no_debye, marker='o', label='No Debye or KDE')
    ax.plot(k_points, energy_debye, marker='s', label='Only Debye')
    ax.plot(k_points, energy_debye_kde, marker='^', label='Debye and KDE')

    # Customize the plot
    ax.set_title(crystal_type.upper())
    ax.set_xlabel('Target K-Point distance (Å⁻¹)')
    ax.set_ylabel('Energy (kJ/mol)')
    ax.legend()
    ax.grid(True)
    
    # Flip the x-axis
    ax.invert_xaxis()

    # Print debug information
    print(f"Plotted {crystal_type} with {len(k_points)} data points")

# Loop through each unique base crystal type
for i, base_crystal in enumerate(base_crystal_types):
    crystal_variants = [ct for ct in data['Crystal Type'].unique() if ct.startswith(base_crystal)]
    
    for j, variant in enumerate(crystal_variants[:2]):  # Limit to 2 variants per base crystal
        crystal_data = data[data['Crystal Type'] == variant]
        
        if not crystal_data.empty:
            create_subplot(axs[i, j], crystal_data, variant)
        else:
            axs[i, j].axis('off')  # Turn off the subplot if no data
            print(f"No data for {variant}")
    
    # Turn off any unused subplots in the row
    for j in range(len(crystal_variants), 2):
        axs[i, j].axis('off')

# Adjust the layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the combined plot
output_filename = f"{output_directory}/combined_plot.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()

print(f"Combined plot has been created and saved as '{output_filename}'.")

# Verify the file was created and has content
if os.path.exists(output_filename):
    file_size = os.path.getsize(output_filename)
    print(f"File created successfully. Size: {file_size} bytes")
else:
    print("File was not created successfully.")
