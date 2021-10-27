import random
from typing import List


class Snake:

	def __init__(self, r: int, c: int) -> None:

		self.columns = c
		self.rows = r
		self.desk = [[0 for _ in range(c)] for _ in range(r)]
		self.directions = {
		1: (0, -1),
		2: (0, 1),
		3: (-1, 0),
		4: (1, 0)
		}
		self.food_eaten = False

		self.direction = 1

		# coords of head
		init_x = random.randint(0, r - 1)
		init_y = random.randint(0, c - 1)

		self.spawn_food()

		self.snake = [(init_x, init_y)]

		self.update_desk()


	def step(self):

		"""
		1 - up
		2 - down
		3 - left
		4 - right
		"""

		self.food_eaten = False
		dy, dx = self.directions[self.direction]

		# moving snake
		prev = self.snake[0]
		for i in range(len(self.snake) - 1):
			
			nxt = self.snake[i + 1]
			self.snake[i + 1] = prev
			prev = nxt
			

		x, y = self.snake[0]

		# Boundaries
		if x + dx < 0:
			new_x = len(self.desk[0]) - 1
		elif x + dx > len(self.desk[0]) - 1:
			new_x = 0
		else:
			new_x = dx + x


		# crossing boundaries
		if y + dy < 0:
			new_y = len(self.desk) - 1
		elif y + dy > len(self.desk) - 1:
			new_y = 0
		else:
			new_y = y + dy

		if (new_x, new_y) in self.snake:
			return "Colision"

		self.snake[0] = (new_x, new_y)

		if (new_x, new_y) == (self.food_x, self.food_y):

			self.eat_food()
			self.food_eaten = True

		self.update_desk()


	def update_desk(self):

		self.desk = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

		self.desk[self.food_x][self.food_y] = 2

		for cell in self.snake:
			x, y = cell
			self.desk[x][y] = 1


	def spawn_food(self):

		# What if food spawns at snake ?
		self.food_x = random.randint(0, self.rows - 1)
		self.food_y = random.randint(0, self.columns - 1)


	def eat_food(self):

		last = self.snake[-1]
		x, y = last

		dy, dx = self.directions[self.direction]

		self.snake.append((x + dx, y + dy))
		self.spawn_food()