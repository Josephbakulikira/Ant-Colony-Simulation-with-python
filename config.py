import arcade.color
import math  # Add this import

# Window settings
WIDTH = HEIGHT = 800

# Game entities
ANT_COUNT = 100
ANT_SIZE = 3  # Reduced from 10
FOOD_STOCK_COUNT = 10
FOOD_INITIAL_STOCK = 25
FOOD_BITE_SIZE = 1
NEST_RADIUS = 45

# Pheromone settings
PHEROMONE_INITIAL_STRENGTH = 100  # Reduced initial strength
PHEROMONE_MERGE_DISTANCE = 20     # Increased merge distance
GRID_CELL_SIZE = 50
EVO_HOME_RATE = 1.0               # Increased evaporation rate
EVO_FOOD_RATE = 0.5               # Increased evaporation rate

# Performance settings
SPATIAL_HASH_CELL_SIZE = 50
CACHE_LIFETIME = 5
MAX_VECTOR_CACHE = 2048
PHEROMONE_UPDATE_RATE = 2  # Update every N frames

# Colors
NEST_COLOR = arcade.color.DARK_BLUE
FOOD_COLOR = arcade.color.GOLD
ANT_COLOR = arcade.color.LIGHT_GRAY
PHEROMONE_FOOD_COLOR = (0, 255, 0)       # Green without alpha
PHEROMONE_HOME_COLOR = (0, 191, 255)     # Blue without alpha

# Scavenger settings
WANDER_DISTANCE = 20
WANDER_RADIUS = 10
WANDER_ANGLE = 1
WANDER_DELTA_ANGLE = math.pi / 4

# Food settings
FOOD_MIN_SIZE = 5
