# Simulation and Performance Evaluation
This is the repository of the Simulation and Performance Evaluation course offered in the Computer science degree.
In this repository you can find:
- The homework assigned, with the relative report and code
- The implemented project with all useful information about it.


## Project: Impact of Urban Environments on V2V Communication
This section contains the exact commands to run, to obtain the same results contained inside the final report.

### Prerequisites
To run this simulation, you must have the following installed:
- OMNeT++ (v5.6.2 or compatible)
- SUMO (Simulation of Urban MObility, v1.8.0 or compatible)
- Veins Framework (v5.1 or compatible)
- Python 3 (with `pandas`, `matplotlib`, `numpy` and `scipy`)

### Repository Structure
The `/Project` directory contains:
- Python analysis scripts (inside the `/script` folder);
- The OMNeT++ configuration files (inside the `/simulations` folder)
- The scalar (`.sca`) and vector (`.vec`) result files, along with the exported `.csv` files (inside the `/simulations/results` folder)

### 1. Generating Traffic
Traffic is generated stochastically to ensure statistical fairness across runs. \
We utilize SUMO's `randomTrips.py` script. Navigate to the `/simulations` folder and run:
```
python $SUMO_HOME/tools/randomTrips.py -n map.net.xml -r routes.rou.xml -e 100 -l
```

### 2. Running Simulations
The simulation is configured to run 5 independent replications for each scenario using different RNG seeds to calculate 95% Confidence Intervals.

To execute the runs from the command line:
```
./run_simulations.sh
```
_(Alternatively, open omnetpp.ini in the OMNeT++ IDE, select the desired Scenario, and run all repetitions)._

The defined scenarios are three:
- Free Space: idealized baseline vacuum;
- Two-Ray Ground: introduces asphalt reflection and multipath fading;
- Obstacle Shadowing: introduces physical building polygons.

### 3. Data Extraction and Plotting
Once the simulations complete, the scalar files must be parsed. The Python scripts automatically calculate the mean, Packet Delivery Ratio (PDR), and 95% Confidence Intervals across all 5 runs.

Execute the plotting script:
```
python script/plot.py
```

The script will output three graphs to the root directory:

+ V2V_PDR_Confidence.pdf (Packet Delivery Ratio with CI error bars)
+ MAC_Collisions.pdf
+ Channel_Busy_Time.pdf
