#!/bin/bash

#to be run from python control script
kick_pressure_sci=1e-4
base_pressure_sci=22e-6
#groove_height=3

for groove_height in 1.7 1.8 1.9 2 2.1
do
    cd "data/groove_height_sweep/cases"
    mkdir -p "$groove_height"
    cd ..
    cp -R "steady_state_base" "cases/$groove_height/steady_state_$groove_height"
    cd "cases/$groove_height/steady_state_$groove_height"
    cd 0
    sed -i "s/replace_w_PD/$base_pressure_sci/" p
    cd .. 
    cd system
    sed -i "s/replace_w_height/$groove_height/" blockMeshDict
    cd ..
    blockMesh
    simpleFoam
    array=($(ls -t ))
    cd ..
    cd ..
    cd ..

    cp -R "icofoam_base" "cases/$groove_height/icofoam_$groove_height"
    cd "cases/$groove_height"
    cp -f "steady_state_$groove_height/${array[0]}/p" "icofoam_$groove_height/0/p"
    cp -f "steady_state_$groove_height/${array[0]}/U" "icofoam_$groove_height/0/U"
    cd "icofoam_$groove_height"
    cd 0
    sed -i "/jumpTable/d" p
    sed -i "s/jump            uniform -.*/jumpTable       table ((0 -$base_pressure_sci) (25 -$base_pressure_sci) (25.5 -$kick_pressure_sci) (26 -$base_pressure_sci));/g;" p
    cd ..
    cd system
    sed -i "s/replace_w_height/$groove_height/" blockMeshDict
    cd ..
    blockMesh
    variable_t_icoFoam
    cd ..
    cd ..
    cd ..
    cd ..
    cd ..
done