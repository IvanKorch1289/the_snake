from random import choice, randrange

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DICT_KEY_EVENT = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (220, 220, 220)
SCORE_COLOR = (255, 165, 0)

START_COUNT_STONES = (GRID_WIDTH + GRID_HEIGHT) // 4

START_SPEED = 10

SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    def __init__(self,
                 body_color=BOARD_BACKGROUND_COLOR,
                 position=SCREEN_CENTER):
        self.body_color = body_color
        self.position = position

    def draw_cell(self, position):
        """Метод отрисовки одной ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для отрисовки объектов на игровом поле"""
        self.draw_cell(self.position)


class Apple(GameObject):
    """Класс игрового объекта - Яблоко."""

    def __init__(self, body_color, position):
        super().__init__(body_color, position=self.randomize_position())

    @staticmethod
    def randomize_position():
        """Метод для определения случайной позиции объекта."""
        coordinate_x = randrange(0, SCREEN_WIDTH - 1, GRID_SIZE)
        coordinate_y = randrange(0, SCREEN_HEIGHT - 1, GRID_SIZE)
        return (coordinate_x, coordinate_y)


class Stone(Apple):
    """Класс игрового объекта - Камень."""


class Snake(GameObject):
    """Класс игрового объекта - Змейка."""

    def __init__(self, body_color, position):
        super().__init__(body_color, position)
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления движения игрового объекта."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновления позиции игрового объекта."""
        head = self.get_head_position()

        new_head_position = ()

        coord_x = head[0] % SCREEN_WIDTH + self.direction[0] * GRID_SIZE
        coord_y = head[-1] % SCREEN_HEIGHT + self.direction[-1] * GRID_SIZE

        new_head_position = (coord_x, coord_y)

        if new_head_position in self.positions:
            index_head = self.positions.index(new_head_position)
            if index_head not in (0, 1):
                self.reset()

        self.positions.insert(0, new_head_position)

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
            self.draw_cell(position)

        self.draw_cell(self.get_head_position())

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
            reverse_direction = tuple([i * -1 for i in game_object.direction])
            if reverse_direction != DICT_KEY_EVENT[event.key]:
                game_object.next_direction = DICT_KEY_EVENT[event.key]


def main():
    """Основной метод игры"""
    pygame.init()

    speed = START_SPEED

    score = 0
    font_score = pygame.font.SysFont('Arial', 20, bold=True)

    apple = Apple(APPLE_COLOR, Apple.randomize_position())
    snake = Snake(SNAKE_COLOR, SCREEN_CENTER)
    list_stones = []

    for i in range(START_COUNT_STONES):
        stone = Stone(STONE_COLOR, Stone.randomize_position())
        while stone.position == apple.position:
            stone.position = Stone.randomize_position()
        list_stones.append(stone)

    while True:
        clock.tick(speed)

        list_stones_position = [st.position for st in list_stones]

        render_score = font_score.render(f'Баллы: {score}', 1, SCORE_COLOR)
        screen.blit(render_score, (5, 5))

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        apple.draw()
        snake.draw()
        for stone in list_stones:
            stone.draw()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            apple.position = Apple.randomize_position()

            ls_occupied_cells = snake.positions + list_stones_position
            while apple.position in ls_occupied_cells:
                apple.randomize_position()

            if len(snake.positions) % 5 == 0:
                stone = Stone(STONE_COLOR, Stone.randomize_position())
                list_stones.append(stone)
                speed += 2

            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() in list_stones_position:
            snake.reset()
            del list_stones[START_COUNT_STONES - 1]
            score = 0
            speed = START_SPEED

        snake.last = snake.positions[-1]

        pygame.display.update()


if __name__ == '__main__':
    main()
