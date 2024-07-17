#!/bin/bash

#to be run from python control script
kick_pressure_sci=REPLACE_THIS_WITH_KICK_PRESSURE_SCI
base_pressure_sci=REPLACE_THIS_WITH_BASE_PRESSURE_SCI

cd "data/pressure_sweep/cases"
mkdir -p "$base_pressure_sci"
cd ..
cp -R "steady_state_base" "cases/$base_pressure_sci/steady_state_$base_pressure_sci"
cd "cases/$base_pressure_sci/steady_state_$base_pressure_sci"
cd 0
sed -i "s/replace_w_PD/$base_pressure_sci/" p
cd .. 
simpleFoam
array=($(ls -t ))
cd ..
cd ..
cd ..

cp -R "icofoam_base" "cases/$base_pressure_sci/icofoam_$base_pressure_sci"
cd "cases/$base_pressure_sci"
cp -f "steady_state_$base_pressure_sci/${array[0]}/p" "icofoam_$base_pressure_sci/0/p"
cp -f "steady_state_$base_pressure_sci/${array[0]}/U" "icofoam_$base_pressure_sci/0/U"
cd "icofoam_$base_pressure_sci"
cd 0
sed -i "/jumpTable/d" p
sed -i "s/jump            uniform -.*/jumpTable       table ((0 -$base_pressure_sci) (25 -$base_pressure_sci) (25.5 -$kick_pressure_sci) (26 -$base_pressure_sci));/g;" p
cd ..
variable_t_icoFoam
cd ..
cd ..
cd ..
cd ..
cd ..
