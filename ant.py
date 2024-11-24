import math
import random

from config import *
from sprite_base import VectorSprite
from vector import Vector  # Add this import


class AntSprite(VectorSprite):
    def __init__(self, position, nest):
        super().__init__()
        
        self.has_food = False  # Move this up before using it
        self.width = self.height = ANT_SIZE * 1.5  # Reduced multiplier from 2 to 1.5
        self.color = FOOD_COLOR if self.has_food else ANT_COLOR
        self.alpha = 255  # Ensure full opacity
        self._create_ant_texture()
        self.position = position
        
        self.velocity = Vector()
        self.max_speed = 3
        self.scavenger = Scavenger()  # Add scavenger initialization
        self._setup_sensors()
        self.nest = nest
        self.isFollowingTrail = False  # Add this back
        
    def _setup_sensors(self):
        self.trigger_radius = 10
        self.smell_radius = 30
        self._cached_smell_radius_sq = self.smell_radius ** 2
        self._cached_trigger_radius_sq = self.trigger_radius ** 2
        
    def update(self, foods, pheromones, delta_time):
        self._update_movement(foods, pheromones)
        self._update_position()
        
    def _update_movement(self, foods, pheromones):
        if self.has_food:
            self._return_to_nest(pheromones)
        else:
            self._search_for_food(foods.GetClosestFood(self.position), pheromones)
            
    def _update_position(self):
        self.position = self.position + self.velocity.Scale(self.max_speed)
        self.angle = math.degrees(self.velocity.Heading())
        
    def _create_ant_texture(self):
        texture_size = max(self.width, self.height)
        self.texture = self.create_triangular_texture(texture_size, self.color)
        # Make hitbox slightly smaller than visual size
        hitbox_size = texture_size * 0.8
        self.set_hit_box([
            (-hitbox_size/2, -hitbox_size/2),
            (0, hitbox_size/2),
            (hitbox_size/2, -hitbox_size/2)
        ])
        
    def _return_to_nest(self, pheromone):
        nest_pos = self.nest.position
        if not isinstance(nest_pos, Vector):
            nest_pos = Vector(nest_pos[0], nest_pos[1])
            
        if Vector.WithinRange(self.position, nest_pos, self.nest.radius):
            self.has_food = False
            self.nest.stock += 1
            self.color = ANT_COLOR
            return
            
        self.velocity += self.scavenger.Seek(self.position, nest_pos, self.velocity, self.max_speed)
        wander_force = self.scavenger.Wander(self.velocity)
        self.velocity += (wander_force * 0.5)
        pher_direction = self.velocity.Negate()
        pheromone.append_pheromone(self.position, pher_direction, "food")

    def _search_for_food(self, closest_food, pheromone):
        if not closest_food:
            self._follow_pheromone_or_wander(pheromone)
            return
            
        dist_sq = Vector.GetDistanceSQ(self.position, closest_food.position)
        if dist_sq < self._cached_trigger_radius_sq:
            self._take_food(closest_food)
        elif dist_sq < self._cached_smell_radius_sq:
            self._step(closest_food, pheromone)
        else:
            self._follow_pheromone_or_wander(pheromone)
        pheromone.append_pheromone(self.position, self.velocity, "home")

    def _take_food(self, closest_food):
        self.has_food = True
        self.isFollowingTrail = False
        self.color = FOOD_COLOR
        closest_food.Bite()

    def _step(self, closest_food, pheromone):
        self.velocity += self.scavenger.Seek(self.position, closest_food.position, self.velocity, self.max_speed)

    def _follow_pheromone_or_wander(self, pheromone):
        pheromone_direction = pheromone.PheromoneDirection(self.position, self.smell_radius, "food")
        pheromone_direction = pheromone_direction.Scale(self.max_speed)
        self.velocity = pheromone_direction
        self.velocity += self.scavenger.Wander(self.velocity)

class Scavenger:
    def __init__(self):
        self.wander_distance = 20
        self.wander_radius = 10
        self.wander_angle = 1
        self.wander_delta_angle = math.pi/4

    def Seek(self, position, target, velocity, max_speed):
        diff = target - position
        diff = diff.Scale(max_speed)
        return diff - velocity

    def Wander(self, velocity):
        pos = velocity.Copy()
        pos = pos.Scale(self.wander_distance)
        displacement = Vector(0, -1).Scale(self.wander_radius)
        displacement = displacement.SetAngle(self.wander_angle)
        self.wander_angle += random.uniform(0, 1) * self.wander_delta_angle - self.wander_delta_angle * 0.5
        return pos + displacement
