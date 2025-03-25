from random import choice, randint
from typing import Tuple

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для игровых обьектов."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self) -> None:
        """Метод отрисовки обьекта на игровом поле."""
        pass


class Apple(GameObject):
    """
    Класс обьекта Яблоко. Определяет случайную позицию и метод
    отрисовки на игровом поле. Наследуется от класса GameObject.
    """

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовки обьекта Яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self) -> Tuple[int, int]:
        """Метод выбора случайной позиции на игровом поле."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """
    Класс обьекта Змейка. Определяет позицию, направление движения и
    используется для отрисовки обьекта на игровом поле.
    Наследуется от класса GameObject.
    """

    def __init__(self):
        super().__init__()
        self.length = SNAKE_START_LENGTH
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Метод отрисовки обьекта Змейка на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self) -> None:
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> Tuple[int, int]:
        """
        Метод обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        current_x, current_y = self.get_head_position()
        dx, dy = self.direction
        return (
            (current_x + dx * 20) % SCREEN_WIDTH,
            (current_y + dy * 20) % SCREEN_HEIGHT
        )

    def get_head_position(self) -> Tuple[int, int]:
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сбрасывает змейку в начальное состояние"""
        self.length = SNAKE_START_LENGTH
        self.positions = [(self.position)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def main():
    """Запуск игры и основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        next_head_position = snake.move()
        if next_head_position in snake.positions:
            snake.reset()
        snake.positions.insert(0, next_head_position)
        if next_head_position == apple.position:
            snake.length = snake.length + 1
            apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        if len(snake.positions) != snake.length:
            snake.last = snake.positions.pop()
        pygame.display.update()


if __name__ == '__main__':
    main()
