import random
import os
import string

import pygame as pg


class Sudoku:
    def __init__(self):
        self.width = 500
        self.height = 500

        self.x, self.y, self.val = 0, 0, 0
        self.dif = self.width / 9

        self.field = self.parse_sud()

        pg.font.init()
        self.font1 = pg.font.SysFont("arial", 30)

        pg.display.set_caption("Sudoku")
        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(color="white")

    def draw(self):
        # Coloring the already existing numbers and placing them.
        for i in range(9):
            for j in range(9):
                if self.field[i][j] != '0':
                    dif_i = self.dif * i
                    dif_j = self.dif * j
                    pg.draw.rect(self.screen, "lightcyan", (dif_i, dif_j, self.dif + 1, self.dif + 1))

                    self.draw_value(self.field[i][j], (dif_i, dif_j))

        # Vertical and horizontal lines
        for i in range(10):
            if i % 3 == 0:
                thick = 7
            else:
                thick = 1

            # Vertical
            pg.draw.line(self.screen, (0, 0, 0), start_pos=(i * self.dif, 0), end_pos=(i * self.dif, self.height),
                         width=thick)
            # Horizontal
            pg.draw.line(self.screen, (0, 0, 0), start_pos=(0, i * self.dif), end_pos=(self.width, i * self.dif),
                         width=thick)

    def invalid(self, case_x, case_y):
        ranges = [self.field[case_x]]

        tmp = []
        for s in self.field:
            tmp.append(s[case_y])

        ranges.append(tmp)

        tmp = []
        for s in range(3):
            for d in range(3):
                tmp.append(self.field[case_x // 3 * 3 + d][case_y // 3 * 3 + s])

        ranges.append(tmp)

        return ranges

    def draw_value(self, val, pos):
        text = self.font1.render(f"{val}", True, "black")
        self.screen.blit(text, (pos[0] + self.dif / 2.0 - 6, pos[1] + self.dif / 4.0 - 4))

    @staticmethod
    def parse_sud():
        with open("puzzle/field.txt", "r") as f:
            puzzle = f.read()

            parsed = []
            letter = []
            for let in puzzle:
                if let == "\n":
                    parsed.append(letter)
                    letter = list()
                elif let in string.digits:
                    letter.append(let)
        parsed.append(letter)
        return parsed

    def run(self):
        # pg.init()
        self.draw()
        pg.display.flip()

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False


if __name__ == '__main__':
    sudoku = Sudoku()
    print(sudoku.invalid(3, 3))
    sudoku.run()
