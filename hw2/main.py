#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# Draws the starting plot. Don't change this code
def draw_initial_plot(data, x, y):

    # Draw grid and hide labels
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    ax.set_xlim(-.5, len(x)-.5)
    ax.set_ylim(-.5, len(y)-.5)
    ax.grid(True)
    plt.xticks(np.arange(-.5,data.shape[0], step=1))
    plt.yticks(np.arange(-.5,data.shape[1], step=1))
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    # Add text on cells
    for i in range(len(x)):
        for j in range(len(y)):
            ax.text(i,j+.1, str(int(data[i,j])), ha='center', va='bottom', size=18)

    return fig, ax


# Load data and make range arrays for looping
data = np.load("hw2/scalars_2D.npy") # access scalar values by data[i,j]
x = np.arange(0,data.shape[0])
y = np.arange(0,data.shape[1])

fig, ax = draw_initial_plot(data, x, y)


# Draws a dot at a given point
# point - type of tuple or array with length 2: (x,y) or [x,y]
# color - string of color to draw dot - Ex: ""red", "green", "blue"
def draw_dot(point, color):
    ax.scatter(point[0], point[1], color=color)

# Draws a line from point0 to point1
# point0 - type of tuple or array with length 2: (x,y) or [x,y]
# point1 - type of tuple or array with length 2: (x,y) or [x,y]
def draw_line(point0, point1):
    x = [point0[0], point1[0]]
    y = [point0[1], point1[1]]
    ax.plot(x, y, color="black")



#-----------------------
# ASSIGNMENT STARTS HERE
#-----------------------
parser = argparse.ArgumentParser(description='Marching Squares Algorithm')
parser.add_argument('--li', action='store_true', help='Use linear interpolation instead of midpoint method')
args = parser.parse_args()

isovalue = 50
# linear_interpolation = False # else, midpoint method
linear_interpolation = args.li

# Add colored points to identify if cells are below or above the isovalue threshold
ax.scatter([], [], color='black', label='below')  # Empty black dot for legend
ax.scatter([], [], color='red', label='above')    # Empty red dot for legend
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Place legend outside the plot

for i in x:
    for j in y:
        # TODO Part 1
        if data[i, j] >= isovalue:
            draw_dot((i, j), "red")
        else:
            draw_dot((i, j), "black")
        continue


# Draw Lines in Marching Squares - Midpoint
def march_sq_midpoint(data, i, j, isovalue):
    # TODO Part 2
    v0 = data[i, j]       # Bottom left
    v1 = data[i+1, j]     # Bottom right
    v2 = data[i+1, j+1]   # Top right
    v3 = data[i, j+1]     # Top left
    
    # case number by comparing each vertex to isovalue
    case = 0
    if v0 >= isovalue: case |= 1    # Bottom left
    if v1 >= isovalue: case |= 2    # Bottom right
    if v2 >= isovalue: case |= 4    # Top right
    if v3 >= isovalue: case |= 8    # Top left
    
    # Calculate midpoints of cell edges
    bottom = [i + 0.5, j]      # Bottom edge midpoint
    right = [i + 1, j + 0.5]   # Right edge midpoint
    top = [i + 0.5, j + 1]     # Top edge midpoint
    left = [i, j + 0.5]        # Left edge midpoint
    
    # Draw appropriate lines based on case number
    if case == 1 or case == 14:
        draw_line(bottom, left)
    elif case == 2 or case == 13:
        draw_line(bottom, right)
    elif case == 3 or case == 12:
        draw_line(left, right)
    elif case == 4 or case == 11:
        draw_line(right, top)
    elif case == 5:
        draw_line(bottom, right)
        draw_line(left, top)
    elif case == 6 or case == 9:
        draw_line(bottom, top)
    elif case == 7 or case == 8:
        draw_line(left, top)
    elif case == 10:
        draw_line(left, bottom)
        draw_line(right, top)
    else:
        return
    # # Cases 0 and 15 have no lines
    # return

# Draw Lines in Marching Squares - Linear Interpolation
def march_sq_lin_interp(data, i, j, isovalue):
    # TODO Part 3
    v0 = data[i, j]       # Bottom left
    v1 = data[i+1, j]     # Bottom right
    v2 = data[i+1, j+1]   # Top right
    v3 = data[i, j+1]     # Top left

    case = 0
    if v0 >= isovalue: case |= 1    # Bottom left
    if v1 >= isovalue: case |= 2    # Bottom right
    if v2 >= isovalue: case |= 4    # Top right
    if v3 >= isovalue: case |= 8    # Top left

    def interpolate(v1, v2, p1, p2):
        if abs(v1 - v2) < 1e-10:     # devison by zero
            return p1
        t = (isovalue - v1) / (v2 - v1)
        return[p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])]
    
    # interpolated points of cell edges
    bottom = interpolate(v0, v1, [i, j], [i+1, j])     # Bottom edge point
    right = interpolate(v1, v2, [i+1, j], [i+1, j+1])  # Right edge point
    top = interpolate(v2, v3, [i+1, j+1], [i, j+1])    # Top edge point
    left = interpolate(v3, v0, [i, j+1], [i, j])       # Left edge point

    # appropriate lines based on case number
    if case == 1 or case == 14:
        draw_line(bottom, left)
    elif case == 2 or case == 13:
        draw_line(bottom, right)
    elif case == 3 or case == 12:
        draw_line(left, right)
    elif case == 4 or case == 11:
        draw_line(right, top)
    elif case == 5:
        draw_line(bottom, right)
        draw_line(left, top)
    elif case == 6 or case == 9:
        draw_line(bottom, top)
    elif case == 7 or case == 8:
        draw_line(left, top)
    elif case == 10:
        draw_line(left, bottom)
        draw_line(right, top)
    else:
        return


# Implement simple marching squares with midpoint approach
for i in x[0:-1]:
    for j in y[0:-1]:
        if (linear_interpolation):
            march_sq_lin_interp(data, i, j, isovalue)
        else:
            march_sq_midpoint(data, i, j, isovalue)


plt.show()