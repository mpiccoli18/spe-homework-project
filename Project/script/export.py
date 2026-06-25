import os

# Mapping the .sca file prefixes to the expected CSV names in plot_results.py
scenarios = {
    'Scenario1': 'Scenario1_FreeSpace',
    'Scenario2': 'Scenario2_TwoRayGround',
    'Scenario3': 'Scenario3_ObstacleShadowing'
}

# The folder where the results are located
results_dir = 'results' 

# Fallback just in case you are running this from outside the project directory
if not os.path.exists(results_dir):
    results_dir = os.path.join('Project', 'simulations', 'results')

print("Starting batch conversion of .sca files to .csv...")

for sca_prefix, csv_prefix in scenarios.items():
    for i in range(10):
        # OMNeT++ saves as: Scenario1-#0.sca
        sca_filename = f"{sca_prefix}-#{i}.sca"
        # plot_results.py expects: Scenario1_FreeSpace-#0.csv
        csv_filename = f"{csv_prefix}-#{i}.csv"
        
        sca_filepath = os.path.join(results_dir, sca_filename)
        csv_filepath = os.path.join(results_dir, csv_filename)
        
        if not os.path.exists(sca_filepath):
            print(f"Warning: Could not find {sca_filepath}.")
            continue
        
        with open(sca_filepath, 'r') as f:
            lines = f.readlines()
            
        # Find the official OMNeT++ Run ID
        run_name = "Unknown"
        for line in lines:
            if line.startswith('run '):
                run_name = line.strip().split(' ')[1]
                break

        # Reconstruct the exact opp_scavetool CSV format
        csv_lines = ["run,type,module,name,attrname,attrvalue,value"]
        for line in lines:
            if line.startswith('scalar'):
                parts = line.strip().split()
                if len(parts) >= 4:
                    module = parts[1]
                    metric = parts[2]
                    value = parts[3]
                    # Format: run, type, module, name, attrname, attrvalue, value
                    csv_lines.append(f"{run_name},scalar,{module},{metric},,,{value}")
                    
        # Save the authentic CSV file
        with open(csv_filepath, 'w') as f:
            f.write("\n".join(csv_lines) + "\n")
            
        print(f"✅ Successfully generated {csv_filename} ({len(csv_lines)-1} data rows recorded).")

print("\nAll files converted! You can now run plot_results.py")