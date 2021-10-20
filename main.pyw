import json
import visualize
import os

dirname = os.path.dirname(__file__)
conf_path = dirname + r"\work_files\config.json"

# Parse json
with open(conf_path, "r") as f:
    config = json.load(f)

# Get settings
cell_color = tuple(config["color_cells"])
bg_color = tuple(config["color_bg"])
food_color = tuple(config["food_color"])
r, c = config["dimensions"]
width, height = config["screen_size"]
speed = config["speed"]

# run game
game = visualize.SnakeVisualize(r, c, speed, bg_color, cell_color, food_color, width, height)
game.run()