import arcade
import PIL.Image
import PIL.ImageDraw
from vector import Vector
from config import *  # Import config for any constants needed

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

    @staticmethod
    def create_triangular_texture(size, color):
        # Convert arcade color to RGBA
        if isinstance(color, (tuple, list)):
            rgba_color = color if len(color) == 4 else (*color, 255)
        else:
            rgba_color = (255, 255, 255, 255)  # Default white
            
        image = PIL.Image.new('RGBA', (int(size), int(size)), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        points = [(size/2, 0), (0, size), (size, size)]
        draw.polygon(points, fill=rgba_color)
        image = image.resize((int(size * 2), int(size * 2)), PIL.Image.ANTIALIAS)  # Anti-aliasing
        return arcade.Texture(f"triangle_{size}", image)

    @staticmethod
    def create_circular_texture(size, color):
        image = PIL.Image.new('RGBA', (int(size), int(size)), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.ellipse([0, 0, size, size], fill=color)
        image = image.resize((int(size * 2), int(size * 2)), PIL.Image.ANTIALIAS)  # Anti-aliasing
        return arcade.Texture(f"circle_{size}", image)