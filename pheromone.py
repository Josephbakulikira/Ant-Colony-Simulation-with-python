import arcade
from config import *
from vector import Vector

class PheromoneParticle(arcade.SpriteCircle):
    def __init__(self, position, direction, type="Food"):
        color = arcade.color.GREEN if type == "food" else arcade.color.PURPLE
        super().__init__(2, color, soft=True)
        
        self.vector_pos = position
        self.center_x = position.x  # Set arcade sprite position
        self.center_y = position.y
        self.direction = direction
        self.strength = PHEROMONE_INITIAL_STRENGTH
        self.type = type
        
    @property
    def position(self):
        return self.vector_pos
        
    @position.setter
    def position(self, new_pos):
        self.vector_pos = new_pos
        self.center_x = new_pos.x
        self.center_y = new_pos.y
        
    def update(self):
        rate = EVO_FOOD_RATE if self.type == "food" else EVO_HOME_RATE
        self.strength -= rate
        self.alpha = int(self.strength * 2.55)  # Scale 0-100 to 0-255

class PheromoneSystem:
    def __init__(self):
        self.food_particles = arcade.SpriteList(use_spatial_hash=True)
        self.home_particles = arcade.SpriteList(use_spatial_hash=True)
        self.grid_size = GRID_CELL_SIZE
        self.grid = {}  # Spatial hash grid
        
    def _get_grid_pos(self, pos):
        return (int(pos.x / self.grid_size), int(pos.y / self.grid_size))
        
    def append_pheromone(self, position, direction, pher_type="food"):
        grid_pos = self._get_grid_pos(position)
        if grid_pos in self.grid:
            # Merge with existing pheromones if too close
            for p in self.grid[grid_pos]:
                if Vector.GetDistance(position, p.position) < PHEROMONE_MERGE_DISTANCE:
                    p.strength = min(100, p.strength + 20)
                    return
                    
        particle = PheromoneParticle(position, direction, pher_type)
        if grid_pos not in self.grid:
            self.grid[grid_pos] = []
        self.grid[grid_pos].append(particle)
        
        if pher_type == "food":
            self.food_particles.append(particle)
        else:
            self.home_particles.append(particle)
            
    def update(self):
        # Update and remove dead particles
        for particles in [self.food_particles, self.home_particles]:
            for p in particles:
                p.update()
                if p.strength <= 0:
                    p.remove_from_sprite_lists()
                    
    def draw(self, show_food=True, show_home=True):
        if show_food:
            self.food_particles.draw()
        if show_home:
            self.home_particles.draw()
            
    def PheromoneDirection(self, position, range_offset, pher_type="food"):
        """Get average direction from nearby pheromones."""
        grid_pos = self._get_grid_pos(position)
        pher_directions = []
        particles = self.food_particles if pher_type.lower() == "food" else self.home_particles
        
        # Only check neighboring cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_pos = (grid_pos[0] + dx, grid_pos[1] + dy)
                if check_pos in self.grid:
                    for particle in self.grid[check_pos]:
                        if Vector.WithinRange(position, particle.position, range_offset):
                            pher_directions.append(particle.direction)
                            
        return Vector.Average(pher_directions) if pher_directions else Vector()

