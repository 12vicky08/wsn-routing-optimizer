#!/bin/bash
cd /Users/bhargavasrisai/ns-3.45
BIN=./build/scratch/ns3.45-wsn-comparative-sim-optimized
ON=/Users/bhargavasrisai/Downloads/Papers/data/final_sweep/base_dutyOn.csv
OFF=/Users/bhargavasrisai/Downloads/Papers/data/final_sweep/ablation_dutyOff.csv
LOG=/Users/bhargavasrisai/Downloads/Papers/data/final_sweep/run.log
for seed in 1 2 3 4 5 6 7 8 9 10; do
  for s in IAGAPC-Enhanced AGAPC EGATS-N RCGA-ABC DGA-M CGAPD; do
    echo "=== ON seed=$seed scheme=$s $(date) ===" >> $LOG
    $BIN --scheme=$s --numNodes=200 --dataRateKbps=250 --rngRun=$seed --dutyCycle=true --outputFile=$ON >> $LOG 2>&1
  done
done
echo "=== BASE_DONE $(date) ===" >> $LOG
for seed in 1 2 3 4 5 6 7 8 9 10; do
  for s in IAGAPC-Enhanced AGAPC EGATS-N RCGA-ABC DGA-M CGAPD; do
    echo "=== OFF seed=$seed scheme=$s $(date) ===" >> $LOG
    $BIN --scheme=$s --numNodes=200 --dataRateKbps=250 --rngRun=$seed --dutyCycle=false --outputFile=$OFF >> $LOG 2>&1
  done
done
echo "=== ALL_DONE $(date) ===" >> $LOG
