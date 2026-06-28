import pandas as pd
import os

filepath = './Project/simulations/results/Scenario4_HalfSimulation-#0.csv'

if not os.path.exists(filepath):
    print(f"Error: Could not find {filepath}. Make sure you are in the project root.")
else:
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
    peak_time = 0
    
    # Walk through the timeline to find the peak
    for time, change in events:
        current_cars += change
        if current_cars > max_cars:
            max_cars = current_cars
            peak_time = time
            
    print(f"Total unique vehicles spawned over 100s: {len(starts)}")
    print(f"Maximum CONCURRENT vehicles on the map: {max_cars} cars")
    print(f"This peak traffic occurred at exactly {peak_time:.2f} seconds into the simulation.")