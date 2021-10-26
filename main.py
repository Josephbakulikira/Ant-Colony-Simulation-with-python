import pygame
from parameters import *
from vector import Vector
from colony import Colony

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
fps = 30

# initialize colony
colony = Colony()

# toggles
show_pheromone_food = True
show_pheromone_home = True

pause = False

run = True
while run:
    if not pause:
        screen.fill(black)
    delta_time = clock.tick(fps)
    # update caption
    frame_rate = int(clock.get_fps())
    pygame.display.set_caption("Ant Colony Simulation - FPS : ( {} )".format(frame_rate))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_f:
                show_pheromone_food = not show_pheromone_food
            if event.key == pygame.K_h:
                show_pheromone_home = not show_pheromone_home
            if event.key == pygame.K_SPACE:
                pause = not pause

    if not pause:
        colony.Update(screen, showFoodTrail=show_pheromone_food, showHomeTrail=show_pheromone_home, delta_time=delta_time)
        colony.Show(screen)

        pygame.display.flip()

pygame.quit()
