import time
import random

import pygame


class Game:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 500

        self.fps_controller = pygame.time.Clock()

        self.score = 0

    def set_surface(self):
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))

    def set_title(self):
        pygame.display.set_caption('Snake')

    def text_renderer(self, message, text_color, text_size):
        font = pygame.font.SysFont('Ubuntu Mono', text_size)
        text = font.render(message, 0, text_color)
        return text

    def main_menu(self):
        menu = True
        selected = 'Start'

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = 'Start'
                    elif event.key == pygame.K_DOWN:
                        selected = 'Quit'
                    if event.key == pygame.K_RETURN:
                        if selected == 'Start':
                            print('Start')
                            run()
                        if selected == 'Quit':
                            pygame.quit()
                            quit()

            self.surface.fill((98, 48, 98))

            text_title = self.text_renderer('Snake Game', (0, 255, 0), 30)

            if selected == 'Start':
                text_start = self.text_renderer('Start', (250, 250, 250), 20)
            else:
                text_start = self.text_renderer('Start', (0, 0, 0), 20)
            if selected == 'Quit':
                text_quit = self.text_renderer('Quit', (250, 250, 250), 20)
            else:
                text_quit = self.text_renderer('Quit', (0, 0, 0), 20)

            rect_title = text_title.get_rect()
            rect_start = text_start.get_rect()
            rect_quit = text_quit.get_rect()

            self.surface.blit(text_title, (self.screen_width / 2 - (rect_title[2] / 2), 80))
            self.surface.blit(text_start, (self.screen_width / 2 - (rect_start[2] / 2), 180))
            self.surface.blit(text_quit, (self.screen_width / 2 - (rect_quit[2] / 2), 220))

            pygame.display.update()
            game.refresh_screen()

    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_ESCAPE:
                    game.main_menu()

        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        game.fps_controller.tick(18)

    def show_score(self):
        font = pygame.font.SysFont('Ubuntu Mono', 18)
        surf = font.render(f'Score: {self.score}', True, (255, 255, 255))
        rect = surf.get_rect()
        rect.midtop = (450, 10)
        self.surface.blit(surf, rect)

    def game_over(self):
        font = pygame.font.SysFont('Ubuntu Mono', 32)
        surf = font.render('Game over', True, (255, 255, 255))
        rect = surf.get_rect()
        rect.midtop = (250, 200)
        self.surface.blit(surf, rect)
        pygame.display.flip()
        time.sleep(3)
        game.main_menu()


class Snake:
    def __init__(self):
        self.snake_head_pos = [380, 50]
        self.snake_body = [[380, 50], [390, 50], [400, 50], [410, 50], [420, 50], [430, 50]]
        self.snake_color = (70, 255, 80)
        self.direction = 'LEFT'
        self.change_to = self.direction

    def draw_snake(self, surface, surface_color=(98, 48, 98)):
        surface.fill(surface_color)
        for pos in self.snake_body:
            # pygame.Rect(x, y, sizex, sizey)
            pygame.draw.rect(surface, self.snake_color, pygame.Rect(pos[0], pos[1], 9, 9))

    def crossing_border(self):
        if self.snake_head_pos[0] < 0:
            # TODO set screen width
            self.snake_head_pos[0] = 490
        elif self.snake_head_pos[0] > 490:
            self.snake_head_pos[0] = 0
        elif self.snake_head_pos[1] < 0:
            self.snake_head_pos[1] = 490
        elif self.snake_head_pos[1] > 490:
            self.snake_head_pos[1] = 0

    def change_direction(self):
        if any((self.change_to == 'RIGHT' and not self.direction == 'LEFT',
                self.change_to == 'LEFT' and not self.direction == 'RIGHT',
                self.change_to == 'UP' and not self.direction == 'DOWN',
                self.change_to == 'DOWN' and not self.direction == 'UP')):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == 'RIGHT':
            self.snake_head_pos[0] += 10
        elif self.direction == 'LEFT':
            self.snake_head_pos[0] -= 10
        elif self.direction == 'UP':
            self.snake_head_pos[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, food_pos, screen_width, screen_height, score):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if self.snake_head_pos == food_pos:
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return food_pos, score

    def check_crash(self, game_over):
        for block in self.snake_body[1:]:
            if block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]:
                game_over()


class Food:
    def __init__(self, screen_width, screen_height):
        self.food_color = (255, 0, 0)
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]

    def draw_food(self, surface):
        pygame.draw.rect(surface, self.food_color, pygame.Rect(self.food_pos[0], self.food_pos[1],
                                                               self.food_size_x, self.food_size_y))


def run():
    snake = Snake()
    food = Food(game.screen_width, game.screen_height)
    game.set_title()
    game.set_surface()

    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.change_head_position()
        snake.change_direction()
        snake.crossing_border()
        food.food_pos, game.score = snake.snake_body_mechanism(food.food_pos, game.screen_width, game.screen_height,
                                                               game.score)
        snake.draw_snake(game.surface)
        food.draw_food(game.surface)
        snake.check_crash(game.game_over)

        game.show_score()
        game.refresh_screen()


pygame.init()
game = Game()
game.set_title()
game.set_surface()
game.main_menu()
