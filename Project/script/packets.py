import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = {
    'Free Space': 'Project\\simulations\\results\\Scenario1_scalars.csv',
    'Two-Ray Ground': 'Project\\simulations\\results\\Scenario2_scalars.csv',
    'Urban Shadowing': 'Project\\simulations\\results\\Scenario3_scalars.csv'
}

scenarios = list(files.keys())
received_data = []
lost_data = []

print("Scanning authentic OMNeT++ CSVs for success vs. loss data...")

for name, filepath in files.items():
    try:
        df = pd.read_csv(filepath, low_memory=False)
        val_col = 'value' if 'value' in df.columns else 'attrvalue'
        
        # Get Successfully Received Messages
        rx = df[df['name'].str.contains('receivedWSMs', na=False)]
        total_rx = rx[val_col].astype(float).sum() if not rx.empty else 0
        received_data.append(total_rx)
        
        # Get Total Lost Packets
        lost = df[df['name'] == 'TotalLostPackets']
        total_lost = lost[val_col].astype(float).sum() if not lost.empty else 0
        lost_data.append(total_lost)
        
        print(f"✅ {name} -> Received: {int(total_rx)} | Lost: {int(total_lost)}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {filepath}.")
        received_data.append(0)
        lost_data.append(0)


# Set up the bar positioning
x = np.arange(len(scenarios))
width = 0.35 

fig, ax = plt.subplots(figsize=(10, 6))

# Draw the two sets of bars (Green for Success, Red for Loss)
bars1 = ax.bar(x - width/2, received_data, width, label='Successfully Received', color='#2ca02c', edgecolor='black', alpha=0.85)
bars2 = ax.bar(x + width/2, lost_data, width, label='Packets Lost/Dropped', color='#d62728', edgecolor='black', alpha=0.85)

ax.set_title('Impact of Urban Environment on V2V Reliability', fontsize=15, fontweight='bold', pad=15)
ax.set_ylabel('Total Number of Messages', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add the exact numbers on top of the bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', fontsize=10)

add_labels(bars1)
add_labels(bars2)

plt.tight_layout()
plt.savefig('Packets.pdf', dpi=300)
print("\n🎉 Master Graph saved as 'Packets.pdf'")
plt.show()