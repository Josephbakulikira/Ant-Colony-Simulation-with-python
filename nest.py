import arcade
from vector import Vector
from config import *
from ant import AntSprite
from sprite_base import VectorSprite

class NestSprite(arcade.SpriteSolidColor):
    def __init__(self, position, n_ants=ANT_COUNT):
        super().__init__(NEST_RADIUS * 2, NEST_RADIUS * 2, NEST_COLOR)
        
        self.vector_pos = position
        self.center_x = position.x
        self.center_y = position.y
        self.n_ants = n_ants
        self.radius = NEST_RADIUS
        self.stock = 0
        self.ants = arcade.SpriteList()
        self.InitializeAnts()
        
    @property
    def position(self):
        return self.vector_pos
        
    def InitializeAnts(self):
        ants = [AntSprite(self.vector_pos, self) for _ in range(self.n_ants)]
        for ant in ants:
            self.ants.append(ant)
    
    def Update(self, foods, pheromones, dt):
        for ant in self.ants:
            ant.update(foods, pheromones, dt)
            # boundary wrapping
            pos = ant.position
            if pos.x < 0:
                ant.position = Vector(WIDTH, pos.y)
            elif pos.x > WIDTH:
                ant.position = Vector(0, pos.y)
            if pos.y < 0:
                ant.position = Vector(pos.x, HEIGHT)
            elif pos.y > HEIGHT:
                ant.position = Vector(pos.x, 0)
        
    def draw(self):
        super().draw()
        # Draw stock count
        arcade.draw_text(
            str(self.stock),
            self.center_x,
            self.center_y,
            arcade.color.WHITE,
            35,
            anchor_x="center",
            anchor_y="center"
        )
