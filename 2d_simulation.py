import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Set up display
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('CRT Simulation')

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
phosphor_screen = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
STARTING_ALPHA = 180 # Starting brightness
phosphor_color = [0, 255, 0]  # The last value is alpha for the brightness effect
PHOSPHOR_DIMMING_INTERVAL = 1
phosphors = []

def emit_electron():
    # Emit electron with initial position at electron_source and initial velocity to the right
    electrons.append({"position": list(electron_source), "velocity": [electron_speed, 0]})

def update_electrons():
        for electron in electrons:
            # Apply global acceleration to y-velocity to simulate magnetic field deflection
            electron['velocity'][1] += x_deflection_acceleration
            # Update position based on velocity
            electron['position'][0] += electron['velocity'][0]
            electron['position'][1] += electron['velocity'][1]

def draw_electrons():
    for electron in electrons:
        pygame.draw.circle(window, electron_color, (int(electron['position'][0]), int(electron['position'][1])), electron_radius)



def update_flat_hosphor_screen():
    # Check for collision between phosphor surface and electrons
    for electron in electrons:
        if electron['position'][0] >= window_width - 100:
            phosphors.append([(window_width - 100, int(electron['position'][1])), STARTING_ALPHA])
            electrons.remove(electron)  # Remove electron once it hits the phosphor screen
    
    # Go through existing phosphor list to alpha value brightness
    for phosphor in phosphors:
        # Draw a circle on the phosphor screen where the electron hits
        pygame.draw.circle(phosphor_screen, phosphor_color + [phosphor[1]], phosphor[0], 5)
        phosphor[1] -= PHOSPHOR_DIMMING_INTERVAL # Slowly reduce phosphor brightness

        if phosphor[1] < 0:
            phosphors.remove(phosphor) # Remove phosphor once the light total dissipates


vblank_timer = 0
hblank_timer = 0
is_hblank = False
is_vblank = False

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Emit a new electron every few frames if it is not currently hblank or vblank
    if pygame.time.get_ticks() % 1 == 0 and not is_hblank and not is_vblank:
        # Change the deflection field strength and direction
        x_deflection_acceleration += x_deflection_division

        emit_electron()

    if x_deflection_acceleration < -1 * x_deflection_limit:
        is_hblank = True
    
    if is_hblank:
        hblank_timer += 1
        if hblank_timer > 60:
            hblank_timer = 0
            is_hblank = False
            x_deflection_acceleration = x_deflection_limit

    # Update electrons
    update_electrons()

    # Update phosphor screen
    update_flat_hosphor_screen()

    # Clear the window
    window.fill((0, 0, 0))

    # Draw electrons
    draw_electrons()

    # Draw phosphor screen
    window.blit(phosphor_screen, (0, 0))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(80000)

# Quit pygame
pygame.quit()
sys.exit()
