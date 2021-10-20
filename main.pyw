import json
import visualize


# Parse json
with open("config.json", "r") as f:
    config = json.load(f)

cell_color = tuple(config["color_cells"])
bg_color = tuple(config["color_bg"])
food_color = tuple(config["food_color"])
r, c = config["dimensions"]
width, height = config["screen_size"]
speed = config["speed"]

game = visualize.SnakeVisualize(r, c, speed, bg_color, cell_color, food_color, width, height)
game.run()