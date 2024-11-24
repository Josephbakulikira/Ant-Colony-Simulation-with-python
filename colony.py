from config import *
from nest import NestSprite
from food import FoodMap
from pheromone import PheromoneSystem
from vector import Vector

class Colony:
    def __init__(self):
        center_pos = Vector(WIDTH//2, HEIGHT//2)
        self.nest = NestSprite(center_pos, ANT_COUNT)
        self.food = FoodMap(FOOD_STOCK_COUNT)
        self.pheromone = PheromoneSystem()

    def update(self, delta_time, showFoodTrail, showHomeTrail):
        self.nest.Update(self.food, self.pheromone, delta_time)
        self.food.Update()
        self.pheromone.update()

    def draw(self):
        self.food.draw()
        self.pheromone.draw()
        self.nest.draw()
