#!/bin/bash

# Make sure the script stops if any error occurs
set -e

EXECUTABLE="../src/Omnet"

echo "Scanning for NED folders and Libraries..."
NED_PATH="."
VEINS_LIB=""

for DIR in "../src" "../../src"; do
    if [ -d "$DIR" ]; then
        NED_PATH="$NED_PATH:$DIR"
        echo " -> Found valid project NED folder: $DIR"
    fi
done

for DIR in "../veins/src" "../../veins/src" "../../../veins/src" "veins/src"; do
    if [ -f "$DIR/libveins.so" ] || [ -f "$DIR/libveins.dylib" ] || [ -f "$DIR/veins.dll" ] || [ -f "$DIR/libveins.a" ]; then
        VEINS_LIB="-l $DIR/veins"
        echo " -> Found compiled Veins library at: $DIR"
        break
    fi
done

if [ -z "$VEINS_LIB" ]; then
    echo " -> Warning: Could not automatically find the compiled Veins library."
    echo " -> If the simulation fails, please use the OMNeT++ IDE '0..9' Run Number method!"
fi

echo "Starting automated simulations..."

echo "======================================================"
echo "Running Scenario 1: Free Space (10 repetitions)..."
$EXECUTABLE -u Cmdenv $VEINS_LIB -n "$NED_PATH" -c Scenario1 omnetpp.ini

echo "======================================================"
echo "Running Scenario 2: Two-Ray Ground (10 repetitions)..."
$EXECUTABLE -u Cmdenv $VEINS_LIB -n "$NED_PATH" -c Scenario2 omnetpp.ini

echo "======================================================"
echo "Running Scenario 3: Obstacle Shadowing (10 repetitions)..."
$EXECUTABLE -u Cmdenv $VEINS_LIB -n "$NED_PATH" -c Scenario3 omnetpp.ini

echo "======================================================"
echo "All 30 simulation runs completed successfully!"
