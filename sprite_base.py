import arcade
from vector import Vector

class VectorSprite(arcade.Sprite):
    def __init__(self, texture=None):
        super().__init__(texture=texture if texture else None)
        self.vector_pos = Vector()
        
    @property
    def position(self):
        return self.vector_pos
        
    @position.setter
    def position(self, new_pos):
        self.vector_pos = new_pos
        self.center_x = new_pos.x
        self.center_y = new_pos.y