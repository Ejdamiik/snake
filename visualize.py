import pygame as pg
import sys
import snake
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
        pg.display.set_caption("Vizualize matrixes")
        self.screen = pg.display.set_mode((self.width, self.height), RESIZABLE)

        self.mrow = len(self.engine.desk)    # count of rows in matrix
        self.mcolumn = len(self.engine.desk[0])  # count of columns in matrix

        self.starting_margin = self.width // self.mrow // 10 # left margin
        self.ending_margin = self.width // self.mrow // 5   # right margin

        self.grid_node_width = self.width // self.mcolumn
        self.grid_node_height = self.height // self.mrow

        self.MOVEEVENT, t = pg.USEREVENT+1, 250 // speed    # doing sth without interaction
        pg.time.set_timer(self.MOVEEVENT, t)



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

        self.draw_matrix(self.engine.desk)


    def up(self) -> None:

        self.engine.direction = 1


    def down(self) -> None:

        self.engine.direction = 2


    def left(self) -> None:

        self.engine.direction = 3


    def right(self) -> None:

        self.engine.direction = 4

    def ending(self) -> None:

        self.screen.fill(self.bg_color)

        message = f"Your score: {len(self.engine.snake)}"

        # Display text
        font = pg.font.Font(None, 32)
        text = font.render(message, True, self.cell_color, self.bg_color)
        textRect = text.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(text, textRect)

        pg.display.update()
        
        time.sleep(5)
        self.screen.fill(self.bg_color)
        self.engine = snake.Snake(self.mrow, self.mcolumn)


    def run(self) -> None:
        """
        Pygame loop : interactive mode
        """
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
