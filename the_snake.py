from random import randint, choice

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

# Парметры камней
STONE_COLOR = (220, 220, 220)
COUNT_STONES = (GRID_WIDTH + GRID_HEIGHT) // 4

# Скорость движения змейки:
SPEED = 10

# Центр экрана
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    def __init__(self):
        self.position = SCREEN_CENTER

    def draw(self):
        """Метод для отрисовки объектов на игровом поле"""
        pass


class Apple(GameObject):
    """Класс игрового объекта - Яблоко."""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод для определения случайной позиции объекта."""
        coordinate_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        coordinate_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (coordinate_x, coordinate_y)

    def draw(self):
        """Метод отрисовки игрового объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(Apple):
    """Класс игрового объекта - Камень."""

    def __init__(self):
        self.position = None
        self.body_color = STONE_COLOR


class Snake(GameObject):
    """Класс игрового объекта - Змейка."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления движения игрового объекта."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновления позиции игрового объекта."""
        head = self.get_head_position()

        new_pos_head = ()

        if head[0] < 0:
            new_pos_head = (SCREEN_WIDTH, head[-1])
        elif head[0] > SCREEN_WIDTH:
            new_pos_head = (0, head[-1])
        elif head[-1] < 0:
            new_pos_head = (head[0], SCREEN_HEIGHT)
        elif head[-1] > SCREEN_HEIGHT:
            new_pos_head = (head[0], 0)
        else:
            coordinate_x = head[0] + self.direction[0] * GRID_SIZE
            coordinate_y = head[-1] + self.direction[-1] * GRID_SIZE
            new_pos_head = (coordinate_x, coordinate_y)

        if new_pos_head in self.positions:
            index_head = self.positions.index(new_pos_head)
            if index_head not in (0, 1):
                self.reset()

        self.positions.insert(0, new_pos_head)

        if len(self.positions) > self.length:
            self.positions.pop(-1)

    def get_head_position(self):
        """Метод определения позиции первого блока змейки"""
        return self.positions[0]

    def reset(self):
        """Метод обновления позиции змейки при столкновении"""
        self.length = 1
        self.position = SCREEN_CENTER
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод отрисовки игрового объекта."""
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


def handle_keys(game_object):
    """Функция получения действий для обновления направления движения."""
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


def main():
    apple = Apple()
    snake = Snake()
    list_stones = []

    for i in range(COUNT_STONES):
        stone = Stone()
        stone.position = stone.randomize_position()
        while stone.position == apple.position:
            stone.position = stone.randomize_position()
        list_stones.append(stone)

    while True:
        clock.tick(SPEED)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        if snake.get_head_position() in [st.position for st in list_stones]:
            snake.reset()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()
        for stone in list_stones:
            stone.draw()

        snake.last = snake.positions[-1]

        pygame.display.update()


if __name__ == '__main__':
    main()
