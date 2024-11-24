import arcade
from config import *
from vector import Vector
import math
import random
from arcade_utils import create_triangular_texture

class AntSprite(arcade.Sprite):
    def __init__(self, position, nest):
        super().__init__()
        
        # Create ant texture as a triangle shape instead of text
        self.width = ANT_SIZE
        self.height = ANT_SIZE
        self._create_ant_texture()
        
        self.vector_pos = position  # Keep Vector for calculations
        self.center_x = position.x  # Set arcade sprite position
        self.center_y = position.y
        
        self.velocity = Vector()
        self.max_speed = 3
        self.trigger_radius = 10
        self.smell_radius = 30
        self.scavenger = Scavenger()
        self.nest = nest
        self.angle = -self.velocity.Heading()
        self.has_food = False
        self.isFollowingTrail = False
        
        # Position sprite
        self.center_x = position.x
        self.center_y = position.y
        
    @property
    def position(self):
        return self.vector_pos
        
    @position.setter
    def position(self, new_pos):
        self.vector_pos = new_pos
        self.center_x = new_pos.x
        self.center_y = new_pos.y
        
    def _create_ant_texture(self):
        texture_size = max(self.width, self.height)
        image = create_triangular_texture(texture_size, ANT_COLOR)
        self.texture = image
        self.set_hit_box([(-self.width/2, -self.height/2),
                         (0, self.height/2),
                         (self.width/2, -self.height/2)])
        
    def update(self, foods, pheromones, delta_time):
        closest_food = foods.GetClosestFood(self.position)
        self.UpdateVelocity(closest_food, pheromones)
        self.velocity = self.velocity.Scale(self.max_speed)
        
        # Update both vector and sprite positions
        self.vector_pos = self.vector_pos + self.velocity
        self.center_x = self.vector_pos.x
        self.center_y = self.vector_pos.y
        self.angle = math.degrees(self.velocity.Heading())
        
    def ReturnToNest(self, pheromone):
        nest_pos = self.nest.position
        if not isinstance(nest_pos, Vector):
            # Convert tuple to Vector if needed
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

    def SearchForFood(self, closest_food, pheromone):
        dist = Vector.GetDistance(self.position, closest_food.position)
        if dist < self.trigger_radius:
            self.TakeFood(closest_food)
        elif dist < self.smell_radius:
            self.Step(closest_food, pheromone)
        else:
            self.FollowPheromoneOrWander(pheromone)
        pheromone.append_pheromone(self.position, self.velocity, "home")

    def UpdateVelocity(self, closest_food, pheromone):
        if self.has_food == True:
            self.ReturnToNest(pheromone)
        else:
            self.SearchForFood(closest_food, pheromone)

    def TakeFood(self, closest_food):
        self.has_food = True
        self.isFollowingTrail = False
        self.color = FOOD_COLOR
        closest_food.Bite()

    def Step(self, closest_food, pheromone):
        self.velocity += self.scavenger.Seek(self.position, closest_food.position, self.velocity, self.max_speed)

    def FollowPheromoneOrWander(self, pheromone):
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
