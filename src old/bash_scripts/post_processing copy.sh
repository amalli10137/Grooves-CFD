#!/usr/bin/env bash

base_pressure_sci=245e-7
sweep_type="groove_height_sweep"

for base_pressure_sci in 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.68 2 2.1
do

    pvbatch "src/processing_scripts/get_uprofile_outlet.py" "$base_pressure_sci" "$sweep_type"
    python3 "src/processing_scripts/RE_process.py" "data/$sweep_type/cases/$base_pressure_sci/uprofile_outlet.csv" "data/$sweep_type/cases/$base_pressure_sci/RE.txt" "$base_pressure_sci"    
    python3 "src/processing_scripts/get_plot_over_time.py" "1520, 1521, 1522, 1565, 1566, 1567" "$base_pressure_sci" "$sweep_type"
    python3 "src/processing_scripts/get_Uy_vs_time.py" "$base_pressure_sci" "$sweep_type"
done

python3 'src/processing_scripts/get_grid_plots.py' "data/groove_height_sweep/cases"
python3 'src/processing_scripts/height_vs_decay.py' "data/groove_height_sweep/cases"
