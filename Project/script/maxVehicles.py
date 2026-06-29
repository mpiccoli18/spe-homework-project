import pandas as pd
import os
import matplotlib.pyplot as plt

# Define all the scenarios we want to analyze
scenarios = [
    'Scenario1_FreeSpace',
    'Scenario2_TwoRayGround',
    'Scenario3_ObstacleShadowing',
    'Scenario4_HalfSimulation',
    'Scenario5_StraightRoad'
]

# Locate the results directory
results_dir = 'results'
if not os.path.exists(results_dir):
    results_dir = os.path.join('Project', 'simulations', 'results')

print("Computing Mean Maximum Concurrent Vehicles across 10 runs...\n")
print("=" * 60)

# Lists to store data for the final plot
plot_labels = []
plot_means = []

# Clean display names for the graph's X-axis
display_names = {
    'Scenario1_FreeSpace': 'Free Space',
    'Scenario2_TwoRayGround': 'Two-Ray Ground',
    'Scenario3_ObstacleShadowing': 'Urban Shadowing',
    'Scenario4_HalfSimulation': 'Half Traffic',
    'Scenario5_StraightRoad': 'Straight Road'
}

for scenario in scenarios:
    max_cars_all_runs = []
    
    # Iterate through all 10 runs
    for i in range(10):
        filepath = os.path.join(results_dir, f"{scenario}-#{i}.csv")
        
        if not os.path.exists(filepath):
            continue # Skip if the file doesn't exist yet
            
        df = pd.read_csv(filepath, low_memory=False)
        val_col = 'value' if 'value' in df.columns else 'attrvalue'
        
        # Extract all start and stop times
        starts = df[df['name'] == 'startTime'][val_col].astype(float).tolist()
        stops = df[df['name'] == 'stopTime'][val_col].astype(float).tolist()
        
        # Create a timeline of events: +1 for entering the map, -1 for leaving
        events = [(t, 1) for t in starts] + [(t, -1) for t in stops]
        
        # Sort the timeline chronologically
        events.sort(key=lambda x: x[0])
        
        current_cars = 0
        max_cars = 0
        
        # Walk through the timeline to find the peak for THIS specific run
        for time, change in events:
            current_cars += change
            if current_cars > max_cars:
                max_cars = current_cars
                
        max_cars_all_runs.append(max_cars)
        
    # Calculate and print the statistics for the scenario
    if max_cars_all_runs:
        runs_found = len(max_cars_all_runs)
        mean_max = sum(max_cars_all_runs) / runs_found
        min_max = min(max_cars_all_runs)
        max_max = max(max_cars_all_runs)
        
        print(f"Scenario: {scenario} (Processed {runs_found}/10 runs)")
        print(f" -> Mean Max Concurrent Vehicles: {mean_max:.1f} cars")
        print(f" -> (Absolute Min: {min_max}, Absolute Max: {max_max})")
        print("-" * 60)
        
        # Save the scenario name and calculated mean for plotting
        plot_labels.append(display_names.get(scenario, scenario))
        plot_means.append(mean_max)
    else:
        print(f"Scenario: {scenario}")
        print(" -> No CSV files found for this scenario.")
        print("-" * 60)

# Generate Bar Graph
if plot_labels:
    print("\nGenerating bar graph...")
    plt.figure(figsize=(10, 6))
    
    # Define a distinct color for each of the 5 scenarios
    bar_colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']

    # Create the bar chart
    bars = plt.bar(plot_labels, plot_means, color=bar_colors[:len(plot_labels)], edgecolor='black', alpha=0.8)
    
    # Add title and labels
    plt.title('Mean Maximum Concurrent Vehicles Across 10 Runs', fontsize=14, fontweight='bold')
    plt.ylabel('Mean Concurrent Vehicles', fontsize=12, fontweight='bold')
    
    # Add a subtle grid for easier reading
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(fontsize=11)
    
    # Add the exact numbers on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 f'{height:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
                 
    plt.tight_layout()
    
    # Save the graph to a PDF file alongside the other project graphs
    output_filename = "V2V_MaxVehicles.pdf"
    plt.savefig(output_filename, format='pdf', bbox_inches='tight')
    print(f"✅ Bar graph successfully saved as '{output_filename}'!")