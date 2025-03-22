import numpy as np
import matplotlib.pyplot as plt
import random

def bilinear_interpolation(vecs, x, y):
    x1, x2 = int(x), int(x) + 1
    y1, y2 = int(y), int(y) + 1
    q11 = vecs[x1, y1]
    q12 = vecs[x1, y2]
    q21 = vecs[x2, y1]
    q22 = vecs[x2, y2]

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def euler_method(vecs, seed_point, step_size, steps):
    points = [seed_point]
    for i in range(steps):
        x, y = points[-1]

        if x < 0 or y < 0 or x >= vecs.shape[0] - 1 or y >= vecs.shape[1] - 1:
            break

        dx, dy = bilinear_interpolation(vecs, x, y)
        new_x, new_y = x + dx * step_size, y + dy * step_size
        points.append((new_x, new_y))

    return points

def rk4(vecs, seed_point, step_size, steps):
    def func(x, y):
        if x < 0 or y < 0 or x >= vecs.shape[0] - 1 or y >= vecs.shape[1] - 1:
            return np.array([0, 0])
        return bilinear_interpolation(vecs, x, y)

    points = [seed_point]
    for _ in range(steps):
        x, y = points[-1]
        k1 = func(x, y)
        k2 = func(x + 0.5 * step_size * k1[0], y + 0.5 * step_size * k1[1])
        k3 = func(x + 0.5 * step_size * k2[0], y + 0.5 * step_size * k2[1])
        k4 = func(x + step_size * k3[0], y + step_size * k3[1])

        dx, dy = step_size * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        new_x, new_y = x + dx, y + dy
        points.append((new_x, new_y))

    return points

def plot_figures(step_size, steps, method=euler_method):

    streamlines = [method(vecs, seed_point, step_size, steps) for seed_point in seed_points]
    
    plt.figure()
    plt.plot(xx, yy, marker='.', color='b', linestyle='none')
    plt.quiver(xx, yy, vecs_flat[:, 0], vecs_flat[:, 1], width=0.001)

    for seed_point in seed_points:
        plt.plot(seed_point[0], seed_point[1], marker='.', color='r', linestyle='none')

    for streamline in streamlines:
        streamline = np.array(streamline)
        plt.plot(streamline[:, 0], streamline[:, 1], color='r')

    plt.xlim(0, 19)
    plt.ylim(0, 19)

    plt.title(f'Wind Data Visualization (Method: {method.__name__}, Step size: {step_size}, Steps: {steps})')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.savefig(f'wind_data_visualization_method_{method.__name__}_step_size_{step_size}_steps_{steps}).png')

# Get data
vecs = np.reshape(np.fromfile("wind_vectors.raw"), (20, 20, 2))
vecs_flat = np.reshape(vecs, (400, 2))  # useful for plotting
vecs = vecs.transpose(1, 0, 2)  # needed otherwise vectors don't match with plot

# X and Y coordinates of points where each vector is in space
xx, yy = np.meshgrid(np.arange(0, 20), np.arange(0, 20))

# Set the random seed manually
random.seed(42)

# Generate 15 random seed points
seed_points = [(random.randint(0, 19), random.randint(0, 19)) for _ in range(15)]

# Part-3: answer-1
seed_points_1 = np.array(seed_points)
plt.scatter(seed_points_1[:, 0], seed_points_1[:, 1], color='r', marker='o', s=50, label='Seed Points')
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Wind Vectors and Seed Points')
plt.savefig('wind_vectors_seed_points.png')
plt.show()

# Create plots with different step sizes and step counts using the Euler method
# Part-3: answer-2
plot_figures(step_size=0.3, steps=8)
# Part-3: answer-3
plot_figures(step_size=0.15, steps=16)
plot_figures(step_size=0.075, steps=32)
plot_figures(step_size=0.0375, steps=64)

# Create plots with different step sizes and step counts using the RK4 method
# Part-4: answer-1
plot_figures(step_size=0.3, steps=8, method=rk4)
plot_figures(step_size=0.15, steps=16, method=rk4)
plot_figures(step_size=0.075, steps=32, method=rk4)
plot_figures(step_size=0.0375, steps=64, method=rk4)

# Show all plots
plt.show()