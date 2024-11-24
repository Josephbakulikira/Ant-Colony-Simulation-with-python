import arcade
from config import *
from vector import Vector
from sprite_base import VectorSprite
import math

class PheromoneParticle(VectorSprite):
    def __init__(self, position, direction, type="food"):
        color = arcade.color.GREEN if type == "food" else arcade.color.PURPLE
        super().__init__()
        
        # Fix texture creation - remove 'soft' parameter
        texture = arcade.make_circle_texture(4, color)
        self.texture = texture
        
        # Set up hit box for circular shape
        radius = 2  # Half of texture size
        self.set_hit_box([(radius * math.cos(angle), radius * math.sin(angle)) 
                         for angle in [0, math.pi/2, math.pi, 3*math.pi/2]])
        
        # Initialize other properties
        self.position = position
        self.direction = direction
        self.type = type
        self.strength = PHEROMONE_INITIAL_STRENGTH
        self.alpha = 255

    def update(self):
        rate = EVO_FOOD_RATE if self.type == "food" else EVO_HOME_RATE
        self.strength -= rate
        self.alpha = int(self.strength * 2.55)  # Scale 0-100 to 0-255

class PheromoneSystem:
    def __init__(self):
        self.particles = {"food": arcade.SpriteList(use_spatial_hash=True),
                         "home": arcade.SpriteList(use_spatial_hash=True)}
        self.grid = {}
        self.grid_size = GRID_CELL_SIZE  # Add this initialization
        
    def append_pheromone(self, position, direction, type="food"):
        if self._should_merge(position, type):
            return
            
        particle = PheromoneParticle(position, direction, type)
        self.particles[type].append(particle)
        self._add_to_grid(particle)
        
    def _should_merge(self, position, type):
        grid_pos = self._get_grid_pos(position)
        return any(Vector.GetDistance(position, p.position) < PHEROMONE_MERGE_DISTANCE 
                  for p in self.grid.get(grid_pos, []))
                  
    def _get_grid_pos(self, pos):
        return (int(pos.x / self.grid_size), int(pos.y / self.grid_size))
        
    def _add_to_grid(self, particle):
        grid_pos = self._get_grid_pos(particle.position)
        if grid_pos not in self.grid:
            self.grid[grid_pos] = []
        self.grid[grid_pos].append(particle)
        
    def update(self):
        for particles in self.particles.values():
            for p in particles:
                p.update()
                if p.strength <= 0:
                    p.remove_from_sprite_lists()
                    
    def draw(self, show_food=True, show_home=True):
        if show_food:
            self.particles["food"].draw()
        if show_home:
            self.particles["home"].draw()
            
    def PheromoneDirection(self, position, range_offset, pher_type="food"):
        grid_pos = self._get_grid_pos(position)
        pher_directions = []
        particles = self.particles[pher_type.lower()]
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_pos = (grid_pos[0] + dx, grid_pos[1] + dy)
                if check_pos in self.grid:
                    for particle in self.grid[check_pos]:
                        if Vector.WithinRange(position, particle.position, range_offset):
                            pher_directions.append(particle.direction)
                            
        return Vector.Average(pher_directions) if pher_directions else Vector()

