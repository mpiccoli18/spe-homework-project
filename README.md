# Simulation and Performance Evaluation
This is the repository of the Simulation and Performance Evaluation course offered in the Computer science degree.
In this repository you can find:
- The homework assigned, with the relative report and code
- The implemented project with all useful information about it.


## Project: Impact of Urban Environments on V2V Communication

**Author: Marco Piccoli**

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

```sh
python $SUMO_HOME/tools/randomTrips.py -n map.net.xml -r routes.rou.xml -e 100 -l
```

### 2. Running Simulations
The simulation is configured to run 10 independent replications for each scenario using different RNG seeds to calculate 95% Confidence Intervals (CI).

To execute the runs, open the OMNeT++ IDE, right-click on `○mnetpp.ini` and select:
- **Run As -> Run Configuration**
- Set the number of **Run(s)** to `0..9` to batch-execute all repetitions.

The defined scenarios are three:
- Free Space: idealized baseline vacuum;
- Two-Ray Ground: introduces asphalt reflection and multipath fading;
- Obstacle Shadowing: introduces physical building polygons.

### 3. Data Extraction and Plotting
Once the simulations complete, the `.sca` (scalar) files must be parsed. To do so, simply run:

```sh
python script/export.py
```

To look at what parameters the simulations have stored inside the _.csv_ files, simply run:

```sh
python script/variables.py
```

Instead, if you want to know how many cars were at most, simultaneously, inside the simulation simply run:

```sh
python script/maxVehicles.py
```

The plotting script automatically calculates the mean and 95% CI across all 10 runs for three different performance metrics:

```sh
python script/plot.py
```

The script will output, to the root directory, three `.pdf` files containing the graphs for each scenario:

+ V2V_PDR_Confidence.pdf (Packet Delivery Ratio with CI)
+ V2V_MAC_Backoffs.pdf (Channel congestion with CI)
+ V2V_SNIR_Drops.pdf (Packets drop due to interference with CI)
