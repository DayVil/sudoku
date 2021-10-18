import string
from random import shuffle
import random

import pygame as pg

from src.numbers import SlotNumber


def to_txt(to_grid):
    with open("./puzzle/grid.txt", "w") as f:
        text = ""
        for i in range(9):
            for j in range(9):
                text += to_grid[i][j].num + " "
            text.strip()
            text += "\n"

        cleaned = len(text) - 1
        f.write(text[0:cleaned])


class Sudoku:
    def __init__(self):
        self.HINTS = 18
        self.width = 500
        self.height = 600
        self.path = "./puzzle/field.txt"

        self.x, self.y, self.val = 0, 0, 0
        self.dif = self.width / 9

        self.field = self.parse_sud()

        pg.font.init()
        self.font1 = pg.font.SysFont("arial", 30)

        pg.display.set_caption("Sudoku")
        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(color="white")

    def select_box(self):
        wid = 5
        for i in range(2):
            p_x = self.x * self.dif
            p_y = self.y * self.dif
            dif_i = i * self.dif
            pg.draw.line(self.screen, color="darkorange", start_pos=(p_x + dif_i, p_y),
                         end_pos=(p_x + dif_i, p_y + self.dif), width=wid)
            pg.draw.line(self.screen, color="darkorange", start_pos=(p_x, p_y + dif_i),
                         end_pos=(p_x + self.dif, p_y + dif_i), width=wid)

    def draw(self):
        # Coloring the already existing numbers and placing them.
        for i in range(9):
            for j in range(9):
                dif_i = self.dif * i
                dif_j = self.dif * j
                val = self.field[i][j]
                if val.num != '0':
                    col = val.colour
                    if col:
                        pg.draw.rect(self.screen, col, (dif_i, dif_j, self.dif + 1, self.dif + 1))
                    self.draw_value(val, (dif_i, dif_j))

        # Vertical and horizontal lines
        for i in range(10):
            if i % 3 == 0:
                thick = 5
            else:
                thick = 1

            # Vertical
            pg.draw.line(self.screen, (0, 0, 0), start_pos=(i * self.dif, 0), end_pos=(i * self.dif, self.height),
                         width=thick)
            # Horizontal
            pg.draw.line(self.screen, (0, 0, 0), start_pos=(0, i * self.dif), end_pos=(self.width, i * self.dif),
                         width=thick)

        # For the bottom part
        pg.draw.rect(self.screen, color="white", rect=(0, self.width + 3, self.width, abs(self.height - self.width)))

    def draw_value(self, val, pos):
        text = self.font1.render(f"{val}", True, "black")
        self.screen.blit(text, (pos[0] + self.dif / 2.0 - 6, pos[1] + self.dif / 4.0 - 4))

    def pos_rect(self):
        pos = pg.mouse.get_pos()
        self.x = int(pos[0] // self.dif)
        self.y = int(pos[1] // self.dif)

    def move(self, x, y):
        x_dif = self.x + x
        y_dif = self.y + y

        if 0 <= x_dif <= 8 and 0 <= y_dif <= 8:
            self.x += x
            self.y += y

    def reset_to_default(self):
        print("Resetting....")
        for i in range(9):
            for j in range(9):
                if self.field[i][j].base is False:
                    self.field[i][j] = SlotNumber('0', False)

    def remove_slot(self, force=False):
        if self.field[self.x][self.y].base is False or force:
            self.field[self.x][self.y] = SlotNumber('0', False)

    def raise_message(self, message, y_offset=0):
        font = pg.font.SysFont("arial", 18)
        text = font.render(f"{message}", True, "black")
        self.screen.blit(text, (5, self.width + 6 + y_offset))

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                num = self.field[j][i].num
                if num == '0':
                    return j, i

        return None, None

    def amount_numbers(self):
        count = 0
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num != '0':
                    count += 1
        return count

    def draw_and_update(self):
        self.screen.fill("white")
        self.draw()
        pg.display.update()

    def generate(self):
        list1 = [i for i in range(1, 10)]
        list2 = [str(i) for i in range(1, 10)]

        shuffle(list1)
        shuffle(list2)

        grid = list()
        tmp = []
        for i in list1:
            tmp.append(SlotNumber(i, True))
        grid.append(tmp)

        val = grid[0][0].num
        index = list2.index(val)

        tmp1 = list2[index]
        tmp2 = list2[0]
        list2[index] = tmp2
        list2[0] = tmp1

        for i in range(1, 9):
            tmp = list()
            tmp.append(SlotNumber(list2[i], True))
            for _ in range(1, 9):
                tmp.append(SlotNumber(0, False))
            grid.append(tmp)

        self.field = grid
        if self.solver(0) is False:
            self.generate()
        else:
            to_txt(grid)
            amount = self.amount_numbers()
            while amount >= self.HINTS:
                amount = self.amount_numbers()
                x_ran = random.randint(0, 8)
                y_ran = random.randint(0, 8)
                self.x = x_ran
                self.y = y_ran
                self.remove_slot(True)

                self.draw_and_update()
                pg.time.delay(50)

            to_txt(self.field)
            self.path = "./puzzle/grid.txt"
            self.field = self.parse_sud()

            self.x = 0
            self.y = 0
            self.draw_and_update()

    def solver(self, time):
        i, j = self.find_empty()
        if i is None:
            return True
        self.x = i
        self.y = j
        valids = self.invalid()
        for val in range(1, 10):
            if self.valid(valids, val):
                self.field[i][j] = SlotNumber(str(val), False)
                # Delaying
                if time != 0:
                    self.draw_and_update()
                    pg.time.delay(time)

                if self.solver(time):
                    return True
                self.field[i][j] = SlotNumber('0', False)

        return False

    def parse_sud(self):
        with open(self.path, "r") as f:
            puzzle = f.read()

            parsed = []
            letter = []
            for let in puzzle:
                if let == "\n":
                    parsed.append(letter)
                    letter = list()
                elif let in string.digits:
                    if let != '0':
                        letters = SlotNumber(let, True, "lightcyan")
                    else:
                        letters = SlotNumber(let, False)
                    letter.append(letters)
        parsed.append(letter)
        return parsed

    def game_won(self):
        flat_field = [i.num for row in self.field for i in row]
        if '0' in flat_field:
            return False
        return True

    def invalid(self):
        t_y = self.y
        t_x = self.x
        ranges = [[i.num for i in self.field[t_x]]]

        tmp = []
        for s in self.field:
            tmp.append(s[t_y].num)

        ranges.append(tmp)

        tmp = []
        for s in range(3):
            for d in range(3):
                tmp.append(self.field[t_x // 3 * 3 + d][t_y // 3 * 3 + s].num)

        ranges.append(tmp)

        return ranges

    def valid(self, invalids, val):
        for i in invalids:
            if str(val) in i:
                return False

        if self.field[self.x][self.y].base or val == '0':
            return False

        return True

    def debug(self):
        print(f"click on:\tx:{self.x}\ty:{self.y}")
        print(f"Invalids:\t {self.invalid()}")

    def run(self):
        self.draw()
        pg.display.flip()
        won = False

        run = True
        while run:
            self.screen.fill("white")
            self.draw()
            if won is False:
                self.raise_message("Controls: UP, DOWN, LEFT, numbers from '1' to '9', RETURN/'s' to solve")
                self.raise_message("               't' for grid copy, 'g' to generate a random grid.", 20)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.pos_rect()
                    self.debug()
                if event.type == pg.KEYDOWN:
                    invalids = self.invalid()
                    value = '0'
                    key = event.key
                    if key == pg.K_LEFT:
                        self.move(-1, 0)
                        self.debug()
                    elif key == pg.K_RIGHT:
                        self.move(1, 0)
                        self.debug()
                    elif key == pg.K_UP:
                        self.move(0, -1)
                        self.debug()
                    elif key == pg.K_DOWN:
                        self.move(0, 1)
                        self.debug()
                    elif key == pg.K_1:
                        value = '1'
                    elif key == pg.K_2:
                        value = '2'
                    elif key == pg.K_3:
                        value = '3'
                    elif key == pg.K_4:
                        value = '4'
                    elif key == pg.K_5:
                        value = '5'
                    elif key == pg.K_6:
                        value = '6'
                    elif key == pg.K_7:
                        value = '7'
                    elif key == pg.K_8:
                        value = '8'
                    elif key == pg.K_9:
                        value = '9'
                    elif key == pg.K_BACKSPACE:
                        self.remove_slot()
                    elif key == pg.K_RETURN:
                        self.solver(0)
                    elif key == pg.K_s:
                        self.solver(40)
                    elif key == pg.K_r:
                        self.reset_to_default()
                    elif key == pg.K_t:
                        to_txt(self.field)
                        print("Copied.")
                    elif key == pg.K_g:
                        self.generate()

                    is_valid = self.valid(invalids, value)
                    print("Value is:\t", is_valid)

                    if is_valid:
                        self.field[self.x][self.y] = SlotNumber(value, False)

            if self.game_won():
                won = True
                self.raise_message("Game Won!")
            self.select_box()
            pg.display.update()


if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.run()
