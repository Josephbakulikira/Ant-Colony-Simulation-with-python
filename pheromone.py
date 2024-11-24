import arcade
from config import *
from vector import Vector

class PheromoneParticle(arcade.SpriteCircle):
    def __init__(self, position, direction, type="Food"):
        color = arcade.color.GREEN if type == "food" else arcade.color.PURPLE
        super().__init__(2, color, soft=True)
        
        # Store vector position separately
        self.vector_pos = position  # Keep Vector for calculations
        # Set arcade sprite position using components
        self.center_x = position.x
        self.center_y = position.y
        self.direction = direction
        self.strength = PHEROMONE_INITIAL_STRENGTH
        self.type = type
        
    @property
    def position(self):
        return self.vector_pos
        
    def update(self):
        rate = EVO_FOOD_RATE if self.type == "food" else EVO_HOME_RATE
        self.strength -= rate
        self.alpha = int(self.strength * 2.55)  # Scale 0-100 to 0-255

class PheromoneSystem:
    def __init__(self):
        self.food_particles = arcade.SpriteList(use_spatial_hash=True)
        self.home_particles = arcade.SpriteList(use_spatial_hash=True)
        
    def append_pheromone(self, position, direction, pher_type="food"):
        particle = PheromoneParticle(position, direction, pher_type)
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
        pher_directions = []
        particles = self.food_particles if pher_type.lower() == "food" else self.home_particles
        
        # Check nearby pheromones
        for particle in particles:
            if Vector.WithinRange(position, particle.position, range_offset):
                pher_directions.append(particle.direction)
                    
        return Vector.Average(pher_directions) if pher_directions else Vector()

