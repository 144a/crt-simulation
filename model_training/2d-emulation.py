import numpy as np
import matplotlib.pyplot as plt
import os
from shutil import rmtree
import random

def generate_crosshatch(horizontal_lines, vertical_lines, width, height):
    """ Generate a basic crosshatch pattern """
    # Using linspace to create line positions
    h_lines = np.linspace(-height/2, height/2, horizontal_lines)
    v_lines = np.linspace(-width/2, width/2, vertical_lines)

    # Plotting lines
    for h in h_lines:
        plt.plot([-width/2, width/2], [h, h], color='black')
    for v in v_lines:
        plt.plot([v, v], [-height/2, height/2], color='black')

def apply_transformation(X, Y, pin_strength, pinbal_angle, key_angle, keybal_angle, h_scale, v_scale):
    """ Apply pincushion, keystone, and size adjustments """
    # Pincushion adjustment
    R = np.sqrt(X**2 + Y**2)
    factor = 1 + pin_strength * R**2
    X = X * factor

    # Keystone Balance adjustment
    X += keybal_angle * Y * np.sign(X)

    # Keystone adjustment
    X += key_angle * Y

    # Size adjustments
    X *= h_scale
    Y *= v_scale

    return X, Y

def display_transformed_grid(horizontal_lines, vertical_lines, width, height, pin_strength, pinbal_angle, key_angle, keybal_angle, h_scale, v_scale):
    """ Display the transformed grid """
    # Create a meshgrid with fewer points
    x = np.linspace(-width/2, width/2, vertical_lines)
    y = np.linspace(-height/2, height/2, horizontal_lines)
    X, Y = np.meshgrid(x, y)

    # Apply transformation
    X, Y = apply_transformation(X, Y, pin_strength, pinbal_angle, key_angle, keybal_angle, h_scale, v_scale)

    # Plotting the transformed grid
    for i in range(X.shape[0]):
        plt.plot(X[i, :], Y[i, :], color='black')
    for j in range(Y.shape[1]):
        plt.plot(X[:, j], Y[:, j], color='black')
    plt.axis('equal')

def manual_simulation():
    # Parameters
    horizontal_lines = 15
    vertical_lines = 15
    width = 20
    height = 20

    # All Values are [-100, 100]
    pincushion_strength = -20
    keystone_angle = 0
    pincushion_balance_strength = 0
    keystone_balance_angle = 0


    horizontal_scale = 1
    vertical_scale = 1

    # Correct for appropriate value ranges
    pincushion_strength *= 0.000015
    pincushion_balance_strength *= 0.000015
    keystone_angle *= 0.001
    keystone_balance_angle *= 0.001

    # Display the transformed grid
    display_transformed_grid(horizontal_lines, vertical_lines, width, height, pincushion_strength, pincushion_balance_strength, keystone_angle, keystone_balance_angle, horizontal_scale, vertical_scale)
    plt.xlim(width/2 * -1.1, width/2 * 1.1)
    plt.ylim(height/2 * -1.1, height/2 * 1.1)
    #plt.show()

    path = os.path.join(os.getcwd(), 'generated_data')

    # Set up data folder
    try:  
        os.mkdir(path)  
    except OSError as error:  
        rmtree(path)
        os.mkdir(path)

    os.chdir(path)
    plt.savefig('testimg1.png')
    plt.clf()
    plt.show()

def automatic_simulation():
    # Parameters
    horizontal_lines = 15
    vertical_lines = 15
    width = 20
    height = 20

    # Randomize the initial conditions:
    pin_list = np.linspace(-100,100,num=200).tolist()
    key_list = np.linspace(-100,100,num=200).tolist()
    pinbal_list = np.linspace(-100,100,num=200).tolist()
    keybal_list = np.linspace(-100,100,num=200).tolist()
    random.shuffle(pin_list)
    random.shuffle(key_list)
    random.shuffle(pinbal_list)
    random.shuffle(keybal_list)


    path = os.path.join(os.getcwd(), 'generated_data')

    # Set up data folder
    try:  
        os.mkdir(path)  
    except OSError as error:  
        rmtree(path)
        os.mkdir(path)

    image_count = 0

    while len(pin_list) > 0:
        # Load values from randomized lists
        pincushion_strength = pin_list.pop(0)
        keystone_angle = key_list.pop(0)
        pincushion_balance_strength = pinbal_list.pop(0)
        keystone_balance_angle = keybal_list.pop(0) 

        file_name = f'_{horizontal_lines}_{vertical_lines}_{width}_{height}_{pincushion_strength}_{keystone_angle}_{pincushion_balance_strength}_{keystone_balance_angle}_{keystone_balance_angle}.png'

        # Set to be static for the time being
        horizontal_scale = 1
        vertical_scale = 1

        # Correct for appropriate value ranges
        pincushion_strength *= 0.000015
        pincushion_balance_strength *= 0.000015
        keystone_angle *= 0.001
        keystone_balance_angle *= 0.001

        # Display the transformed grid
        display_transformed_grid(horizontal_lines, vertical_lines, width, height, pincushion_strength, pincushion_balance_strength, keystone_angle, keystone_balance_angle, horizontal_scale, vertical_scale)
        
        plt.xlim(width/2 * -1.1, width/2 * 1.1)
        plt.ylim(height/2 * -1.1, height/2 * 1.1)

        os.chdir(path)
        plt.savefig(str(image_count) + file_name)
        plt.clf()

        print(str(image_count) + file_name)

        image_count += 1
        


if __name__ == '__main__':

    automatic_simulation()







