#!/usr/bin/env bash

for n in {5..75..5};
do 
    #pvbatch "get_uprofile_outlet.py" "${n}e-6"
    #python3 "RE_process.py" "cases/${n}e-6/uprofile_outlet.csv" "cases/${n}e-6/RE.txt" "${n}e-6"    
    python3 "get_plot_over_time.py" "496,497,498,499,526,527,528,529" "${n}"
    python3 "get_Uy_vs_time.py" "${n}"
done
