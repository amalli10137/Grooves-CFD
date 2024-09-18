import argparse
import subprocess
import sys
import numpy as np
import pexpect
import os
from decimal import Decimal, getcontext, ROUND_HALF_UP


def main():
    parser = argparse.ArgumentParser(description="Control script for parameter sweeps with periodic grooved system in OpenFOAM.")
    parser.add_argument('--pressure-sweep', help='To run a sweep of pressure kicks.', action='store_true')
    parser.add_argument('--base-pressures', type=str, help='Specifies base pressures. Provide either a list of values in scientific notation or an iteration "iterate: start, stop, step"')
    parser.add_argument('--kick-pressure', type=str, help='Specifies pressure of kick.')

    parser.add_argument('--groove-height-sweep', help='To run a sweep of groove heights.', action='store_true')
    parser.add_argument('--groove-heights', type=str, help='Specifies heights of grooves. Provide either a list of values in scientific notation or an iteration "start, stop, step"')

    parser.add_argument('--process', help='To only process data in cases folder.', action='store_true')
    parser.add_argument('--run', help='To only run sweeps without processing.', action='store_true')
    parser.add_argument('--new-sweep', help="For when you want to start a new sweep.", action = 'store_true')

    args = parser.parse_args()

    for arg, value in vars(args).items():
        print(f"{arg}: {value}")

    response = input("Are these parameters correct? Enter Y to continue or N to quit: ").strip().lower()
    if response != 'y':
        print("Exiting the script.")
        sys.exit(0) 

    if(args.pressure_sweep and not(args.groove_height_sweep)):
         run_pressure_sweep(args.base_pressures, args.kick_pressure, args.process, args.run, args.new_sweep)

    if(args.groove_height_sweep):
         run_groove_height_sweep(args.base_pressures, args.kick_pressure, args.groove_heights, args.process, args.run, args.new_sweep)

def run_openfoam_command(script_path):
    try:
        # Check if the script file exists
        if not os.path.isfile(script_path):
            print(f"The script file {script_path} does not exist.")
            return

        # Spawn the openfoam-docker process
        child = pexpect.spawn('openfoam-docker', timeout=None)
        
        # Wait for the prompt to indicate it's ready for a command
        prompt = r'\$'  # Adjust this if the prompt is different
        child.expect(prompt)
        
        # Construct the command to run the .sh script
        script_command = f"./{script_path}"
        
        # Send the command to run the .sh script
        child.sendline(script_command)
        
        # Wait for the command to complete by waiting for the prompt again
        child.expect(prompt, timeout=None)

        child.sendline("exit")
        child.expect(pexpect.EOF)

        print("Script executed successfully inside the OpenFOAM Docker container.")
    except pexpect.exceptions.EOF as e:
        print(f"EOF error: {e}")
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"An error occurred: {e}")
    finally:
        if child.isalive():
            child.terminate()

def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        file_data = file.read()
    
    file_data = file_data.replace(old_string, new_string)
    
    with open(file_path, 'w') as file:
        file.write(file_data)

def replace_nth_line(file_path, n, new_line):
    # Read the file contents into a list
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Check if the specified line number is valid
    if n > len(lines) or n < 1:
        print(f"Line number {n} is out of range.")
        return
    
    # Replace the nth line (n-1 because list index starts from 0)
    lines[n-1] = new_line + '\n'
    
    # Write the updated list of lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def float_to_scientific_notation(number):
    # Set the precision high enough to handle most cases
    getcontext().prec = 50
    
    # Use Decimal for precise representation
    decimal_number = Decimal(str(number))
    # Round to significant digits to avoid precision issues
    rounded_number = decimal_number.quantize(Decimal('1e-15'), rounding=ROUND_HALF_UP)
    # Convert to scientific notation
    scientific_notation = format(rounded_number, ".16e")
    # Split into coefficient and exponent
    coefficient, exponent = scientific_notation.split('e')
    # Strip unnecessary trailing zeroes from coefficient
    coefficient = coefficient.rstrip('0').rstrip('.')
    # Reassemble the scientific notation
    return f"{coefficient}e{int(exponent)}"

