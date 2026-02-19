import copy
import itertools
import random

import mouse

import painter as _painter


def get_grid(size: int) -> list[list[int]]:
    return [[0] * (size + 2) for _ in range(size + 2)]


class Game:
    def __init__(self):
        self.size_pole = 300
        self.count_bots = 20
        self.rate_bots = 10
        self.painter = _painter.Painter(
            size_pole=self.size_pole,
            count_bots=self.count_bots,
            time_loop=1_000,
        )
        self.grid = get_grid(self.count_bots)
        self.grid = self.get_random_grid(self.grid)

    def get_random_grid(self, grid: list[list[int]]) -> list[list[int]]:
        for i in range(1, len(grid) - 1):
            for j in range(1, len(grid) - 1):
                grid[i][j] = random.choices(
                    [0, 1],
                    [self.count_bots - self.rate_bots, self.rate_bots],
                )[0]

        return grid

    def sum_neighbors(self, i: int, j: int, grid: list[list[int]]) -> int:
        count = 0
        for di, dj in itertools.product([-1, 0, 1], repeat=2):
            if di == dj == 0:
                continue

            count += grid[i + di][j + dj]

        return count

    def run_main_loop(self) -> None:
        last_grid = copy.deepcopy(self.grid)
        for i in range(1, len(self.grid) - 1):
            for j in range(1, len(self.grid[0]) - 1):
                count = self.sum_neighbors(i, j, last_grid)
                if not self.grid[i][j] and count == 3:
                    self.grid[i][j] = 1
                elif self.grid[i][j] and (count == 2 or count == 3):
                    pass
                else:
                    self.grid[i][j] = 0

                self.add_rules(i, j)

        self.painter.render_pole(self.grid)
        self.painter.starter_fun_in_loop(self.run_main_loop)

    def add_rules(self, i: int, j: int) -> None:
        # rule_1(i, j)
        # rule_1(j, i)
        # rule_2(i, j)
        self.rule_3(i, j)

    def rule_1(self, i: int, j: int) -> None:
        if i % 10 == 0:
            self.grid[i][j] = 0

    def rule_2(self, i: int, j: int) -> None:
        if i == j:
            self.grid[i][j] = 0

    def rule_3(self, i: int, j: int) -> None:
        if (
            i == 1
            or i == len(self.grid) - 2
            or j == 1
            or j == len(self.grid) - 2
        ):
            self.grid[i][j] = 0

    def painted_bot_on_click(self) -> None:
        x, y = mouse.get_position()
        win_x, win_y = self.painter.get_par_win()

        x -= win_x
        y -= win_y
        if 0 <= x < self.painter.size_pole and 0 <= y < self.painter.size_pole:
            x //= self.painter.size_bots
            y //= self.painter.size_bots

            x += 1
            y += 1

            self.grid[y][x] = int(not self.grid[y][x])

            self.painter.render_pole(self.grid)

    def set_base_pole(self) -> None:
        self.grid = self.get_random_grid(self.grid)
        self.painter.render_pole(self.grid)

    def remove_grid(self) -> None:
        self.grid = self.get_random_grid(self.grid)
        if self.painter.id_run_fun:
            self.painter.cancel_after()

        self.painter.render_pole(self.grid)

    def initiate_events(self) -> None:
        self.painter.tk.bind('<BackSpace>', lambda _: self.remove_grid())
        self.painter.tk.bind('<1>', lambda _: self.painted_bot_on_click())
        self.painter.tk.bind(
            '<Return>',
            lambda _: self.painter.starter_fun_in_loop(self.run_main_loop),
        )
        self.painter.tk.bind(
            '<plus>',
            lambda _: self.painter.increase_time_loop(),
        )
        self.painter.tk.bind(
            '<minus>',
            lambda _: self.painter.reduce_time_loop(),
        )

    def run(self) -> None:
        self.initiate_events()
        self.painter.run_painter_loop()


if __name__ == '__main__':
    game = Game()
    game.run()
