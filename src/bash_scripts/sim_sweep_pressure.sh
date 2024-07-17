#!/bin/bash
#10..45..5

#run openfoam-docker in the openfoam folder directory
kick_pressure_sci = 0
base_pressure_sci = 0

cd "cases"
mkdir -p "$base_pressure_sci"
cd ..
cp -R "SteadyState_base" "cases/$base_pressure_sci/SteadyState_$base_pressure_sci"
#mv "SteadyState_$n" "${n}e-6"
cd "cases/$base_pressure_sci/SteadyState_$base_pressure_sci"
cd 0
sed -i "s/replace_w_PD/$base_pressure_sci/" p
cd .. 
simpleFoam
array=($(ls -t ))
cd ..
cd ..
cd ..

cp -R "icoFoam_base" "cases/$base_pressure_sci/icoFoam_$base_pressure_sci"
cd "cases/$base_pressure_sci"
cp -f "SteadyState_$base_pressure_sci/${array[0]}/p" "icoFoam_$base_pressure_sci/0/p"
cp -f "SteadyState_$base_pressure_sci/${array[0]}/U" "icoFoam_$base_pressure_sci/0/U"
cd "icoFoam_$base_pressure_sci"
cd 0
sed -i "/jumpTable/d" p
sed -i "s/jump            uniform -.*/jumpTable       table ((0 -$base_pressure_sci) (25 -$base_pressure_sci) (25.5 -$kick_pressure_sci) (26 -$base_pressure_sci));/g;" p
cd ..
variable_t_icoFoam
cd ..
cd ..
cd ..

