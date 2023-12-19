import pygame

# Window size
WINDOW_WIDTH    = 500
WINDOW_HEIGHT   = 500
WINDOW_SURFACE  = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE

DARK_BLUE = (   3,   5,  54 )
WHITE     = ( 255, 255, 255 )

### initialisation
pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
pygame.display.set_caption("Bad Mouse Paint")

# Drawing on
canvas = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
canvas.fill( DARK_BLUE )

### Main Loop
mouse_down = False
clock = pygame.time.Clock()
done = False
while not done:

    # Handle user-input
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            done = True
        elif ( event.type == pygame.MOUSEBUTTONDOWN ):
            mouse_down = True
        elif ( event.type == pygame.MOUSEBUTTONUP ):
            mouse_down = False

    # Mouse Movement
    if ( mouse_down ):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle( canvas, WHITE, mouse_pos, 5, 0 )

    # Update the window, but not more than 60fps
    window.blit( canvas, ( 0, 0 ) )
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)


pygame.quit()