def run_pressure_sweep(base_pressures, kick_pressure, process=False, run=False, new_sweep=False):
        
        list_of_pressure_sweep_dirs = os.listdir("data/pressure_sweep")

        if(new_sweep):
            list_of_pressure_sweep_dirs.remove("icofoam_base")
            list_of_pressure_sweep_dirs.remove("steady_state_base")

            list_of_pressure_sweep_dirs = sorted(list_of_pressure_sweep_dirs)

            print(list_of_pressure_sweep_dirs[-1])
            if(list_of_pressure_sweep_dirs[-1] == "cases"):
                new_index = 0
            else: 
                new_index = int(list_of_pressure_sweep_dirs[-1][-1]) + 1
            

            if os.path.exists("data/pressure_sweep/cases"):
                os.rename("data/pressure_sweep/cases", f"data/pressure_sweep/cases_{new_index}")

            os.makedirs("data/pressure_sweep/cases", exist_ok=True)

        replace_nth_line("src/bash_scripts/sim_sweep_pressure.sh", 4, f"kick_pressure_sci={kick_pressure}")
        
        base_pressures = base_pressures.lower().split()

        if base_pressures[0].lower() == "iterate:":
            start = float(base_pressures[1])
            stop = float(base_pressures[2])
            step = float(base_pressures[3])
            base_pressures = [float_to_scientific_notation(i) for i in np.arange(start, stop, step)]
        else:
            base_pressures = [i for i in base_pressures[0:]]

        print("Base pressure list: " + str(base_pressures))
        print("Kick pressure: " + kick_pressure)
        
        #running simulations
        if(run):

            for base_pressure in base_pressures:
                replace_nth_line("src/bash_scripts/sim_sweep_pressure.sh", 5, f"base_pressure_sci={base_pressure}")
                run_openfoam_command("src/bash_scripts/sim_sweep_pressure.sh")

        #post processing

        if(process):

            replace_nth_line("src/bash_scripts/post_processing.sh", 4, 'sweep_type="pressure_sweep"')

            for base_pressure in base_pressures:
                replace_nth_line("src/bash_scripts/post_processing.sh", 3, f"base_pressure_sci={base_pressure}")
                subprocess.run(["./src/bash_scripts/post_processing.sh"])

            subprocess.run(['python3', 'src/processing_scripts/get_grid_plots.py', "data/pressure_sweep/cases"])
            subprocess.run(['python3', 'src/processing_scripts/RE_vs_decay.py', "data/pressure_sweep/cases"])

        return 0

def run_groove_height_sweep(base_pressures, kick_pressure, groove_heights, process=False, run=False, new_sweep=False):
        
        list_of_sweep_dirs = os.listdir("data/groove_height_sweep")

        if(new_sweep):
            list_of_sweep_dirs.remove("icofoam_base")
            list_of_sweep_dirs.remove("steady_state_base")

            list_of_sweep_dirs = sorted(list_of_sweep_dirs)

            print(list_of_sweep_dirs[-1])
            if(list_of_sweep_dirs[-1] == "cases"):
                new_index = 0
            else: 
                new_index = int(list_of_sweep_dirs[-1][-1]) + 1
            

            if os.path.exists("data/groove_height_sweep/cases"):
                os.rename("data/groove_height_sweep/cases", f"data/groove_height_sweep/cases_{new_index}")

            os.makedirs("data/groove_height_sweep/cases", exist_ok=True)
        
        base_pressures = base_pressures.lower().split()
        groove_heights = groove_heights.lower().split()

        if base_pressures[0].lower() == "iterate:":
            start = float(base_pressures[1])
            stop = float(base_pressures[2])
            step = float(base_pressures[3])
            base_pressures = [float_to_scientific_notation(i) for i in np.arange(start, stop, step)]
        else:
            base_pressures = [i for i in base_pressures[0:]]


        if groove_heights[0].lower() == "iterate:":
            start = float(groove_heights[1])
            stop = float(groove_heights[2])
            step = float(groove_heights[3])
            groove_heights = [round(i, 2) for i in np.arange(start, stop, step)]
        else:
            groove_heights = [i for i in groove_heights[1:]]

        for groove_height in groove_heights:
            print(str(groove_height))
            for base_pressure in base_pressures:
                print("\t" + str(base_pressure))

        replace_nth_line("src/bash_scripts/sim_sweep_groove_height.sh", 4, f"kick_pressure_sci={kick_pressure}")

        #running simulations
        if(run):

            for groove_height in groove_heights:
                
                newpath = f"data/groove_height_sweep/cases/{groove_height}"
                if not os.path.exists(newpath):
                    os.makedirs(newpath)

                replace_nth_line("src/bash_scripts/sim_sweep_groove_height.sh", 6, f"groove_height={groove_height}")

                for base_pressure in base_pressures:

                    replace_nth_line("src/bash_scripts/sim_sweep_groove_height.sh", 5, f"base_pressure_sci={base_pressure}")

                    run_openfoam_command("src/bash_scripts/sim_sweep_groove_height.sh")

        
        #post processing

        if(process):

            for groove_height in groove_heights:

                replace_nth_line("src/bash_scripts/post_processing_grooves.sh", 5, f"groove_height={groove_height}")

                for base_pressure in base_pressures:
                    replace_nth_line("src/bash_scripts/post_processing_grooves.sh", 3, f"base_pressure_sci={base_pressure}")
                    subprocess.run(["./src/bash_scripts/post_processing_grooves.sh"])

                subprocess.run(['python3', 'src/processing_scripts/get_grid_plots.py', "data/groove_height_sweep/cases/" + str(groove_height)])
                subprocess.run(['python3', 'src/processing_scripts/RE_vs_decay.py', "data/groove_height_sweep/cases/" + str(groove_height)])
        
        return 0
    
if __name__ == "__main__":
    main()
