import arcade
from config import *
from random import randint
from vector import Vector
from sprite_base import VectorSprite

class FoodSprite(VectorSprite):
    def __init__(self, position):
        super().__init__()
        self.vector_pos = position  # Store Vector for calculations
        self.center_x = position.x  # Use x,y components for arcade sprite
        self.center_y = position.y
        self.stock = FOOD_INITIAL_STOCK
        self.bite_size = FOOD_BITE_SIZE
        self.color = FOOD_COLOR
        self.min_size = FOOD_MIN_SIZE  # Use constant from config.py
        self._create_food_texture()
        
    @property
    def position(self):
        return self.vector_pos
        
    def _create_food_texture(self):
        size = max(self.min_size, self.stock + 5)  # Ensure minimum size
        texture = arcade.make_circle_texture(size, self.color)
        self.texture = texture
        
    def Bite(self):
        self.stock = max(0, self.stock - self.bite_size)  # Prevent negative stock
        self._create_food_texture()  # Update size
        
    def draw(self):
        if self.stock > 0:
            super().draw()
            # Make food count more visible
            arcade.draw_text(
                str(self.stock),
                self.center_x,
                self.center_y,
                arcade.color.BLACK,  # Change to black for better contrast
                16,  # Larger font size
                anchor_x="center",
                anchor_y="center",
                bold=True  # Make text bold
            )

class FoodMap:
    def __init__(self, food_stock):
        self.size = food_stock
        self.foods = arcade.SpriteList()
        self._spatial_hash = {}  # Add spatial hashing
        self._cell_size = 50
        self.InitializeFood()

    def _get_cell(self, position):
        return (int(position.x / self._cell_size), 
                int(position.y / self._cell_size))
                
    def InitializeFood(self):
        screen_offset = 30
        for _ in range(self.size):
            pos = Vector(
                randint(screen_offset, WIDTH - screen_offset),
                randint(screen_offset, HEIGHT - screen_offset)
            )
            food = FoodSprite(pos)
            self.foods.append(food)
            cell = self._get_cell(food.position)
            if cell not in self._spatial_hash:
                self._spatial_hash[cell] = []
            self._spatial_hash[cell].append(food)

    def Update(self):
        for food in self.foods[:]:  # Create a copy of list for safe iteration
            if food.stock <= 0:
                food.remove_from_sprite_lists()

    def GetClosestFood(self, position):
        if not self.foods:  # Handle empty food list
            return None
            
        cell = self._get_cell(position)
        search_cells = [
            (cell[0] + dx, cell[1] + dy)
            for dx, dy in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
        ]
        
        closest_food = None
        closest_distance = float('inf')
        
        for cell in search_cells:
            if cell in self._spatial_hash:
                for food in self._spatial_hash[cell]:
                    if food.stock <= 0:
                        continue
                    dist = Vector.GetDistanceSQ(position, food.position)
                    if dist < closest_distance:
                        closest_food = food
                        closest_distance = dist
                        
        return closest_food

    def draw(self):
        self.foods.draw()
