import pygame
from config import *
from vector import Vector
from math import pi, degrees, radians
import random

class Ant:
    def __init__(self, position=Vector(), nest=None):
        self.position = position
        self.velocity = Vector()
        self.max_speed = 3
        self.trigger_radius = 10
        self.smell_radius = 30
        self.scavenger = Scavenger()
        self.nest = nest
        # angle in radiant
        self.angle = -self.velocity.Heading()
        self.color = white
        self.has_food = False
        self.isFollowingTrail = False

    def ReturnToNest(self, pheromone):
        if Vector.WithinRange(self.position, self.nest.position, self.nest.radius):
            self.has_food = False
            self.nest.stock += 1
            self.color = white
            print(f"Ant returned to nest. Stock: {self.nest.stock}")
            return
        self.velocity += self.scavenger.Seek(self.position, self.nest.position, self.velocity, self.max_speed)
        # add some randomness to have some more realistic movement
        wander_force = self.scavenger.Wander(self.velocity)
        self.velocity += (wander_force * 0.5)
        pher_direction = self.velocity.Negate()

        pheromone.AppendPheromone(self.position, pher_direction ,"food")
        print(f"Ant at {self.position} is returning to nest and depositing 'food' pheromone.")

    def SearchForFood(self, closest_food, pheromone):
        dist = Vector.GetDistance(self.position, closest_food.position)

        if dist < self.trigger_radius:
            self.TakeFood(closest_food)
        elif dist < self.smell_radius:
            self.Step(closest_food, pheromone)
        else:
            self.FollowPheromoneOrWander(pheromone)

        pheromone.AppendPheromone(self.position, self.velocity, "home")
        print(f"Ant at {self.position} is searching for food and depositing 'home' pheromone.")

    def UpdateVelocity(self, closest_food, pheromone):
        if self.has_food == True:
            self.ReturnToNest(pheromone)
        else:
            self.SearchForFood(closest_food, pheromone)


    def TakeFood(self, closest_food):
        self.has_food = True
        self.isFollowingTrail = False
        self.color = (220, 130 , 30)
        closest_food.Bite()

    def Step(self, closest_food, pheromone):
        self.velocity += self.scavenger.Seek(self.position, closest_food.position, self.velocity, self.max_speed)

    def FollowPheromoneOrWander(self, pheromone):
        pheromone_direction = pheromone.PheromoneDirection(self.position, self.smell_radius, "food")
        pheromone_direction = pheromone_direction.Scale(self.max_speed)
        self.velocity = pheromone_direction
        self.velocity += self.scavenger.Wander(self.velocity)
        # Optionally, ensure pheromones are being appended here if needed
        # pheromone.AppendPheromone(self.position, self.velocity, "home")

    def Update(self, foods, pheromones, dt):
        closest_food = foods.GetClosestFood(self.position)
        self.UpdateVelocity(closest_food, pheromones)
        self.velocity = self.velocity.Scale(self.max_speed)
        # self.position += self.velocity.Normalize()  * dt * self.max_speed
        self.position += self.velocity
        self.angle = self.velocity.Heading()


    def Show(self, screen):
        # initialize triangle point
        # rotate point based on the angle
        triangle = [
            ( self.position + Vector(ant_size//2, 0).Rotate(self.angle) ).xy(),
            ( self.position - Vector(ant_size//2, - ant_size/3).Rotate(self.angle) ).xy(),
            ( self.position - Vector(ant_size//2, + ant_size/3).Rotate(self.angle) ).xy()
        ]
        if self.has_food:
            pygame.draw.circle(screen, (220, 130 , 30), (self.position + Vector(ant_size/1.5, 0).Rotate(self.angle)).xy(), 2 )

        pygame.draw.polygon(screen, self.color, triangle)

class Scavenger:
    def __init__(self):
        self.wander_distance = 20
        self.wander_radius = 10
        self.wander_angle = 1
        self.wander_delta_angle = pi/4

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
