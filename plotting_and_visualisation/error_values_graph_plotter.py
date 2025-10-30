import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('k_point_error_statistics.csv')

# Filter out the row where k-value is 0.1
filtered_df = df[df['k-value'] != 0.1]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['k-value'], filtered_df['mean absolute error'], marker='o', label='Mean Absolute Error')
plt.plot(filtered_df['k-value'], filtered_df['mean signed error'], marker='s', label='Mean Signed Error')
plt.plot(filtered_df['k-value'], filtered_df['max absolute error'], marker='^', label='Max Absolute Error')

plt.xlabel('K-Point (Å)')
plt.ylabel('Error Value')
plt.legend()
plt.grid(True)

plt.savefig('error_vs_kpoint.png')
plt.show()
