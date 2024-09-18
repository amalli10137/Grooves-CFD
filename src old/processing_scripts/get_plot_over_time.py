import sys
import os
import csv

def get_plot_over_time(cell_ids, number):
    base_dir = "data/"+sys.argv[3]+"/cases/" + number + "/icofoam_" + number
    output_file = os.path.join(base_dir, "../U_vs_time.csv")
    
    # Filter out non-numeric directories
    time_steps = sorted(
        [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.replace('.', '', 1).isdigit()],
        key=lambda x: float(x)
    )
    
    data = {}
    
    for time_step in time_steps:
        u_file_path = os.path.join(base_dir, time_step, 'U')
        
        if os.path.isfile(u_file_path):
            with open(u_file_path, 'r') as u_file:
                lines = u_file.readlines()
                
                # Find the line with "internalField"
                try:
                    internal_field_line = next(i for i, line in enumerate(lines) if 'internalField' in line)
                except StopIteration:
                    print(f"internalField not found in {u_file_path}")
                    continue
                
                # Extract velocities for specified cell IDs
                for cell_id in cell_ids:
                    cell_line = internal_field_line + 3 + cell_id
                    if cell_line < len(lines):
                        try:
                            velocity = lines[cell_line].strip()
                            # Validate if the velocity line contains valid data
                            if velocity:
                                if time_step not in data:
                                    data[time_step] = {}
                                data[time_step][cell_id] = velocity
                        except ValueError:
                            print(f"Error reading velocity for cell {cell_id} at time {time_step}")
                            continue
    
    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['time'] + [f'U_{cell_id}' for cell_id in cell_ids]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for time_step in sorted(data.keys(), key=float):
            row = {'time': time_step}
            for cell_id in cell_ids:
                row[f'U_{cell_id}'] = data[time_step].get(cell_id, '')
            writer.writerow(row)

if __name__ == "__main__":
    # Example usage
    cell_ids = [int(c) for c in sys.argv[1].split(',')] 
    nums = sys.argv[2]
    get_plot_over_time(cell_ids, nums)
