import arcade
from config import *
from random import randint
from vector import Vector

class FoodSprite(arcade.Sprite):
    def __init__(self, position):
        super().__init__()
        self.vector_pos = position  # Store Vector for calculations
        self.center_x = position.x  # Use x,y components for arcade sprite
        self.center_y = position.y
        self.stock = FOOD_INITIAL_STOCK
        self.bite_size = FOOD_BITE_SIZE
        self.color = FOOD_COLOR
        self._create_food_texture()
        
    @property
    def position(self):
        return self.vector_pos
        
    def _create_food_texture(self):
        size = self.stock + 5
        texture = arcade.make_circle_texture(size, self.color)
        self.texture = texture
        
    def Bite(self):
        self.stock -= self.bite_size
        self._create_food_texture()  # Update size
        
    # Remove GetPosition method since we now use position property
        
    def draw(self):
        if self.stock > 0:
            super().draw()
            arcade.draw_text(
                str(self.stock),
                self.center_x,
                self.center_y,
                arcade.color.WHITE,
                12,
                anchor_x="center",
                anchor_y="center"
            )

class FoodMap:
    def __init__(self, food_stock):
        self.size = food_stock
        self.foods = arcade.SpriteList()
        self.InitializeFood()

    def InitializeFood(self):
        screen_offset = 30
        for _ in range(self.size):
            pos = Vector(
                randint(screen_offset, WIDTH - screen_offset),
                randint(screen_offset, HEIGHT - screen_offset)
            )
            food = FoodSprite(pos)
            self.foods.append(food)

    def Update(self):
        for food in self.foods[:]:  # Create a copy of list for safe iteration
            if food.stock <= 0:
                food.remove_from_sprite_lists()

    def GetClosestFood(self, position):
        if not self.foods:  # Handle empty food list
            return None
            
        closest_food = self.foods[0]
        closest_distance = Vector.GetDistanceSQ(position, closest_food.position)
        
        for food in self.foods[1:]:
            temp_distance = Vector.GetDistanceSQ(position, food.position)
            if temp_distance < closest_distance:
                closest_food = food
                closest_distance = temp_distance
                
        return closest_food

    def draw(self):
        self.foods.draw()
