import arcade.color

WIDTH = 800
HEIGHT = 800
RESOLUTION = (WIDTH, HEIGHT)

# Renamed constants
ANT_COUNT = 10
FOOD_STOCK_COUNT = 3

# Adjust evaporation rates for smoother fading
EVO_HOME_RATE = 0.05  # Reduced from 0.8
EVO_FOOD_RATE = 0.02  # Reduced from 0.1

WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED
BLUE = arcade.color.BLUE
GREEN = arcade.color.GREEN
YELLOW = arcade.color.YELLOW

ANT_SIZE = 10

# Performance parameters
GRID_CELL_SIZE = 50
MAX_PHEROMONES_PER_CELL = 50
PHEROMONE_MERGE_DISTANCE = 10  # Increased from 5 to 10 for more merging
RENDER_DISTANCE = 400  # Only render pheromones within this distance of screen center

# Optimization flags
USE_SPATIAL_HASH = True
BATCH_RENDER = True

PHEROMONE_INITIAL_STRENGTH = 100
ANT_COLOR = arcade.color.WHITE

# New constants
NEST_RADIUS = 45
NEST_COLOR = arcade.color.BLUE

FOOD_INITIAL_STOCK = 25
FOOD_COLOR = arcade.color.ORANGE  # Updated to use arcade color
FOOD_BITE_SIZE = 1

# Remove or comment out the lowercase constants
# pheromone_step = 1
# ant_count = 10
# food_stock_count = 3
