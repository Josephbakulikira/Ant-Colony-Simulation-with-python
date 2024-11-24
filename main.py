import arcade
from config import *
from colony import Colony

class AntColonyWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Ant Colony Simulation")
        
        arcade.set_background_color(arcade.color.BLACK)
        self.colony = None
        self.show_pheromone_food = True
        self.show_pheromone_home = True
        self.paused = False
        
    def setup(self):
        self.colony = Colony()
        
    def on_draw(self):
        self.clear()
        if self.colony:
            self.colony.draw()
            
    def on_update(self, delta_time):
        if not self.paused and self.colony:
            self.colony.update(delta_time, self.show_pheromone_food, self.show_pheromone_home)
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.F:
            self.show_pheromone_food = not self.show_pheromone_food
        elif key == arcade.key.H:
            self.show_pheromone_home = not self.show_pheromone_home
        elif key == arcade.key.SPACE:
            self.paused = not self.paused

def main():
    window = AntColonyWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
