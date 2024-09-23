#!/bin/bash

#to be run from python control script
kick_pressure_sci=1e-4
base_pressure_sci=2.3e-5
groove_height=4.0

cd "data/groove_height_sweep/cases/$groove_height"
mkdir -p "$base_pressure_sci"
cd ..
cd ..
cp -R "steady_state_base" "cases/$groove_height/$base_pressure_sci/steady_state_${groove_height}_$base_pressure_sci"
cd "cases/$groove_height/$base_pressure_sci/steady_state_${groove_height}_$base_pressure_sci"
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
cd ..

cp -R "icofoam_base" "cases/$groove_height/$base_pressure_sci/icofoam_${groove_height}_$base_pressure_sci"
cd "cases/$groove_height/$base_pressure_sci"
cp -f "steady_state_${groove_height}_$base_pressure_sci/${array[0]}/p" "icofoam_${groove_height}_$base_pressure_sci/0/p"
cp -f "steady_state_${groove_height}_$base_pressure_sci/${array[0]}/U" "icofoam_${groove_height}_$base_pressure_sci/0/U"
cd "icofoam_${groove_height}_$base_pressure_sci"
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
cd ..