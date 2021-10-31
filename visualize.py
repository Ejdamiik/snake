import pygame as pg
import sys
import snake
import time
import os
import file_handle
from pygame.locals import *
from typing import Optional, List, Tuple



class SnakeVisualize:

    def __init__(self,
        r: int,
        c: int,
        speed: int,
        bg_color: Tuple,
        cell_color: Tuple,
        food_color: Tuple,
        width = 400,
        height = 400) -> None:
        """
        r - count of rows
        c - count of columns
        speed - speed of refreshing (ms)
        """

        # Loading current best
        dirname = os.path.dirname(__file__)
        self.best_path = dirname + r"\work_files\best.txt"

        self.best = int(file_handle.get_content(self.best_path))

        self.score = 0

        self.width = width
        self.height = height

        self.bg_color = bg_color
        self.cell_color = cell_color
        self.food_color = food_color

        self.engine = snake.Snake(r, c)

        # initializing pygame window
        self.fps = 30
        self.CLOCK = pg.time.Clock()

        pg.init()
        self.font = pg.font.Font(None, 32)
        pg.display.set_caption("Snake")

        pg.mixer.music.load(dirname + r"\work_files\eat_sound.mp3")

        self.mrow = len(self.engine.desk)    # count of rows in matrix
        self.mcolumn = len(self.engine.desk[0])  # count of columns in matrix

        self.starting_margin = self.width // self.mrow // 10 # left margin
        self.ending_margin = self.width // self.mrow // 5   # right margin

        self.grid_node_width = self.width // self.mcolumn
        self.grid_node_height = self.height // self.mrow

        self.MOVEEVENT, t = pg.USEREVENT+1, 250 // speed    # doing sth without interaction
        pg.time.set_timer(self.MOVEEVENT, t)

        self.init_screen()


    def init_screen(self):

        LOWER_BAR_HEIGHT = self.height // 5
        LINE_COLOR = self.cell_color
        LINE_THICKNESS = 5

        self.screen = pg.display.set_mode((self.width, self.height + LOWER_BAR_HEIGHT))
        pg.draw.line(self.screen, LINE_COLOR, (0, self.height), (self.width, self.height), LINE_THICKNESS)
        self.show_score()


    def show_score(self):


        MSG = f"Score: {self.score}"
        x_center, y_center = self.screen.get_rect().center
        y_center += self.height // 2


        text = self.font.render(MSG, True, self.cell_color, self.bg_color)
        textRect = text.get_rect(center = (x_center, y_center))
        self.screen.blit(text, textRect)

        pg.display.update()


    def createSquare(self, x: int, y: int, color: Tuple) -> None:
        pg.draw.rect(self.screen, color, [
                     x + self.starting_margin, y + self.starting_margin,
                      self.grid_node_width - self.ending_margin, self.grid_node_height - self.ending_margin])


    def draw_matrix(self, data: List[List[int]]) -> None:


        y = 0  # we start at the top of the screen
        for row in data:
            x = 0  # for every row we start at the left of the screen again
            for item in row:
                if item == 0:   # bg
                    self.createSquare(x, y, self.bg_color)
                elif item == 1: # snake
                    self.createSquare(x, y, self.cell_color)
                else:   # food
                    self.createSquare(x, y, self.food_color)

                x += self.grid_node_width
            y += self.grid_node_height

        pg.display.update()


    def move(self) -> None:

        if self.engine.step() == "Colision":
            return "Colision"

        if self.engine.food_eaten is True:
            pg.mixer.music.play()
            self.score += 1
            self.show_score()

        self.draw_matrix(self.engine.desk)


    # Forbid to go reversed direction
    def up(self) -> None:

    	if self.engine.direction != 2:
        	self.engine.direction = 1


    def down(self) -> None:

    	if self.engine.direction != 1:
        	self.engine.direction = 2


    def left(self) -> None:

    	if self.engine.direction != 4:
        	self.engine.direction = 3


    def right(self) -> None:

    	if self.engine.direction != 3:
        	self.engine.direction = 4

    def ending(self) -> None:

        self.screen.fill(self.bg_color)

        message = f"Your score: {self.score}"

        # If we reached new high score
        if self.score > self.best:
            self.best = self.score
            file_handle.save_content(self.best_path, str(self.best))

        message_best = f"Your current best: {self.best}"

        center = self.screen.get_rect().center

        # Display text
        text = self.font.render(message, True, self.cell_color, self.bg_color)
        textBest = self.font.render(message_best, True, self.cell_color, self.bg_color)
        textRect = text.get_rect(center = center)
        textRectBest = textBest.get_rect(center = (center[0], center[1] + self.height // 3))
        self.screen.blit(text, textRect)
        self.screen.blit(textBest, textRectBest)

        pg.display.update()
        
        # Wait for 5 seconds
        pg.time.wait(5000)

        # Reset game
        self.screen.fill(self.bg_color)
        self.engine = snake.Snake(self.mrow, self.mcolumn)
        self.score = 0
        self.init_screen()


    def run(self) -> None:

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    # Window quit
                    pg.quit()
                    sys.exit()

                if event.type == self.MOVEEVENT:

                    if self.move() == "Colision":

                        self.ending()


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.left()

                elif event.key == pg.K_RIGHT:
                    self.right()

                elif event.key == pg.K_UP:
                    self.up()

                elif event.key == pg.K_DOWN:
                    self.down()


            pg.display.update()
            self.CLOCK.tick(self.fps)
