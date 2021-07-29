import pygame
from gym import Env
from pygame import Vector2
from gym.spaces import Discrete, Box
import numpy as np
import random
import sys
from time import sleep


class SnakeEnv(Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Game board related constant values (20x20 [squares] game board on 640x640 [pixels] screen)
        self.GRID_DENSITY = 20
        self.DISPLAY_SIZE = 640
        self.BODY_PART_SIZE = (self.DISPLAY_SIZE // self.GRID_DENSITY, self.DISPLAY_SIZE // self.GRID_DENSITY)
        self.SCREEN_CENTER = (self.DISPLAY_SIZE / 2, self.DISPLAY_SIZE / 2)
        self.MOVEMENT_STEP = self.BODY_PART_SIZE[0]
        self.ROWS = int(self.DISPLAY_SIZE / self.BODY_PART_SIZE[0])

        # Fruit and snake position
        self.fruit_x = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[0]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_y = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[1]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_pos = Vector2(self.fruit_x, self.fruit_y)

        self.body = [Vector2(self.SCREEN_CENTER[0], self.SCREEN_CENTER[1]),
                     Vector2(self.SCREEN_CENTER[0] - self.BODY_PART_SIZE[0], self.SCREEN_CENTER[1]),
                     Vector2(self.SCREEN_CENTER[0] - (2 * self.BODY_PART_SIZE[0]), self.SCREEN_CENTER[1])]

        # Movement related variables
        self.N = Vector2(0, -self.MOVEMENT_STEP)
        self.E = Vector2(self.MOVEMENT_STEP, 0)
        self.S = Vector2(0, self.MOVEMENT_STEP)
        self.W = Vector2(-self.MOVEMENT_STEP, 0)
        self.DIRECTIONS = (self.N, self.E, self.S, self.W)

        # Initial direction of snake (right)
        self.directions_index = 1
        self.direction = self.DIRECTIONS[self.directions_index]

        self.score = 0
        self.frame_iteration = 0

        self.action_space = Discrete(3)
        self.observation_space = Box(low=0, high=1, shape=(11,), dtype=np.uint8)

    def step(self, action):
        self.frame_iteration += 1
        game_over = False

        # Turn right
        if action == 0:
            if self.directions_index == len(self.DIRECTIONS) - 1:
                self.directions_index = 0
            else:
                self.directions_index += 1
            self.direction = self.DIRECTIONS[self.directions_index]
        # Turn left
        elif action == 2:
            if self.directions_index == 0:
                self.directions_index = len(self.DIRECTIONS) - 1
            else:
                self.directions_index -= 1
            self.direction = self.DIRECTIONS[self.directions_index]
        # Go forward
        elif action == 1:
            self.direction = self.DIRECTIONS[self.directions_index]

        self.move_snake()

        reward = 0

        # Conditions of ending the game
        if self.detect_collision() or self.frame_iteration > 60 * len(self.body):
            game_over = True
            reward = -10

        # Condition of eating the food
        if self.body[0] == self.fruit_pos:
            self.expand_snake()
            self.create_new_fruit()
            self.frame_iteration = 0
            self.score += 1
            reward = 10

        # Generating new food if old one was eaten
        if self.is_food_eaten():
            self.create_new_fruit()

        info = {}

        observation = self.get_state()
        return observation, reward, game_over, info

    def reset(self):
        self.fruit_x = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[0]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_y = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[1]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_pos = Vector2(self.fruit_x, self.fruit_y)
        self.body = [Vector2(self.SCREEN_CENTER[0], self.SCREEN_CENTER[1]),
                     Vector2(self.SCREEN_CENTER[0] - self.BODY_PART_SIZE[0], self.SCREEN_CENTER[1]),
                     Vector2(self.SCREEN_CENTER[0] - (2 * self.BODY_PART_SIZE[0]), self.SCREEN_CENTER[1])]

        self.directions_index = 1
        self.direction = self.DIRECTIONS[self.directions_index]

        self.score = 0
        self.frame_iteration = 0

        observation = self.get_state()
        return observation

    def render(self, mode='human'):
        pygame.init()
        pygame.display.set_caption("Snake")

        self.font = pygame.font.Font(None, int(self.DISPLAY_SIZE / 25))
        self.screen = pygame.display.set_mode((self.DISPLAY_SIZE, self.DISPLAY_SIZE))
        self.clock = pygame.time.Clock()

        text_score_font = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        frame_ite_font = self.font.render(f"Time left: {60 * len(self.body) - self.frame_iteration}", True,
                                          (255, 255, 255))

        # Exit the game with ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        sleep(0.04)

        self.screen.fill((0, 0, 0))
        self.draw_snake()
        self.draw_fruit()
        self.screen.blit(text_score_font, (0, 0))
        self.screen.blit(frame_ite_font, (0, 20))

        pygame.display.update()
        self.clock.tick(60)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x)
            y_pos = int(block.y)
            body_rect = pygame.Rect((x_pos, y_pos), self.BODY_PART_SIZE)
            pygame.draw.rect(self.screen, (0, 155, 100), body_rect)

    def move_snake(self):
        new_body = self.body[:-1]
        new_body.insert(0, new_body[0] + self.direction)
        self.body = new_body[:]

    def expand_snake(self):
        new_cords = Vector2(self.body[-1].x,
                             self.body[-1].y)
        self.body.append(new_cords)

    def draw_fruit(self):
        fruit_rect = pygame.Rect((self.fruit_pos.x, self.fruit_pos.y), self.BODY_PART_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 0), fruit_rect)

    def create_new_fruit(self):
        self.fruit_x = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[0]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_y = random.randint(0, int(self.DISPLAY_SIZE - self.BODY_PART_SIZE[1]) //
                                      self.BODY_PART_SIZE[0]) * self.BODY_PART_SIZE[0]
        self.fruit_pos = Vector2(self.fruit_x, self.fruit_y)

    def detect_collision(self, point=None):
        if point is None:
            point = self.body[0]
        return point.x < 0 or point.x > self.DISPLAY_SIZE - self.BODY_PART_SIZE[0] or \
               point.y < 0 or point.y > self.DISPLAY_SIZE - self.BODY_PART_SIZE[0] or \
               point in self.body[1:]

    def is_food_eaten(self):
        return self.fruit_pos in self.body[1:]

    def get_state(self):
        head = self.body[0]

        point_left = Vector2(head.x - self.BODY_PART_SIZE[0], head.y)
        point_right = Vector2(head.x + self.BODY_PART_SIZE[0], head.y)
        point_up = Vector2(head.x, head.y - self.BODY_PART_SIZE[0])
        point_down = Vector2(head.x, head.y + self.BODY_PART_SIZE[0])

        dir_left = self.direction == self.W
        dir_right = self.direction == self.E
        dir_up = self.direction == self.N
        dir_down = self.direction == self.S

        state = [
            # Danger straight
            (dir_right and self.detect_collision(point_right)) or
            (dir_left and self.detect_collision(point_left)) or
            (dir_up and self.detect_collision(point_up)) or
            (dir_down and self.detect_collision(point_down)),

            # Danger right
            (dir_up and self.detect_collision(point_right)) or
            (dir_down and self.detect_collision(point_left)) or
            (dir_left and self.detect_collision(point_up)) or
            (dir_right and self.detect_collision(point_down)),

            # Danger left
            (dir_down and self.detect_collision(point_right)) or
            (dir_up and self.detect_collision(point_left)) or
            (dir_right and self.detect_collision(point_up)) or
            (dir_left and self.detect_collision(point_down)),

            # Move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,

            # Food location
            self.fruit_x < head.x,  # food left
            self.fruit_x > head.x,  # food right
            self.fruit_y < head.y,  # food up
            self.fruit_y > head.y  # food down
        ]
        return np.array(state, dtype=np.uint8)
