#!/usr/bin/env bash

base_pressure_sci=2.3e-5
sweep_type="groove_height_sweep"
groove_height=1.1

pvbatch "src/processing_scripts/get_uprofile_outlet_grooves.py" "$base_pressure_sci" "$groove_height"
python3 "src/processing_scripts/RE_process.py" "data/$sweep_type/cases/$groove_height/$base_pressure_sci/uprofile_outlet.csv" "data/$sweep_type/cases/$groove_height/$base_pressure_sci/RE.txt" "$base_pressure_sci"    
python3 "src/processing_scripts/get_plot_over_time_grooves.py" "1520, 1521, 1522, 1565, 1566, 1567" "$base_pressure_sci" "$sweep_type" "$groove_height"
python3 "src/processing_scripts/get_Uy_vs_time_grooves.py" "$base_pressure_sci" "$sweep_type" "$groove_height"

# my mesh "1520, 1521, 1522, 1565, 1566, 1567"

#marc mesh "1685, 1686, 1687, 1730, 1731, 1732"