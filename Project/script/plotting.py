import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# This files takes as input the results of the whole simulation
# and plots the results for each of the scenario.
# The resulting plots are saved inside the repository 

scenario = 'Project\\simulations\\results\\Scenario1.csv'

print(f"Loading scenario from {scenario}")

readScenario = pd.read_csv(scenario, low_memory=False)

print("\n--- ALL RECORDED VECTORS ---")
all_vectors = readScenario['name'].dropna().unique()

for v in all_vectors:
    print(v)

print("\n Searching for Power Vectors...\n")

powerVectors = readScenario[readScenario['name'].str.contains('Power', na=False, case=False)]['name'].unique()
print(f"Found {len(powerVectors)} Power Vectors: {powerVectors}")
metric = "rxPower:vector"
car = "node[0]"

print(f"\n Filtering for {metric} of {car}...\n")

filteredData = readScenario[(readScenario['name'] == metric) & (readScenario['module'].str.contains(car, na=False))]

if filteredData.empty:
    print("No data found for the specified metric and car.")
else:
    row = filteredData.iloc[0]
    time = str(row['vectime'])
    value = str(row['vecvalue'])

    times = np.array([float(t) for t in time.split()])
    values = np.array([float(v) for v in value.split()])

    print(f"Success! Extracted {len(times)} data points. Drawing graph...")

    plt.figure(figsize=(10, 6))
    plt.plot(times, values, label=f'{car} Received Power', color='#2ca02c', alpha=0.8)

    plt.title('Received Signal Power Over Time (Scenario 1)', fontsize=14, fontweight='bold')
    plt.xlabel('Simulation Time (seconds)', fontsize=12)
    plt.ylabel('Received Power (dBm)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('Scenario1.pdf', dpi=300)
    plt.show()