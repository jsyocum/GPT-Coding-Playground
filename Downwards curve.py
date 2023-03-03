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


def find_vertex_point(start_point, end_point, height):
    height += start_point[2]

    # find the midpoint between start and end points
    midpoint = (start_point + end_point) / 2.0

    # calculate the vector from start to end
    line_vec = end_point - start_point

    # calculate the perpendicular vector
    perp_vec = np.array([line_vec[1], -line_vec[0], 0.0], dtype=float)

    # normalize the perpendicular vector
    perp_vec /= np.linalg.norm(perp_vec)

    # calculate the vertex point
    vertex_point = midpoint + height * perp_vec

    # rotate the vertex_point
    vertex_point = rotate_curve_points(vertex_point, start_point, end_point, 90)

    return vertex_point


def bezier_curve(start_point, vertex_point, end_point, n):
    # Calculate the control point
    control_point = 2 * vertex_point - 0.5 * (start_point + end_point)

    # Calculate the curve points
    t = np.linspace(0, 1, n).reshape((1, n))
    B = (1 - t) ** 2 * start_point.reshape((3, 1)) + 2 * (1 - t) * t * control_point.reshape((3, 1)) + t ** 2 * end_point.reshape((3, 1))
    curve_points = B.T

    return curve_points


def rotate_curve_points(curve_points, start_point, end_point, angle_degrees):
    # calculate axis vector
    axis_vec = end_point - start_point
    axis_norm = np.linalg.norm(axis_vec)
    if axis_norm == 0:
        raise ValueError("start and end points are the same")
    axis_unit = axis_vec / axis_norm

    # create rotation matrix around axis
    angle_radians = np.radians(angle_degrees)
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    rot_matrix = np.array([[cos_theta + axis_unit[0]**2*(1-cos_theta),
                            axis_unit[0]*axis_unit[1]*(1-cos_theta) - axis_unit[2]*sin_theta,
                            axis_unit[0]*axis_unit[2]*(1-cos_theta) + axis_unit[1]*sin_theta],
                           [axis_unit[1]*axis_unit[0]*(1-cos_theta) + axis_unit[2]*sin_theta,
                            cos_theta + axis_unit[1]**2*(1-cos_theta),
                            axis_unit[1]*axis_unit[2]*(1-cos_theta) - axis_unit[0]*sin_theta],
                           [axis_unit[2]*axis_unit[0]*(1-cos_theta) - axis_unit[1]*sin_theta,
                            axis_unit[2]*axis_unit[1]*(1-cos_theta) + axis_unit[0]*sin_theta,
                            cos_theta + axis_unit[2]**2*(1-cos_theta)]])

    # rotate curve points
    rotated_points = np.dot(curve_points - start_point, rot_matrix) + start_point

    return rotated_points


def calculate_curve_points(start_point, end_point, H, num_points=100):
    # Calculate vertex point
    vertex_point = find_vertex_point(start_point, end_point, H)

    # Calculate curve points
    curve_points = bezier_curve(start_point, vertex_point, end_point, num_points)

    # Rotate curve points
    # curve_points = rotate_curve_points(curve_points, start_point, end_point, 90)

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
