import arcade
from config import *
from vector import Vector
from sprite_base import VectorSprite
import math

class PheromoneParticle(VectorSprite):
    def __init__(self, position, direction, type="food"):
        base_color = PHEROMONE_FOOD_COLOR if type == "food" else PHEROMONE_HOME_COLOR
        color = (*base_color, 255)  # Start fully opaque
        super().__init__()
        
        # Create texture with initial alpha
        texture = arcade.make_circle_texture(8, color)
        self.texture = texture
        self.alpha = 255
        
        # Set up hit box for circular shape
        radius = 3  # Increased from 2
        self.set_hit_box([(radius * math.cos(angle), radius * math.sin(angle)) 
                         for angle in [0, math.pi/2, math.pi, 3*math.pi/2]])
        
        # Initialize other properties
        self.position = position
        self.direction = direction
        self.type = type
        self.strength = PHEROMONE_INITIAL_STRENGTH
        self.alpha = 255  # Start fully visible

    def update(self):
        rate = EVO_FOOD_RATE if self.type == "food" else EVO_HOME_RATE
        self.strength -= rate
        if self.strength <= 0:
            self.strength = 0
        # Calculate new alpha value
        new_alpha = int((self.strength / PHEROMONE_INITIAL_STRENGTH) * 255)
        # Update sprite's alpha
        self.alpha = new_alpha
        # Update sprite's color to include new alpha
        base_color = PHEROMONE_FOOD_COLOR if self.type == "food" else PHEROMONE_HOME_COLOR
        self.color = (*base_color, new_alpha)
        # No need to call self.set_alpha(new_alpha)

class PheromoneSystem:
    def __init__(self):
        self.particles = {
            "food": arcade.SpriteList(use_spatial_hash=True),
            "home": arcade.SpriteList(use_spatial_hash=True)
        }
        self.grid = {}
        self.grid_size = GRID_CELL_SIZE
        self._cache = {}  # Add direction cache
        self._cache_lifetime = 5  # Cache lifetime in frames
        self._frame_counter = 0
        
    def append_pheromone(self, position, direction, type="food"):
        grid_pos = self._get_grid_pos(position)
        for particle in self.grid.get(grid_pos, []):
            if Vector.GetDistanceSQ(position, particle.position) < PHEROMONE_MERGE_DISTANCE ** 2:
                # Strengthen existing particle
                particle.strength = PHEROMONE_INITIAL_STRENGTH
                particle.direction = (particle.direction + direction).Normalize()
                return  # Skip adding a new particle
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

    def _remove_from_grid(self, particle):
        grid_pos = self._get_grid_pos(particle.position)
        if grid_pos in self.grid and particle in self.grid[grid_pos]:
            self.grid[grid_pos].remove(particle)
            if not self.grid[grid_pos]:
                del self.grid[grid_pos]
        
    def update(self):
        self._frame_counter += 1
        if self._frame_counter >= self._cache_lifetime:
            self._cache.clear()
            self._frame_counter = 0
            
        for particles in self.particles.values():
            for p in particles[:]:  # Iterate over a copy to avoid modification issues
                p.update()
                if p.strength <= 0:
                    self._remove_from_grid(p)
                    p.remove_from_sprite_lists()
                    
    def draw(self, show_food=True, show_home=True):
        if show_home:
            self.particles["home"].draw()
        if show_food:
            self.particles["food"].draw()
            
    def PheromoneDirection(self, position, range_offset, pher_type="food"):
        cache_key = (int(position.x), int(position.y), pher_type)
        if cache_key in self._cache:
            return self._cache[cache_key]
            
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
                            
        result = Vector.Average(pher_directions) if pher_directions else Vector()
        self._cache[cache_key] = result
        return result

