import argparse
import subprocess
import sys
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Control script for parameter sweeps with periodic grooved system in OpenFOAM.")
    parser.add_argument('--pressure-sweep', help='To run a sweep of pressure kicks.', action='store_true')
    parser.add_argument('--base-pressures', type=str, help='Specifies base pressures. Provide either a list of values in scientific notation or an iteration "iterate: start, stop, step"')
    parser.add_argument('--kick-pressure', type=float, help='Specifies pressure of kick.')

    parser.add_argument('--groove-height-sweep', help='To run a sweep of groove heights.', action='store_true')
    parser.add_argument('--groove-heights', type=str, help='Specifies heights of grooves. Provide either a list of values in scientific notation or an iteration "start, stop, step"')

    parser.add_argument('--new-sweep', help="For when you want to start a new sweep.", action = 'store_true')

    args = parser.parse_args()

    for arg, value in vars(args).items():
        print(f"{arg}: {value}")

    response = input("Are these parameters correct? Enter Y to continue or N to quit: ").strip().lower()
    if response != 'y':
        print("Exiting the script.")
        sys.exit(0) 

    kick_pressure_value, base_pressures, groove_heights = run_groove_height_sweep(args.base_pressures, args.kick_pressure, args.groove_heights)
    print("kick_pressure_value : " + str(kick_pressure_value))
    print("base_pressures : ")
    print(base_pressures)
    for base_pressure in base_pressures:
        print(str(base_pressure))
    print("groove_heights: ")
    print(groove_heights)
    for groove_height in groove_heights:
         print(str(groove_height))

def run_pressure_sweep(base_pressures, kick_pressure):
        
        base_pressures = base_pressures.lower().split()

        if base_pressures[0].lower() == "iterate:":
            start = float(base_pressures[1])
            stop = float(base_pressures[2])
            step = float(base_pressures[3])
            base_pressures = [i for i in np.arange(start, stop, step)]
        else:
            base_pressures = [float(i) for i in base_pressures[1:]]
        
        return kick_pressure, base_pressures

def run_groove_height_sweep(base_pressures, kick_pressure, groove_heights):
        
        base_pressures = base_pressures.lower().split()
        groove_heights = groove_heights.lower().split()

        if base_pressures[0].lower() == "iterate:":
            start = float(base_pressures[1])
            stop = float(base_pressures[2])
            step = float(base_pressures[3])
            base_pressures = [i for i in np.arange(start, stop, step)]
        else:
            base_pressures = [float(i) for i in base_pressures[1:]]

        if groove_heights[0].lower() == "iterate:":
            start = float(groove_heights[1])
            stop = float(groove_heights[2])
            step = float(groove_heights[3])
            groove_heights = [i for i in np.arange(start, stop, step)]
        else:
            groove_heights = [float(i) for i in base_pressures[1:]]
        
        return kick_pressure, base_pressures, groove_heights
    

    


if __name__ == "__main__":
    main()
