import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load data
file_path = "observed-structures-from-csvs.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Calculate correlation statistics
corr_coef, p_value = stats.pearsonr(df['density'], df['free energy'])
slope, intercept, r_value, p_value, std_err = stats.linregress(df['density'], df['free energy'])

# Create plot
plt.figure(figsize=(12, 6))
ax = sns.scatterplot(data=df, 
                    x='density', 
                    y='free energy',
                    hue='id',
                    palette='viridis',
                    s=100,
                    alpha=0.8,
                    legend=False)

# Add regression line
x_values = np.linspace(df['density'].min(), df['density'].max(), 100)
y_values = intercept + slope * x_values
plt.plot(x_values, y_values, color='red', linestyle='--', linewidth=2)

# Add correlation stats to plot
stats_text = (f"Pearson r = {corr_coef:.3f}\n"
             f"p-value = {p_value:.3e}\n"
             f"R² = {r_value**2:.3f}\n"
             f"Slope = {slope:.3f} kJ/mol·(g/cm³)⁻¹")
plt.text(0.05, 0.95, stats_text, 
        transform=ax.transAxes,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8))

plt.xlabel('Density (g/cm³)', fontsize=12)
plt.ylabel('Vibrational Free Energy (kJ/mol)', fontsize=12)
plt.title('Density vs. Vibrational Free Energy with Correlation Statistics', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save and show
plt.savefig('density_vs_free_energy_with_stats.png', dpi=300, bbox_inches='tight')
plt.show()

# Print additional statistics to console
print("\nAdditional Statistics:")
print("---------------------")
print(f"Mean density: {df['density'].mean():.3f} ± {df['density'].std():.3f} g/cm³")
print(f"Mean free energy: {df['free energy'].mean():.3f} ± {df['free energy'].std():.3f} kJ/mol")
print(f"Number of data points: {len(df)}")
print(f"Linear regression equation: y = {slope:.3f}x + {intercept:.3f}")