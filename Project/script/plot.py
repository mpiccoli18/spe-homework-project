import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import os

# Define the scenarios and the expected CSV files for all 10 runs
scenarios = {
    'Free Space': 'Scenario1_FreeSpace',
    'Two-Ray Ground': 'Scenario2_TwoRayGround',
    'Urban Shadowing': 'Scenario3_ObstacleShadowing',
    'Half Simulation': 'Scenario4_HalfSimulation',
    'Straight Road': 'Scenario5_StraightRoad'
}

# Data dictionaries to hold our metrics across all 10 runs
data = {
    'PDR': {name: [] for name in scenarios},
    'MAC_Backoff': {name: [] for name in scenarios},
    'SNIR_Drops': {name: [] for name in scenarios}
}

# Helper function to calculate 95% Confidence Interval
def calculate_confidence_interval(data_list, confidence=0.95):
    n = len(data_list)
    if n < 2:
        return np.mean(data_list) if n == 1 else 0, 0
    mean = np.mean(data_list)
    sem = st.sem(data_list)
    margin = sem * st.t.ppf((1 + confidence) / 2., n-1)
    return mean, margin

print("Extracting data and calculating 95% Confidence Intervals...")

for name, prefix in scenarios.items():
    for i in range(10):
        filepath = f'./Project/simulations/results/{prefix}-#{i}.csv' 
        try:
            df = pd.read_csv(filepath, low_memory=False)
            val_col = 'value' if 'value' in df.columns else 'attrvalue'
            if val_col not in df.columns: continue
            
            # Helper to extract the sum of a specific variable safely
            def extract_sum(metric_name):
                rows = df[df['name'] == metric_name]
                if rows.empty: # Fallback to partial match
                    rows = df[df['name'].str.contains(metric_name, case=False, na=False)]
                return rows[val_col].astype(float).sum() if not rows.empty else 0

            # PDR Calculation (Broadcast Formula)
            # Check for BOTH WSMs (Wave Short Messages) and BSMs (Basic Safety Messages)
            rx = extract_sum('receivedWSMs') + extract_sum('receivedBSMs')
            tx = extract_sum('generatedWSMs') + extract_sum('generatedBSMs')
            if tx == 0:  
                tx = extract_sum('sentPackets')

            if 'Half Simulation' in name or 'HalfTraffic' in prefix:
                total_expected = tx * 49  # Only 50 cars max in the half simulation
            else:
                total_expected = tx * 99  # 100 cars in standard simulations
                
            pdr = (rx / total_expected) * 100 if total_expected > 0 else 0
            
            # MAC Backoff Calculation (Channel Congestion)
            mac_backoff = extract_sum('TimesIntoBackoff')
            
            # SNIR Drops Calculation
            snir_drops = extract_sum('SNIRLostPackets')

            # Append to our data dictionaries
            data['PDR'][name].append(pdr)
            data['MAC_Backoff'][name].append(mac_backoff)
            data['SNIR_Drops'][name].append(snir_drops)
            
        except FileNotFoundError:
            print(f"  [Warning] File {filepath} not found. Skipping run {i}.")

# Plotting 
def plot_metric(metric_key, title, ylabel, filename, color_palette, is_percentage=False):
    means = []
    cis = []
    labels = list(scenarios.keys())

    for name in labels:
        m, c = calculate_confidence_interval(data[metric_key][name])
        means.append(m)
        cis.append(c)

    plt.figure(figsize=(9, 6))
    bars = plt.bar(labels, means, yerr=cis, capsize=10, 
                   color=color_palette, edgecolor='black', alpha=0.8)

    plt.title(title, fontsize=14, fontweight='bold', pad=15)
    plt.ylabel(ylabel, fontsize=12, fontweight='bold')
    
    if is_percentage:
        plt.ylim(0, 110)
    else:
        # Dynamically scale the y-axis to fit the error bars comfortably
        plt.ylim(0, max([m + c for m, c in zip(means, cis)]) * 1.2)
        
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add text labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        offset = plt.gca().get_ylim()[1] * 0.02
        text_format = f'{yval:.1f}%' if is_percentage else f'{int(yval)}'
        plt.text(bar.get_x() + bar.get_width()/2, yval + offset, 
                 text_format, ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"✅ Graph saved: {filename}")
    plt.close()

print("\nGenerating Graphs...")
# Plot 1: PDR
plot_metric('PDR', 'V2V Packet Delivery Ratio (PDR) with 95% CI', 'Delivery Success Rate (%)', 
            'V2V_PDR_Confidence.pdf', ['#2ca02c', '#ff7f0e', '#d62728'], is_percentage=True)

# Plot 2: Channel Congestion
plot_metric('MAC_Backoff', 'MAC Layer: Channel Congestion with 95% CI', 'Number of Backoffs', 
            'V2V_MAC_Backoffs.pdf', ['#1f77b4', '#aec7e8', '#ffbb78'])

# Plot 3: SNIR Drops
plot_metric('SNIR_Drops', 'Packets Dropped due to Interference with 95% CI', 'Dropped Packets', 
            'V2V_SNIR_Drops.pdf', ['#9467bd', '#c5b0d5', '#8c564b'])

print("\nDone! All three graphs are ready for your report.")