from parameters import *
import pygame
from vector import Vector
from math import ceil

def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

class Pheromone:
    def __init__(self, position, direction, type="Food"):
        self.position = position
        self.direction = direction
        self.strength = 100
        self.max_strength = 100
        self.evaporation_rate = evo_food_rate
        self.home_evaporation_rate = evo_home_rate
        self.color = green
        self.type = type
        self.radius = 2

    def Update(self):
        # reduce the pheromone
        if self.type == "food":
            self.strength -= self.evaporation_rate
        elif self.type == 'home':
            self.strength -= self.home_evaporation_rate

    def Combine(self, other):
        # merge a solution of two pheromones close to each other
        if type(other) != Pheromone:
            print("Error")
        average_position = Vector.Average([self.position, other.position])
        average_direction = Vector.Average([self.direction, other.direction])

        new_strength = min(self.strength + other.strength, self.max_strength)

        self.position = average_position
        self.direction = average_position
        self.strength = new_strength

    def Show(self, screen, showFoodTrail, showHomeTrail):
        if showFoodTrail:
            if self.type == "food":
                # alpha = int(translateValue(self.strength, 0, 100, 1, 4))
                # pygame.draw.circle(screen, (234, 52, 80) , self.position.xy(), alpha)
                val = max(self.strength, 1)
                alpha = int(translateValue(val, 0, 100, 1, 255))
                r, g, b = (234, 52, 80)
                surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
                pygame.draw.circle(surface, (r, g, b, alpha), (self.radius, self.radius), self.radius)
                screen.blit(surface, (self.position-self.radius).xy())
        if showHomeTrail:
            if self.type == "home":
                # alpha = int(translateValue(self.strength, 0, 100, 0, 4))
                # pygame.draw.circle(screen, (125, 55, 252), self.position.xy(), alpha)
                val = max(self.strength, 1)
                alpha = int(translateValue(val, 0, 100, 1, 255))
                r, g, b = (125, 55, 252)
                surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
                pygame.draw.circle(surface, (r, g, b, alpha), (self.radius, self.radius), self.radius)
                screen.blit(surface, (self.position-self.radius).xy())

class PheromoneMap:
    def __init__(self):
        self.home_pheromones = []
        self.food_pheromones = []
        self.pheromone_dispersion = pheromone_step
        self.radius = 2

    def ErasePheromone(self,screen, showFoodTrail, showHomeTrail):
        # update pheromones and render
        # remove pheromone if it equal or inferior to zero
        for pher in self.food_pheromones:
            pher.Update()
            if pher.strength <= 0:
                self.food_pheromones.remove(pher)
            pher.Show(screen, showFoodTrail, showHomeTrail)
        for pher in self.home_pheromones:
            pher.Update()
            if pher.strength <= 0:
                self.home_pheromones.remove(pher)
            pher.Show(screen, showFoodTrail, showHomeTrail)

    def AppendPheromone(self, position, direction, pher_type="food"):
        # Add pheromone based on it type(food or home)
        pher = Pheromone(position.Copy(), direction.Copy(), pher_type)
        selected_index = 0
        if pher_type.lower() == "food":
            selected_index = 0
        elif pher_type.lower() == "home":
            selected_index = 1

        if selected_index == 0:
            for i in range(len(self.food_pheromones)):
                    # if pheromone is within the range of the other
                    # then Merge the two pheromone
                    if Vector.WithinRange(self.food_pheromones[i].position, pher.position, self.pheromone_dispersion):
                        self.food_pheromones[i].Combine(pher)
                        return
            self.food_pheromones.append(pher)
        elif selected_index == 1:
            for i in range(len(self.home_pheromones)):
                # if pheromone is within the range of the other
                # then Merge the two pheromone
                    if Vector.WithinRange(self.home_pheromones[i].position, pher.position, self.pheromone_dispersion):
                        self.home_pheromones[i].Combine(pher)
                        return
            self.home_pheromones.append(pher)

    def PheromoneDirection(self, position, range_offset, pher_type="food"):
        # Get the Direction
        pher_directions = []

        selected_index = 0
        if pher_type.lower() == "food":
            selected_index = 0
        elif pher_type.lower() == "home":
            selected_index = 1

        if selected_index == 0:
            for i in range(len(self.food_pheromones)):
                if Vector.WithinRange(self.food_pheromones[i].position, position, range_offset):
                    pher_directions.append(self.food_pheromones[i].direction)
        elif selected_index == 1:
            for i in range(len(self.home_pheromones)):
                if Vector.WithinRange(self.home_pheromones[i].position, position, range_offset):
                    pher_directions.append(self.home_pheromones[i].direction)
        # print(Vector.Average(pher_directions))
        return Vector.Average(pher_directions)

    def Update(self,screen, showFoodTrail, showHomeTrail):
        self.ErasePheromone(screen, showFoodTrail=showFoodTrail, showHomeTrail=showHomeTrail)
