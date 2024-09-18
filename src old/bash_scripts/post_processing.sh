#!/usr/bin/env bash

base_pressure_sci=2.45e-5
sweep_type="pressure_sweep"

pvbatch "src/processing_scripts/get_uprofile_outlet.py" "$base_pressure_sci" "$sweep_type"
python3 "src/processing_scripts/RE_process.py" "data/$sweep_type/cases/$base_pressure_sci/uprofile_outlet.csv" "data/$sweep_type/cases/$base_pressure_sci/RE.txt" "$base_pressure_sci"    
python3 "src/processing_scripts/get_plot_over_time.py" "1685, 1686, 1687, 1730, 1731, 1732" "$base_pressure_sci" "$sweep_type"
python3 "src/processing_scripts/get_Uy_vs_time.py" "$base_pressure_sci" "$sweep_type"

