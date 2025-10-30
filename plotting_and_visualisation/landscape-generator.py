import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('structures.csv')  # Replace with your CSV path

# Create figure
plt.figure(figsize=(10, 6))

# Plot all points in blue
plt.scatter(df['density'], df['energy'], 
            c='blue', alpha=1, edgecolors='w', linewidth=0.5,
            label='Predicted structures')

# Highlight observed crystal in red
observed = df[df['id'] == 'gocwea-QR-7-3342-3']
plt.scatter(observed['density'], observed['energy'], 
            c='red', s=100, edgecolors='k', linewidth=1,
            label='Observed structure (gocwea-QR-7-3342-3)')

# Label axes and add title
plt.xlabel('Density (g/cm³)', fontsize=12)
plt.ylabel('Lattice Energy (kJ/mol)', fontsize=12)

# Add legend and grid
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

# Save high-resolution figure
plt.savefig('csp_energy_vs_density.png', dpi=300, bbox_inches='tight')
plt.show()