import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_time_per_unique_k_point(avg_times_file, avg_k_points_file, output_file):
    # Read the average times and average unique k-points data
    avg_times_df = pd.read_csv(avg_times_file)
    avg_k_points_df = pd.read_csv(avg_k_points_file)

    # Merge the two datasets on K-Value/K-Point
    merged_df = avg_times_df.merge(avg_k_points_df, left_on='K-Value', right_on='K-Point')

    # Calculate average time per unique k-point
    merged_df['Average Time per Unique K-Point (seconds)'] = (
        merged_df['Total Time (seconds)'] / merged_df['Number of Sampled Unique K-Points']
    )

    # Group by K-Value and calculate the mean of Average Time per Unique K-Point
    result = merged_df.groupby('K-Value').agg({
        'Average Time per Unique K-Point (seconds)': 'mean'
    }).reset_index()

    # Debug: Print grouped data with new column
    print("Grouped data with Average Time per Unique K-Point:\n", result)

    # Save the resulting data to a new CSV file
    result.to_csv(output_file, index=False)

    print(f"Average time per unique k-point saved to: {output_file}")
    return result

def plot_average_time_per_unique_k_point(data, output_plot_path):
    # Plot average time per unique k-point for each k-value
    plt.figure(figsize=(10, 6))

    plt.plot(
        data['K-Value'], 
        data['Average Time per Unique K-Point (seconds)'], 
        marker='o', linestyle='-', color='purple', label='Avg. Time per Unique K-Point'
    )

    plt.title('Average Time per Unique K-Point for Each K-Value')
    plt.xlabel('K-Value')
    plt.ylabel('Average Time per Unique K-Point (Seconds)')
    plt.grid(True)
    plt.legend()

    # Save the plot as a PNG file
    plt.savefig(output_plot_path)
    
    plt.show()
    
    print(f"Plot saved to: {output_plot_path}")

def main():
    avg_times_file = "average-times-per-k-point.csv"
    avg_k_points_file = "number-of-sampled-k-points.csv"
    output_file = "average-time-per-unique-k-point.csv"
    output_plot_path = "average_time_per_unique_k_point.png"

    # Calculate average time per unique k-point and save to CSV
    result = calculate_average_time_per_unique_k_point(avg_times_file, avg_k_points_file, output_file)

    # Plot the average time per unique k-point for each k-value
    plot_average_time_per_unique_k_point(result, output_plot_path)

if __name__ == "__main__":
    main()
