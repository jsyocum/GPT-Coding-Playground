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


def bezier_curve(start_point, end_point, height, num_points=50):
    p0 = (start_point[0] + (end_point[0] - start_point[0])/3,
          start_point[1] + (end_point[1] - start_point[1])/3,
          start_point[2] + height)
    p1 = (end_point[0] - (end_point[0] - start_point[0])/3,
          end_point[1] - (end_point[1] - start_point[1])/3,
          start_point[2] + height)

    # Calculate points on the curve
    curve_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = (1 - t)**3 * start_point[0] + 3 * t * (1 - t)**2 * p0[0] + 3 * t**2 * (1 - t) * p1[0] + t**3 * end_point[0]
        y = (1 - t)**3 * start_point[1] + 3 * t * (1 - t)**2 * p0[1] + 3 * t**2 * (1 - t) * p1[1] + t**3 * end_point[1]
        z = (1 - t)**3 * start_point[2] + 3 * t * (1 - t)**2 * p0[2] + 3 * t**2 * (1 - t) * p1[2] + t**3 * end_point[2]
        curve_points.append((x, y, z))

    # Convert to NumPy array for slicing
    curve_points = np.array(curve_points)

    return curve_points


# Sets up the plot
def set_plot_parameters(start_point, end_point, height, start_marker, end_marker, ax, plt, num_points=50):
    curve_points = bezier_curve(start_point, end_point, height, num_points)
    ax.scatter(start_point[0], start_point[1], start_point[2], marker=start_marker, s=100)
    ax.scatter(end_point[0], end_point[1], end_point[2], marker=end_marker, s=100)
    ax.plot((start_point[0], end_point[0]), (start_point[1], end_point[1]), start_point[2] + height)
    ax.plot(curve_points[:,0], curve_points[:,1], curve_points[:,2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.draw()
    plt.pause(0.001)


# Input values
start_point = np.array([0, 0, 0])
end_point = np.array([10, 10, 0])
height = 65
num_points = 50

# Define markers for start point, end point, and vertex
start_marker = 'o'
end_marker = '^'

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
vertex_point = set_plot_parameters(start_point, end_point, height, start_marker, end_marker, ax, plt, num_points)

# Allow user to change curve parameters
while True:
    # Get user input
    print('\nCurrent parameters:')
    print(f'  Start point: {start_point}')
    print(f'  End point: {end_point}')
    print(f'  Height: {height}')
    print(f'  Points on curve: {num_points}')
    print('\nSelect a parameter to change:')
    print('  1: Start point')
    print('  2: End point')
    print('  3: Height')
    print('  4: Points on curve')
    print('  5: Change all parameters')
    print('  6: No changes')
    print('  7: Quit')
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
            height = float(input('> '))
        except:
            print('Invalid input. Please try again.')
    elif selection == '4':
        print('Enter new number of points on curve to calculate:')
        try:
            num_points = int(input('> '))
        except:
            print('Invalid input. Please try again.')
    elif selection == '5':
        print('Enter new parameters as "start_x start_y start_z end_x end_y end_z height num_points":')
        try:
            start_x, start_y, start_z, end_x, end_y, end_z, height, num_points = [float(i) for i in input('> ').split()]
            start_point = np.array([start_x, start_y, start_z])
            end_point = np.array([end_x, end_y, end_z])
        except:
            print('Invalid input. Please try again.')
    elif selection == '6':
        print('No changes made.')
    elif selection == '7':
        break
    else:
        print('Invalid selection. Please try again.')
        continue

    if plt.fignum_exists(fig.number):
        ax.clear()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    set_plot_parameters(start_point, end_point, height, start_marker, end_marker, ax, plt, num_points)
