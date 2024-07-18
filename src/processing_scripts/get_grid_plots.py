import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
import sys

def create_graph_grid(base_dir, output_file):
    case_dirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))], key=lambda x: float(x.replace('e-', 'e-')))
    image_files = [os.path.join(base_dir, case, "Uy_vs_time.png") for case in case_dirs]

    # Determine the grid size
    num_images = len(image_files)
    grid_cols = 3  # Adjust the number of columns as needed
    grid_rows = ceil(num_images / grid_cols)

    # Create the grid plot
    fig, axes = plt.subplots(grid_rows, grid_cols, figsize=(15, grid_rows * 5))

    for ax, img_file in zip(axes.flatten(), image_files):
        if os.path.isfile(img_file):
            img = mpimg.imread(img_file)
            ax.imshow(img)
            ax.axis('off')
        else:
            ax.axis('off')  # Hide axes without an image

    # Hide any unused subplots
    for ax in axes.flatten()[num_images:]:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":

    base_dir = sys.argv[1]
    output_file = os.path.join(base_dir, 'Uy_vs_time_grid.png')

    create_graph_grid(base_dir, output_file)
