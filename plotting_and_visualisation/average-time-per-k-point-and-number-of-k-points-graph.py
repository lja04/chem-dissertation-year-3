import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_times(input_file, output_file):
    # Read the input CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Debug: Print column names
    print("Columns in input file:", df.columns.tolist())

    # Ensure numeric columns for time data
    df['Total Time (seconds)'] = pd.to_numeric(df['Total Time (seconds)'], errors='coerce')
    df['Total Time (minutes)'] = pd.to_numeric(df['Total Time (minutes)'], errors='coerce')
    df['Total Time (hours)'] = pd.to_numeric(df['Total Time (hours)'], errors='coerce')

    # Extract k-value from the 'Name' column
    df['K-Value'] = df['Name'].apply(lambda x: float(x.split('_')[-1]))  # Extract k-point value

    # Group by k-value and calculate average times across all crystals and polymorphs
    grouped = df.groupby('K-Value').agg({
        'Total Time (seconds)': 'mean',
        'Total Time (minutes)': 'mean',
        'Total Time (hours)': 'mean'
    }).reset_index()

    # Debug: Print grouped data
    print("Grouped data:\n", grouped)

    # Write the grouped data to a new CSV file
    grouped.to_csv(output_file, index=False)

    print(f"Average times saved to: {output_file}")
    return grouped

def calculate_average_k_points(k_points_file):
    # Read the number-of-sampled-k-points.csv file into a pandas DataFrame
    df = pd.read_csv(k_points_file)

    # Ensure numeric columns for k-points data
    df['K-Point'] = pd.to_numeric(df['K-Point'], errors='coerce')
    df['Number of Sampled Unique K-Points'] = pd.to_numeric(df['Number of Sampled Unique K-Points'], errors='coerce')

    # Group by k-point and calculate the average number of unique k-points
    grouped_k_points = df.groupby('K-Point').agg({
        'Number of Sampled Unique K-Points': 'mean'
    }).reset_index()

    # Debug: Print grouped k-points data
    print("Grouped k-points data:\n", grouped_k_points)

    return grouped_k_points

def plot_average_times(output_file, average_k_points):
    # Read the average times CSV file for plotting
    avg_times_df = pd.read_csv(output_file)

    # Merge average times with average unique k-points data on K-Value/K-Point
    merged_df = avg_times_df.merge(average_k_points, left_on='K-Value', right_on='K-Point')

    # Plot average times for each k-point on the primary y-axis
    fig, ax1 = plt.subplots(figsize=(12, 8))  # Increased figure size for better visibility

    color1 = 'blue'
    ax1.plot(
        merged_df['K-Value'], 
        merged_df['Total Time (seconds)'], 
        marker='o', linestyle='-', color=color1, label='Average Time (Seconds)'
    )
    
    ax1.set_xlabel('Target K-Point distance (Å⁻¹)')
    ax1.set_ylabel('Average Time (Seconds)', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Plot average number of unique k-points on the secondary y-axis
    ax2 = ax1.twinx()  # Create a second y-axis sharing the same x-axis

    color2 = 'red'
    ax2.plot(
        merged_df['K-Point'], 
        merged_df['Number of Sampled Unique K-Points'], 
        marker='o', linestyle='--', color=color2, label='Avg. Number of Unique K-Points'
    )
    
    ax2.set_ylabel('Avg. Number of Unique K-Points', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    # Add gridlines to improve readability
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Add title and adjust legends to avoid overlapping points
    fig.suptitle('Average Time and Number of Unique K-Points per K-Point')
    
    # Add legends for both y-axis plots, positioning them outside the plot area
    ax1.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95))
    ax2.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95))

    # Save the plot as a PNG file
    plot_path = os.path.join(os.path.dirname(output_file), 'average_times_and_k_points_per_k_point.png')
    plt.savefig(plot_path)
    
    plt.show()
    
    print(f"Plot saved to: {plot_path}")

def main():
    input_file = "time-and-number-of-k-points.csv"
    output_file = "average-times-per-k-point.csv"
    k_points_file = "number-of-sampled-k-points.csv"

    # Calculate average times and save to CSV
    avg_times_df = calculate_average_times(input_file, output_file)

    # Calculate average number of unique k-points per k-point value
    avg_k_points_df = calculate_average_k_points(k_points_file)

    # Plot both metrics on one graph
    plot_average_times(output_file, avg_k_points_df)

if __name__ == "__main__":
    main()
