import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

# Initialize Pygame
pygame.init()

# Set up display
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('CRT Simulation')

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Set up Pygame display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

# List to store sphere positions
spheres = []


# NTSC Video Properties:
SCAN_LINE_LENGTH = 63.6 # 63.6 μs per scan line in NTSC, 64 for PAL
HORIZONTAL_BLANKING_INTERVAL = SCAN_LINE_LENGTH * 0.172 # 10.9 μs of the 63.6


# Starting acceleration for the electrons
x_deflection_limit = 0.05
x_deflection_acceleration = 0.05
x_deflection_division = -0.0005

# List of all existing electrons
electrons = []

# Radius/Speed of the visable electrons
electron_radius = 2
electron_speed = 10
electron_color = (255, 255, 255)

# Electron source position
electron_source = (100, 300)

# Phosphor Settings
#phosphor_screen = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
#STARTING_ALPHA = 180 # Starting brightness
#phosphor_color = [0, 255, 0]  # The last value is alpha for the brightness effect
#PHOSPHOR_DIMMING_INTERVAL = 1
#phosphors = []



# Function to draw a white sphere
def draw_electron(radius=0.1, slices=10, stacks=10):
    quad = gluNewQuadric()
    glColor3fv((1, 1, 1))
    gluSphere(quad, radius, slices, stacks)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Add a new sphere with random Y position on the left side
    if random.random() < 0.01:
        spheres.append([-2.0, random.uniform(-1.5, 1.5), 0.0])

    new_spheres = []
    for sphere in spheres:
        x, y, z = sphere
        x += 0.02  # Move the sphere to the right
        if x < 0.9:  # Check if it's still visible
            glPushMatrix()
            glTranslatef(x, y, z)
            draw_electron()
            glPopMatrix()
            new_spheres.append([x, y, z])
    spheres = new_spheres
    print(spheres)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()