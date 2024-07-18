import os
import pexpect
import numpy as np
import subprocess

def run_openfoam_command(script_path):
    try:
        # Check if the script file exists
        if not os.path.isfile(script_path):
            print(f"The script file {script_path} does not exist.")
            return

        # Spawn the openfoam-docker process
        child = pexpect.spawn('openfoam-docker', timeout=None)
        
        # Log output for debugging
        with open("openfoam_log.txt", "wb") as log_file:
            child.logfile_read = log_file

            # Wait for the prompt to indicate it's ready for a command
            prompt = r'\$'  # Adjust this if the prompt is different
            child.expect(prompt)
            
            # Construct the command to run the .sh script
            script_command = f"./{script_path}"
            
            # Send the command to run the .sh script
            child.sendline(script_command)
            
            # Since simulations can take a long time, we loop and read outputs
            while True:
                try:
                    child.expect(prompt, timeout=None)  # Wait indefinitely
                    break  # Exit loop if prompt is detected
                except pexpect.exceptions.TIMEOUT:
                    pass  # Continue waiting

            # Send the exit command to close the OpenFOAM Docker terminal
            child.sendline("exit")
            child.expect(pexpect.EOF)
        
        print("Script executed successfully and exited the OpenFOAM Docker container.")
    except pexpect.exceptions.EOF as e:
        print(f"EOF error: {e}")
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"An error occurred: {e}")
    finally:
        if child.isalive():
            child.terminate()

def replace_string_in_file(file_path, search_string, replace_string):
    with open(file_path, 'r') as file:
        data = file.read()
    data = data.replace(search_string, replace_string)
    with open(file_path, 'w') as file:
        file.write(data)

def main_old():
        
        np.set_printoptions(formatter={'float': '{:.0e}'.format})

        script_path = "src/bash_scripts/test.sh"  # Replace with the path to your .sh file

        # Run the OpenFOAM Docker command
        for i in [10e-6, 13e-6, 16e-6]:

            print(i)
            replace_string_in_file("src/bash_scripts/test.sh", "REPLACE", str(i))
            run_openfoam_command(script_path)
            replace_string_in_file("src/bash_scripts/test.sh", str(i), "REPLACE")


        # Continue with the rest of the script
        print("Continuing with the rest of the script...")

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


def main():
    replace_nth_line("src/bash_scripts/post_processing.sh", 4, 'sweep_type="pressure_sweep"')


    for base_pressure in ['7e-6', '1e-5', '1.3e-5', '1.6e-5', '1.9e-5', '2.2e-5', '2.5e-5', '2.8e-5', '3.1e-5']:
        replace_nth_line("src/bash_scripts/post_processing.sh", 3, f"base_pressure_sci={base_pressure}")
        subprocess.run(["./src/bash_scripts/post_processing.sh"])

    subprocess.run(['python3', 'src/processing_scripts/get_grid_plots.py', "data/pressure_sweep/cases"])
    subprocess.run(['python3', 'src/processing_scripts/RE_vs_decay.py', "data/pressure_sweep/cases"])


if __name__ == "__main__":
    main()
