import pandas as pd


file = "Project\\simulations\\results\\Scenario3_ObstacleShadowing-#0.csv"  

print(f"Scanning {file} for variable names...\n")

df = pd.read_csv(file, low_memory=False)

unique_names = sorted(df['name'].dropna().unique())

print("--- EXACT VARIABLE NAMES FOUND IN THIS FILE ---")
for name in unique_names:
    print(f"'{name}'")