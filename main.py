import pygame
from config import *
from vector import Vector
from colony import Colony

def main():
    pygame.display.init()
    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()
    fps = 30
    
    # Pre-create surfaces
    pheromone_layer = pygame.Surface(RESOLUTION, pygame.SRCALPHA, 32)  # Ensure 32-bit for alpha
    background = pygame.Surface(RESOLUTION)
    
    colony = Colony()
    show_pheromone_food = True
    show_pheromone_home = True
    pause = False
    
    # Visible area tracking
    view_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    
    running = True
    while running:
        if not pause:
            # Clear only changed areas
            dirty_rects = []
            
        delta_time = clock.tick(fps)
        pygame.display.set_caption(f"Ant Colony Simulation - FPS: {int(clock.get_fps())}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    show_pheromone_food = not show_pheromone_food
                if event.key == pygame.K_h:
                    show_pheromone_home = not show_pheromone_home
                if event.key == pygame.K_SPACE:
                    pause = not pause

        if not pause:
            # Clear layers
            background.fill(BLACK)  # Changed from black to BLACK
            # pheromone_layer.fill((0,0,0,0))  # Ensure this line remains commented out
            
            colony.Update(pheromone_layer, show_pheromone_food, show_pheromone_home, delta_time)
            
            # Composite layers
            screen.blit(background, (0,0))
            screen.blit(pheromone_layer, (0,0), special_flags=pygame.BLEND_ADD)  # Ensure additive blending
            colony.Show(screen)
            
            pygame.display.flip()

if __name__ == "__main__":
    main()
