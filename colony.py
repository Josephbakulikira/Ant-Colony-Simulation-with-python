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
        self._frame_counter = 0

    def update(self, delta_time, showFoodTrail, showHomeTrail):
        self._frame_counter += 1
        
        self.nest.Update(self.food, self.pheromone, delta_time)
        self.food.Update()
        
        if self._frame_counter % PHEROMONE_UPDATE_RATE == 0:
            self.pheromone.update()
            self._frame_counter = 0

    def draw(self):
        self.food.draw()
        self.nest.draw()
        self.pheromone.draw()  # Draw pheromones after the nest
        self.nest.ants.draw()  # Draw ants on top of pheromones
        self.draw_stats()
        
    def draw_stats(self):
        stats = [
            f"Food Sources: {len(self.food.foods)}",
            f"Food Collected: {self.nest.stock}",
            f"Active Ants: {len(self.nest.ants)}"
        ]
        
        for i, text in enumerate(stats):
            arcade.draw_text(
                text,
                10,
                HEIGHT - 20 * (i + 1),
                arcade.color.WHITE,
                14
            )
