import pygame
import sys
import time

# Set up display
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('CRT Simulation')


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
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
sys.exit()