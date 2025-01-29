import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def visualize_brain_slices(data, colormaps=['gray', 'viridis']):
   
    # Get middle slices from each axis
    x_middle = data.shape[0] // 2
    y_middle = data.shape[1] // 2
    z_middle = data.shape[2] // 2
    
    sagittal_slice = data[x_middle, :, :]
    coronal_slice = data[:, y_middle, :]
    axial_slice = data[:, :, z_middle]
    
    # Create figure with two rows (one for each colormap)
    for cmap in colormaps:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'Brain MRI Slices - {cmap} colormap')
        
        # Plot sagittal slice
        axes[0].imshow(sagittal_slice.T, cmap=cmap)
        axes[0].set_title('Sagittal View')
        axes[0].axis('off')
        
        # Plot coronal slice
        axes[1].imshow(coronal_slice.T, cmap=cmap)
        axes[1].set_title('Coronal View')
        axes[1].axis('off')
        
        # Plot axial slice
        axes[2].imshow(axial_slice.T, cmap=cmap)
        axes[2].set_title('Axial View')
        axes[2].axis('off')
        
        plt.tight_layout()
        
        plt.savefig(f'brain_slices_{cmap}.png')
        plt.close()


def main():
    filepath = 'T2.nii.gz'  # Update with your local file path

    img = nib.load(filepath)
    data = img.get_fdata()

    visualize_brain_slices(data)


if __name__ == "__main__":
    main()