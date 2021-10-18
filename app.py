import string

import pygame as pg

from src.numbers import SlotNumber


class Sudoku:
    def __init__(self):
        self.width = 500
        self.height = 600

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

    def raise_message(self, message):
        font = pg.font.SysFont("arial", 20)
        text = font.render(f"{message}", True, "black")
        self.screen.blit(text, (5, self.width + 6))

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
        ranges = [[i.num for i in self.field[self.x]]]

        tmp = []
        for s in self.field:
            tmp.append(s[self.y].num)

        ranges.append(tmp)

        tmp = []
        for s in range(3):
            for d in range(3):
                tmp.append(self.field[self.x // 3 * 3 + d][self.y // 3 * 3 + s].num)

        ranges.append(tmp)

        return ranges

    def valid(self, invalids, val):
        for i in invalids:
            if str(val) in i:
                return False

        if self.field[self.x][self.y].base:
            return False

        return True

    def run(self):
        self.draw()
        pg.display.flip()

        run = True
        while run:
            self.screen.fill("white")
            self.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.pos_rect()
                    print(f"click on:\tx:{self.x}\ty:{self.y}")
                    print(f"Invalids:\t {self.invalid()}")
                if event.type == pg.KEYDOWN:
                    invalids = self.invalid()
                    value = '0'
                    if event.key == pg.K_1:
                        value = '1'
                    elif event.key == pg.K_2:
                        value = '2'
                    elif event.key == pg.K_3:
                        value = '3'
                    elif event.key == pg.K_4:
                        value = '4'
                    elif event.key == pg.K_5:
                        value = '5'
                    elif event.key == pg.K_6:
                        value = '6'
                    elif event.key == pg.K_7:
                        value = '7'
                    elif event.key == pg.K_8:
                        value = '8'
                    elif event.key == pg.K_9:
                        value = '9'

                    is_valid = self.valid(invalids, value)
                    print("Value is:\t", is_valid)

                    if is_valid:
                        self.field[self.x][self.y] = SlotNumber(value, False)

            if self.game_won():
                self.raise_message("Game Won!")
            self.select_box()
            pg.display.update()


if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.run()
