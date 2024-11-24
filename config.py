import arcade.color

# Window settings
WIDTH = HEIGHT = 800

# Simulation parameters
ANT_COUNT = 10
FOOD_STOCK_COUNT = 3
ANT_SIZE = 10
NEST_RADIUS = 45

# Pheromone settings
PHEROMONE_INITIAL_STRENGTH = 100
EVO_HOME_RATE = 0.05
EVO_FOOD_RATE = 0.02

# Optimization parameters
GRID_CELL_SIZE = 50
PHEROMONE_MERGE_DISTANCE = 10
RENDER_DISTANCE = 400

# Colors (use arcade colors directly)
NEST_COLOR = arcade.color.BLUE
FOOD_COLOR = arcade.color.ORANGE
ANT_COLOR = arcade.color.WHITE

# Food settings
FOOD_INITIAL_STOCK = 25
FOOD_BITE_SIZE = 1
