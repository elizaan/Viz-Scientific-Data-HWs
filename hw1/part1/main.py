import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Function to plot box plot
def box_plot(data, label = None):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # ax = fig.add_subplot(111)
    bp = ax.boxplot(data, labels=[label])
    plt.title('Box plot of random numbers', fontsize=20)
    plt.xlabel('Distribution', fontsize=15)
    plt.ylabel('Values', fontsize=15)
    plt.savefig(f'box-plot_{label}.png')
    plt.close()
    # plt.show()

# Function to plot histogram with 20 bins
def histogram(data, num_bins=20, label=None):
    data_min = np.min(data)
    data_max = np.max(data)
    bin_width = (data_max - data_min) / num_bins
    
    bin_edges = np.arange(data_min, data_max + bin_width, bin_width)
    freq = [0] * num_bins

    for value in data:
        for i in range(num_bins):
            if bin_edges[i] <= value < bin_edges[i+1]:
                freq[i] += 1
                
        
    plt.bar(bin_edges[:-1], freq, width=bin_width, label=label)
    plt.title('Histogram of random numbers', fontsize=20)
    plt.xlabel('Values', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.legend()
    plt.savefig('histogram.png')
    plt.close()
    # plt.show()

# line graph cumulatively showing the number of values that fall within each bin
def cumulative_chart(data, num_bins=20, label=None):
    sorted_data = np.sort(data)
    cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.plot(sorted_data, cumulative, label=label)
    plt.title('Cumulative distribution', fontsize=20)
    plt.xlabel('Values', fontsize=15)
    plt.ylabel('Cumulative frequency', fontsize=15)
    plt.legend()
    plt.savefig(f'cumulative-plot_{label}.png')
    plt.close()
    # plt.show()

# 2d array scatter plot
def scatter_plot(x, y, label=None):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.scatter(x, y, label=label)
    plt.title(f'Scatter plot of {label} random numbers', fontsize=20)
    plt.xlabel('X', fontsize=15)
    plt.ylabel('Y', fontsize=15)
    plt.savefig(f'scatter-plot-2d_{label}.png')
    plt.close()
    # plt.show()

def count_points_in_grid(x, y, label=None):
    # grid = np.zeros((100, 100))
    
    # # Clip values to [0,1] range
    # x_clipped = np.clip(x, 0, 1)
    # y_clipped = np.clip(y, 0, 1)
    
    # # Convert point coordinates to grid indices
    # # Multiply by 99.99 instead of 99 to handle edge case of x/y = 1
    # x_indices = np.floor(x_clipped * 99.99).astype(int)
    # y_indices = np.floor(y_clipped * 99.99).astype(int)
    
    # # Count points in each grid cell
    # for i, j in zip(x_indices, y_indices):
    #     grid[i, j] += 1
    
    # # Display grid as image
    # fig = plt.figure(figsize=(10, 7))
    # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    
    # im = ax.imshow(grid, origin='lower')
    # plt.colorbar(im, ax=ax, label='Count')
    
    # plt.title(f'Grid counts for {label} distribution', fontsize=20)
    # plt.xlabel('X grid index', fontsize=15)
    # plt.ylabel('Y grid index', fontsize=15)
    # plt.show()
    
    # return grid

    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    
    hist, xedges, yedges = np.histogram2d(x, y, bins=100)
    
    # Create a mesh grid for plotting
    X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
    
    im = ax.imshow(hist.T, origin='lower', aspect='auto', 
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap='viridis')
    
    plt.colorbar(im, ax=ax, label='Count')
    
    plt.title(f'2D Density plot of {label} distribution', fontsize=20)
    plt.xlabel('X', fontsize=15)
    plt.ylabel('Y', fontsize=15)
    plt.savefig(f'2d-density-plot_{label}.png')
    plt.close()
    # plt.show()

def contour_plot(x, y, label=None):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    
    # contour = ax.tricontourf(x, y, np.zeros_like(x), levels=10)
    contour = ax.tricontourf(x, y, z, levels=10)
    
    plt.colorbar(contour, ax=ax, label='Density')
    
    plt.title(f'Contour plot of {label} distribution', fontsize=20)
    plt.xlabel('X', fontsize=15)
    plt.ylabel('Y', fontsize=15)
    plt.savefig(f'contour-plot_{label}.png')
    plt.close()
    # plt.show()

def main():
    random_numbers1 = np.random.uniform(0, 1, size=100)

    # For the Gaussian distribution between 1 and 100:
    # - Mean should be at the center: (1 + 100)/2 = 50.5
    # - For ~95% of values to fall within [1,100], we want 4 standard deviations 
    #   to span this range: (100-1)/4 ≈ 25

    random_numbers2 = np.random.normal(loc=50.5, scale=25, size=200)

    # print("Random number 1: ", random_numbers1)
    # print("Random number 2: ", random_numbers2)

    box_plot(random_numbers1, label='Uniform')
    box_plot(random_numbers2, label='Gaussian')

    # histogram(random_numbers1, label='Uniform')
    histogram(random_numbers2, label='Gaussian')

    file1 = "random_numbers1.bin"
    file2 = "random_numbers2.bin"
    
    random_numbers1.tofile(file1)
    random_numbers2.tofile(file2)

    f_random_numbers1 = np.fromfile(file1, dtype=float)
    f_random_numbers2 = np.fromfile(file2, dtype=float)

    cumulative_chart(f_random_numbers1, label='Uniform')
    cumulative_chart(f_random_numbers2, label='Gaussian')

    x_uniform = np.random.uniform(0, 1, size=5000)
    x_gaussian = np.random.normal(loc=0.5, scale=0.2, size=5000)

    y_uniform = np.random.uniform(0, 1, size=5000)
    y_gaussian = np.random.normal(loc=0.5, scale=0.2, size=5000)

    scatter_plot(x_uniform, y_uniform, label='Uniform')
    scatter_plot(x_gaussian, y_gaussian, label='Gaussian')

    count_points_in_grid(x_uniform, y_uniform, label='Uniform')
    count_points_in_grid(x_gaussian, y_gaussian, label='Gaussian')

    contour_plot(x_uniform, y_uniform, label='Uniform')
    contour_plot(x_gaussian, y_gaussian, label='Gaussian') 


if __name__ == "__main__":
    main()