import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the data from the CSV file
input_file = 'energy_summary.csv'
data = pd.read_csv(input_file)

# Create a directory for saving graphs if it doesn't exist
output_directory = 'single-energy-graph'
os.makedirs(output_directory, exist_ok=True)

# Loop through each unique crystal type and species
for crystal_type in data['Crystal Type'].unique():
    # Filter data for the current crystal type
    crystal_data = data[data['Crystal Type'] == crystal_type]
    
    # Ensure 'K-Point' is treated as a string and replace '-' with '.'
    crystal_data['K-Point'] = crystal_data['K-Point'].astype(str).str.replace('-', '.', regex=False)
    
    # Convert to numeric, coercing errors to NaN (if there are any invalid entries)
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
    plt.figure(figsize=(10, 6))
    
    plt.plot(k_points, energy_no_debye, marker='o', label='No Debye or KDE')
    plt.plot(k_points, energy_debye, marker='s', label='Only Debye')
    plt.plot(k_points, energy_debye_kde, marker='^', label='Debye and KDE')

    # Customize the plot
    plt.title(crystal_type.replace('_', ' ').upper())
    plt.xlabel('Target K-Point distance (Å⁻¹)')
    plt.ylabel('Energy (kJ/mol)')
    plt.legend()
    plt.grid(True)
    
    # Flip the x-axis
    plt.gca().invert_xaxis()
    
    # Save the figure with an appropriate name
    output_filename = f"{output_directory}/{crystal_type}_energies_graph.png"
    plt.savefig(output_filename)
    
    # Close the plot to free memory
    plt.close()

print(f"Graphs have been created and saved in the '{output_directory}' directory.")
