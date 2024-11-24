from config import *
from vector import *
from nest import *
from pheromone import *
from food import *

class Colony:
    def __init__(self):
        self.nest = Nest(Vector(WIDTH//2, HEIGHT//2), ANT_COUNT)
        self.food = FoodMap(FOOD_STOCK_COUNT)
        self.pheromone = PheromoneMap()

    def Update(self, screen, showFoodTrail, showHomeTrail, delta_time, view_rect=None):
        self.nest.Update(self.food, self.pheromone, delta_time)
        self.food.Update()
        self.pheromone.Update(screen, showFoodTrail, showHomeTrail)

    def Show(self, screen):
        self.nest.Show(screen)
        self.food.Show(screen)
