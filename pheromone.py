from config import *
import pygame
from vector import Vector
from math import ceil
from collections import defaultdict
import numpy as np

def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

class Pheromone:
    def __init__(self, position, direction, type="Food"):
        self.position = position
        self.direction = direction
        self.strength = PHEROMONE_INITIAL_STRENGTH
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

        self.strength = max(self.strength, 0)

    def Combine(self, other):
        if not isinstance(other, Pheromone):
            return
        average_position = Vector.Average([self.position, other.position])
        average_direction = Vector.Average([self.direction, other.direction])

        new_strength = min(self.strength + other.strength, self.max_strength)

        self.position = average_position
        self.direction = average_direction
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
                # Use additive blending to prevent blinking
                screen.blit(surface, (self.position - self.radius).xy(), special_flags=pygame.BLEND_ADD)
        if showHomeTrail:
            if self.type == "home":
                # alpha = int(translateValue(self.strength, 0, 100, 0, 4))
                # pygame.draw.circle(screen, (125, 55, 252), self.position.xy(), alpha)
                val = max(self.strength, 1)
                alpha = int(translateValue(val, 0, 100, 1, 255))
                r, g, b = (125, 55, 252)
                surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
                pygame.draw.circle(surface, (r, g, b, alpha), (self.radius, self.radius), self.radius)
                # Use additive blending to prevent blinking
                screen.blit(surface, (self.position - self.radius).xy(), special_flags=pygame.BLEND_ADD)

class PheromoneMap:
    def __init__(self):
        self.cell_size = 50  # Size of spatial hash cells
        self.food_grid = defaultdict(list)
        self.home_grid = defaultdict(list)
        self.active_cells = set()  # Track only cells with pheromones
        self.pheromone_dispersion = PHEROMONE_MERGE_DISTANCE  # Changed from pheromone_step to PHEROMONE_MERGE_DISTANCE
        self.radius = 4  # Increased from 2 to 4 for better visibility

    def _get_cell(self, pos):
        return (int(pos.x / self.cell_size), int(pos.y / self.cell_size))
    
    def _get_nearby_cells(self, pos, range_offset):
        center_cell = self._get_cell(pos)
        cells_range = int(range_offset / self.cell_size) + 1
        for dx in range(-cells_range, cells_range + 1):
            for dy in range(-cells_range, cells_range + 1):
                yield (center_cell[0] + dx, center_cell[1] + dy)

    def AppendPheromone(self, position, direction, pher_type="food"):
        cell = self._get_cell(position)
        grid = self.food_grid if pher_type.lower() == "food" else self.home_grid
        self.active_cells.add(cell)
        
        # Check nearby cells for merging
        for check_cell in self._get_nearby_cells(position, self.pheromone_dispersion):
            for p in grid[check_cell]:
                if Vector.WithinRange(p.position, position, self.pheromone_dispersion):
                    p.Combine(Pheromone(position, direction, pher_type))
                    return
                        
        # Add new pheromone if no merge
        new_pher = Pheromone(position, direction, pher_type)
        grid[cell].append(new_pher)

    def PheromoneDirection(self, position, range_offset, pher_type="food"):
        pher_directions = []
        grid = self.food_grid if pher_type.lower() == "food" else self.home_grid
        
        # Check pheromones in nearby cells
        for cell in self._get_nearby_cells(position, range_offset):
            for p in grid[cell]:
                if Vector.WithinRange(p.position, position, range_offset):
                    pher_directions.append(p.direction)
                    
        return Vector.Average(pher_directions)

    def Update(self, screen, showFoodTrail, showHomeTrail):
        # Update both grids
        dead_cells = set()
        
        for grid_type, grid in [("food", self.food_grid), ("home", self.home_grid)]:
            show_trail = showFoodTrail if grid_type == "food" else showHomeTrail
            
            for cell in list(self.active_cells):
                pheromones = grid[cell]
                live_pheromones = []
                
                for p in pheromones:
                    p.Update()
                    if p.strength > 0:
                        live_pheromones.append(p)
                        if show_trail:
                            p.Show(screen, showFoodTrail, showHomeTrail)
                
                if live_pheromones:
                    grid[cell] = live_pheromones
                else:
                    dead_cells.add(cell)
                    del grid[cell]
        
        # Remove empty cells
        self.active_cells -= dead_cells

