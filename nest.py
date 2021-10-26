import random
import pygame
from vector import Vector
from parameters import *
from ant import Ant

pygame.font.init()
text_color = (white)
text_font = pygame.font.SysFont("Arial", 35)

class Nest:
    def __init__(self, position, n_ants=20):
        self.position = position
        self.n_ants = n_ants
        self.stock = 0
        self.ants = self.InitializeAnts()
        self.radius = 45
        self.color = blue

    def InitializeAnts(self):
        return [Ant(self.position, self) for _ in range(self.n_ants)]

    def Update(self, foods, pheromones, dt):
        for ant in self.ants:
            # boundary
            ant.Update(foods, pheromones, dt)
            if ant.position.x < 0:
                ant.position.x = width
            elif ant.position.x > width:
                ant.position.x = 0
            if ant.position.y < 0:
                ant.position.y = height
            elif ant.position.y > height:
                ant.position.y = 0
    def Show(self, screen, show_stock=True):
        pygame.draw.circle(screen, self.color, self.position.xy(), self.radius)

        if show_stock:
            text_surface = text_font.render(str(self.stock), True, text_color)
            text_rectangle = text_surface.get_rect(center=self.position.xy())
            screen.blit(text_surface, text_rectangle)
        for ant in self.ants:
            ant.Show(screen)
