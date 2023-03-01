import importlib
import subprocess

# A list of required packages
required_packages = ["numpy", "matplotlib"]

# Check if all required packages are installed, and install them if they are not
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Package {package} not found. Installing...")
        subprocess.check_call(["pip", "install", package])

import numpy as np
import matplotlib.pyplot as plt


def cubic_bezier_curve_through_three_points(P0, P3, V, n=100):
    # find a point on a quadratic bezier curve that has t = 0.5
    Q = (P0 + 2 * V + P3) / 4

    # find two control points that are equidistant from V and lie on QV line
    p11 = Q + (Q - V)
    p22 = Q - (Q - V)

    # create an array of parameter values
    t = np.linspace(0, 1, n)

    # add a new axis to t so it has shape (n, 1)
    t = t[:, np.newaxis]

    # compute the curve using vectorized operations
    B = (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * p11 + \
        3 * (1 - t) * t**2 * p22 + t**3 * P3

    return B


def calculate_curve_points(start_point, end_point, H, num_points=100):
    # Calculate vector from start to end point
    start_to_end = end_point - start_point

    # Calculate the length of the start to end vector
    # start_to_end_length = np.linalg.norm(start_to_end)

    # Calculate the location along the start to end vector where the vertex should be located
    vertex_loc = start_to_end / 2

    # Raise the vertex location to the height of H
    vertex_point = np.array([vertex_loc[0], vertex_loc[1], H])

    # Calculate curve points
    curve_points = cubic_bezier_curve_through_three_points(start_point, end_point, vertex_point)

    return curve_points, vertex_point


# Sets up the plot
def set_plot_parameters(start_point, end_point, H, start_marker, end_marker, vertex_marker, ax, plt):
    curve_points, vertex_point = calculate_curve_points(start_point, end_point, H)
    ax.scatter(start_point[0], start_point[1], start_point[2], marker=start_marker, s=100)
    ax.scatter(end_point[0], end_point[1], end_point[2], marker=end_marker, s=100)
    ax.scatter(vertex_point[0], vertex_point[1], vertex_point[2], marker=vertex_marker, s=100)
    ax.plot(curve_points[:,0], curve_points[:,1], curve_points[:,2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.draw()
    plt.pause(0.001)

    return vertex_point


# Input values
start_point = np.array([0, 0, 0])
end_point = np.array([10, 10, 0])
H = 5

# Define markers for start point, end point, and vertex
start_marker = 'o'
end_marker = '^'
vertex_marker = '*'

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
vertex_point = set_plot_parameters(start_point, end_point, H, start_marker, end_marker, vertex_marker, ax, plt)

# Allow user to change curve parameters
while True:
    # Get user input
    print('\nCurrent parameters:')
    print(f'  Start point: {start_point}')
    print(f'  End point: {end_point}')
    print(f'  Vertex height: {H} (Current vertex coordinates: {vertex_point})')
    print('\nSelect a parameter to change:')
    print('  1: Start point')
    print('  2: End point')
    print('  3: Vertex height')
    print('  4: Change all parameters')
    print('  5: No changes')
    print('  6: Quit')
    selection = input('> ')

    # Change parameter based on user input
    if selection == '1':
        print('Enter new start point as "x y z":')
        try:
            x, y, z = [float(i) for i in input('> ').split()]
            start_point = np.array([x, y, z])
        except:
            print('Invalid input. Please try again.')
    elif selection == '2':
        print('Enter new end point as "x y z":')
        try:
            x, y, z = [float(i) for i in input('> ').split()]
            end_point = np.array([x, y, z])
        except:
            print('Invalid input. Please try again.')
    elif selection == '3':
        print('Enter new vertex height:')
        try:
            H = float(input('> '))
        except:
            print('Invalid input. Please try again.')
    elif selection == '4':
        print('Enter new parameters as "start_x start_y start_z end_x end_y end_z vertex_H":')
        try:
            start_x, start_y, start_z, end_x, end_y, end_z, H = [float(i) for i in input('> ').split()]
            start_point = np.array([start_x, start_y, start_z])
            end_point = np.array([end_x, end_y, end_z])
        except:
            print('Invalid input. Please try again.')
    elif selection == '5':
        print('No changes made.')
    elif selection == '6':
        break
    else:
        print('Invalid selection. Please try again.')
        continue

    if plt.fignum_exists(fig.number):
        ax.clear()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    vertex_point = set_plot_parameters(start_point, end_point, H, start_marker, end_marker, vertex_marker, ax, plt)
