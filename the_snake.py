from random import choice, randint
from typing import Tuple

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Начальная длина змейки:
SNAKE_START_LENGTH = 1

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для игровых обьектов."""

    def __init__(self, body_color=None, border_color=None):
        self.position = SCREEN_CENTER
        self.body_color = body_color
        self.border_color = border_color

    def draw(self) -> None:
        """Метод отрисовки обьекта на игровом поле."""
        raise NotImplementedError('Не описан метод draw для дочернего класса.')

    def draw_cell(self, position) -> None:
        """Метод отрисовки одной ячейки на игровом поле."""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


class Apple(GameObject):
    """
    Класс обьекта Яблоко. Определяет случайную позицию и метод
    отрисовки на игровом поле. Наследуется от класса GameObject.
    """

    def __init__(self, body_color=APPLE_COLOR, border_color=BORDER_COLOR):
        super().__init__(body_color, border_color)
        self.taken_positions = (SCREEN_CENTER,)
        self.randomize_position(self.taken_positions)

    def draw(self) -> None:
        """Метод отрисовки обьекта Яблоко на игровом поле."""
        self.draw_cell(self.position)

    def randomize_position(self, taken_positions) -> None:
        """Метод выбора случайной позиции на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in taken_positions:
                break


class Snake(GameObject):
    """
    Класс обьекта Змейка. Определяет позицию, направление движения и
    используется для отрисовки обьекта на игровом поле.
    Наследуется от класса GameObject.
    """

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        super().__init__(body_color, border_color)
        self.length = SNAKE_START_LENGTH
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self) -> None:
        """Метод отрисовки обьекта Змейка на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_cell(position)

    def update_direction(self) -> None:
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """
        Метод обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        current_x, current_y = self.get_head_position()
        dx, dy = self.direction
        next_head_position = (
            (current_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, next_head_position)

    def get_head_position(self) -> Tuple[int, int]:
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сбрасывает змейку в начальное состояние"""
        self.length = SNAKE_START_LENGTH
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def main():
    """Запуск игры и основной игровой цикл."""
    pg.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        apple.draw()
        snake.draw()
        if len(snake.positions) != snake.length:
            snake.positions.pop()
        pg.display.update()


if __name__ == '__main__':
    main()
