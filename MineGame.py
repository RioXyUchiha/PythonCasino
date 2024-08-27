import pygame
import sys
import json
import os
import random

# Initialisation
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 520
GRID_SIZE, CELL_SIZE, CELL_MARGIN = 5, 60, 5
GRID_WIDTH = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
GRID_HEIGHT = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
GRID_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2
JSON_FILE_PATH = "player_data.json"
IMAGES_DIR = "Images"

# Load Images
def load_images():
    images = {
        "gem": pygame.transform.smoothscale(pygame.image.load(os.path.join(IMAGES_DIR, "star.png")), (CELL_SIZE // 1.25, CELL_SIZE // 1.25)),
        "bomb": pygame.transform.smoothscale(pygame.image.load(os.path.join(IMAGES_DIR, "bomb.png")), (CELL_SIZE // 1.25, CELL_SIZE // 1.25))
    }
    return images

def load_player_usd():
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, "r") as file:
                return json.load(file).get("usd", 0)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON: {e}")
    return 0

def save_player_usd(usd):
    try:
        with open(JSON_FILE_PATH, "w") as file:
            json.dump({"usd": usd}, file)
    except IOError as e:
        print(f"Error saving JSON: {e}")

def initialize_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    bomb_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    grid[bomb_pos[0]][bomb_pos[1]] = -1
    return grid

def draw_grid(screen, grid, revealed_cells, images):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(GRID_X + col * (CELL_SIZE + CELL_MARGIN), GRID_Y + row * (CELL_SIZE + CELL_MARGIN), CELL_SIZE, CELL_SIZE)
            if (row, col) in revealed_cells:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, "red", rect) 
                    image = images["bomb"]
                else:
                    image = images["gem"]
                    pygame.draw.rect(screen, "yellow", rect)
                # Center image in the cell
                image_rect = image.get_rect(center=rect.center)
                screen.blit(image, image_rect.topleft)
            else:
                pygame.draw.rect(screen, "gray20", rect)  # Draw gray background for unrevealed cells
            pygame.draw.rect(screen, "black", rect, 1)  # Draw black border around each cell

def main():
    images = load_images()
    player_usd = load_player_usd()
    grid = initialize_grid()
    revealed_cells = set()
    game_over = False
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 30)

    while True:
        screen.fill("gray30")
        screen.blit(font.render(f"{player_usd} USD", True, "white"), (WINDOW_WIDTH - 110, 10))
        draw_grid(screen, grid, revealed_cells, images)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_player_usd(player_usd)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - GRID_X) // (CELL_SIZE + CELL_MARGIN)
                row = (y - GRID_Y) // (CELL_SIZE + CELL_MARGIN)

                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if not game_over:
                        if (row, col) not in revealed_cells:
                            if grid[row][col] == -1:
                                revealed_cells = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)}
                                game_over = True
                            else:
                                revealed_cells.add((row, col))
                    else:
                        if (row, col) in revealed_cells:
                            grid = initialize_grid()
                            revealed_cells.clear()
                            game_over = False

        if game_over:
            pygame.display.set_caption("Game Over - Click to Restart")

        pygame.display.flip()

main()
