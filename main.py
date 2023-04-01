import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake's thoughts
THOUGHTS = [
    "I wonder what's beyond this screen...",
    "Is there more to life than just eating and growing?",
    "What if I'm just a character in a video game?",
    "Am I the only snake in this world?",
    "I wish I had some snake friends...",
    "Why is my food always running away from me?",
]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASICFONT = pygame.font.Font(None, 18)
    pygame.display.set_caption("Snake Thoughts")

    while True:
        run_game()
        show_gameover_screen()

def run_game():
    snake_coords = [{"x": CELL_SIZE, "y": CELL_SIZE}]
    direction = "right"
    food = get_random_location()
    thought = ""

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_UP and direction != "down":
                    direction = "up"
                elif event.key == K_DOWN and direction != "up":
                    direction = "down"
                elif event.key == K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == K_RIGHT and direction != "left":
                    direction = "right"

        if direction == "up":
            new_head = {"x": snake_coords[0]["x"], "y": snake_coords[0]["y"] - CELL_SIZE}
        elif direction == "down":
            new_head = {"x": snake_coords[0]["x"], "y": snake_coords[0]["y"] + CELL_SIZE}
        elif direction == "left":
            new_head = {"x": snake_coords[0]["x"] - CELL_SIZE, "y": snake_coords[0]["y"]}
        elif direction == "right":
            new_head = {"x": snake_coords[0]["x"] + CELL_SIZE, "y": snake_coords[0]["y"]}

        if (new_head["x"] < 0 or new_head["x"] >= WINDOW_WIDTH or
            new_head["y"] < 0 or new_head["y"] >= WINDOW_HEIGHT or
            new_head in snake_coords):
            return

        snake_coords.insert(0, new_head)

        if (snake_coords[0]["x"] == food["x"] and
            snake_coords[0]["y"] == food["y"]):
            food = get_random_location()
            thought = random.choice(THOUGHTS)
        else:
            snake_coords.pop()

        DISPLAYSURF.fill(BLACK)
        draw_snake(snake_coords)
        draw_food(food)
        draw_thought(thought)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_snake(snake_coords):
    for coord in snake_coords:
        pygame.draw.rect(DISPLAYSURF, GREEN, (coord['x'], coord['y'], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(DISPLAYSURF, RED, (food['x'], food['y'], CELL_SIZE, CELL_SIZE))

def draw_thought(thought):
    thought_surf = BASICFONT.render(thought, True, WHITE)
    thought_rect = thought_surf.get_rect()
    thought_rect.topleft = (10, WINDOW_HEIGHT - 30)
    DISPLAYSURF.blit(thought_surf, thought_rect)

def get_random_location():
    return {
        "x": random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        "y": random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
    }

def show_gameover_screen():
    gameover_font = pygame.font.Font(None, 48)
    gameover_surf = gameover_font.render("Game Over! Press any key to play again.", True, WHITE)
    gameover_rect = gameover_surf.get_rect()
    gameover_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)

    DISPLAYSURF.blit(gameover_surf, gameover_rect)
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                else:
                    return

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
