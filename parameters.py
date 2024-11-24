width = 800
height = 800
resolution = (width, height)

ant_count = 10
food_stock_count = 3

pheromone_step = 1

# Adjust evaporation rates for smoother fading
evo_home_rate = 0.05  # Reduced from 0.8
evo_food_rate = 0.02  # Reduced from 0.1

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

ant_size = 10

# Performance parameters
GRID_CELL_SIZE = 50
MAX_PHEROMONES_PER_CELL = 50
PHEROMONE_MERGE_DISTANCE = 10  # Increased from 5 to 10 for more merging
RENDER_DISTANCE = 400  # Only render pheromones within this distance of screen center

# Optimization flags
USE_SPATIAL_HASH = True
BATCH_RENDER = True
