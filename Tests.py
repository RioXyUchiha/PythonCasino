# Librairies
import pygame
import sys
import json
import os
import random
import websockets

pygame.init()

# Variables
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
WINDOW_WIDTH, WINDOW_HEIGHT = int(SCREEN_WIDTH / 1.1), int(SCREEN_HEIGHT / 1.1)
GRID_SIZE, CELL_SIZE, CELL_MARGIN = 5, 80, 10
GRID_WIDTH = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
GRID_HEIGHT = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
JSON_FILE_PATH = "player_data.json"
IMAGES_DIR = "Images"

# Couleurs
WHITE = pygame.Color('white')
GRAY = pygame.Color('gray20')
GRAY_DARK = pygame.Color('gray30')
RED = pygame.Color('red')
YELLOW = pygame.Color('yellow')
BLACK = pygame.Color('black')

# Chargement des images
def load_images():
    images = {
        "star": pygame.transform.smoothscale(pygame.image.load(os.path.join(IMAGES_DIR, "star.png")), (CELL_SIZE // 1.5, CELL_SIZE // 1.5)),
        "bomb": pygame.transform.smoothscale(pygame.image.load(os.path.join(IMAGES_DIR, "bomb.png")), (CELL_SIZE // 1.5, CELL_SIZE // 1.5)),
        "saturn": pygame.transform.smoothscale(pygame.image.load(os.path.join(IMAGES_DIR, "saturn.png")), (CELL_SIZE // 1.5, CELL_SIZE // 1.5)),
    }
    return images

# Chargement de l'argent du joueur depuis le fichier JSON
def load_player_usd():
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, "r") as file:
                usd = json.load(file).get("usd", 0)
                return round(usd, 2)  # Arrondi à deux décimales
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON: {e}")
    return 0

# Sauvegarde de l'argent du joueur dans le fichier JSON
def save_player_usd(usd):
    try:
        with open(JSON_FILE_PATH, "w") as file:
            json.dump({"usd": round(usd, 2)}, file)  # Arrondi à deux décimales
    except IOError as e:
        print(f"Error saving JSON: {e}")

# Initialisation de la grille de jeu
def initialize_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    bomb_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    grid[bomb_pos[0]][bomb_pos[1]] = -1  # Placement d'une bombe
    return grid

# Dessin de la grille
def draw_grid(screen, grid, revealed_cells, images, grid_x, grid_y):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(grid_x + col * (CELL_SIZE + CELL_MARGIN), grid_y + row * (CELL_SIZE + CELL_MARGIN), CELL_SIZE, CELL_SIZE)
            if (row, col) in revealed_cells:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, "tomato2", rect) 
                    image = images["bomb"]
                else:
                    image = images["star"]
                    pygame.draw.rect(screen, "goldenrod2", rect)
            else:
                pygame.draw.rect(screen, "gray40", rect)
                image = images["saturn"]
            image_rect = image.get_rect(center=rect.center)
            screen.blit(image, image_rect.topleft)

# Dessin du texte
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Dessin du texte du multiplicateur
def draw_multiplier_text(screen, multiplier_text, pos):
    font = pygame.font.SysFont(None, 36)  # Police plus grande pour la visibilité
    text_surface = font.render(multiplier_text, True, WHITE)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

# Boucle principale du jeu
def main():
    images = load_images()
    player_usd = load_player_usd()
    grid = initialize_grid()
    revealed_cells = set()
    game_over = False
    game_started = False
    bet_amount = 0
    current_multiplier = 1.0
    cashout_value = 0
    multiplier_displays = []

    # Affichage de la fenetre
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 30)
    input_box = pygame.Rect(20, 50, 100, 30)
    bet_button = pygame.Rect(20, 100, 100, 30)
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('lightskyblue3')
    color = color_inactive
    active = False
    text = ''
    betting = False

    clock = pygame.time.Clock()

    FRAME_WIDTH = WINDOW_WIDTH // 1.5
    FRAME_HEIGHT = WINDOW_HEIGHT // 1.5
    FRAME_X = (WINDOW_WIDTH - FRAME_WIDTH) // 2
    FRAME_Y = (WINDOW_HEIGHT - FRAME_HEIGHT) // 2

    LEFT_PANEL_WIDTH = FRAME_WIDTH // 4
    RIGHT_PANEL_WIDTH = FRAME_WIDTH - LEFT_PANEL_WIDTH
    PANEL_HEIGHT = FRAME_HEIGHT - 40 
    SEPARATION = 20

    LEFT_PANEL_X = FRAME_X
    LEFT_PANEL_Y = FRAME_Y
    RIGHT_PANEL_X = LEFT_PANEL_X + LEFT_PANEL_WIDTH + SEPARATION
    RIGHT_PANEL_Y = FRAME_Y

    GRID_X = RIGHT_PANEL_X + (RIGHT_PANEL_WIDTH - GRID_WIDTH) // 2
    GRID_Y = RIGHT_PANEL_Y + (PANEL_HEIGHT - GRID_HEIGHT) // 2

    while True:
        screen.fill(GRAY_DARK)

        # Dessin des panneaux gauche et droit
        pygame.draw.rect(screen, GRAY, (LEFT_PANEL_X, LEFT_PANEL_Y, LEFT_PANEL_WIDTH, PANEL_HEIGHT))
        pygame.draw.rect(screen, GRAY, (RIGHT_PANEL_X, RIGHT_PANEL_Y, RIGHT_PANEL_WIDTH, PANEL_HEIGHT))

        # Affichage de l'argent du joueur
        player_usd_text = f"{round(player_usd, 2):.2f} USD"
        player_usd_width, _ = font.size(player_usd_text)
        player_usd_x = WINDOW_WIDTH // 2 - player_usd_width // 2
        draw_text(screen, player_usd_text, font, WHITE, player_usd_x, 10)

        # Dessin de la grille
        draw_grid(screen, grid, revealed_cells, images, GRID_X, GRID_Y)

        # Affichage du montant de la mise
        draw_text(screen, "Bet Amount:", font, WHITE, LEFT_PANEL_X + 10, LEFT_PANEL_Y + 20)

        # Positionnement de la boîte de saisie et du bouton de mise
        input_box.topleft = (LEFT_PANEL_X + 10, LEFT_PANEL_Y + 50)
        bet_button.topleft = (LEFT_PANEL_X + 10, LEFT_PANEL_Y + 100)

        # Texte du bouton de mise et de retrait
        bet_text = "BET" if not game_started else "CASH OUT"
        cashout_text = f"{round(cashout_value, 2):.2f} USD" if game_started else text if text else "0"

        bet_button.width = 270
        bet_button.height = 50
        pygame.draw.rect(screen, color_active if betting else color_inactive, bet_button)

        # Affichage des textes du bouton et du montant de retrait
        bet_text_width, bet_text_height = font.size(bet_text)
        cashout_text_width, cashout_text_height = font.size(cashout_text)

        draw_text(screen, bet_text, font, WHITE, bet_button.centerx - bet_text_width // 2, bet_button.centery - bet_text_height // 2 - 10)
        draw_text(screen, cashout_text, font, WHITE, bet_button.centerx - cashout_text_width // 2, bet_button.centery + bet_text_height // 2 - 10)

        # Affichage du texte de mise
        txt_surface = font.render(text, True, color)
        width = max(270, txt_surface.get_width() + 10)
        input_box.width = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Affichage des multiplicateurs
        current_time = pygame.time.get_ticks()
        for display in multiplier_displays[:]:
            cell_pos, multiplier_value, display_time = display
            if current_time - display_time < 1000:
                row, col = cell_pos
                cell_center = (GRID_X + col * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2, GRID_Y + row * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2)
                draw_multiplier_text(screen, f"x{multiplier_value:.2f}", cell_center)
            else:
                multiplier_displays.remove(display)

        # Vérification de la fin de la partie
        if game_started:
            all_non_bomb_cells_revealed = len(revealed_cells) == (GRID_SIZE * GRID_SIZE - 1)
            if all_non_bomb_cells_revealed:
                revealed_cells = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)}
                player_usd += cashout_value
                player_usd = round(player_usd, 2)
                game_over = True
                game_started = False
                betting = False
                multiplier_displays.clear()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_player_usd(player_usd)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if bet_button.collidepoint(event.pos):
                    if not game_started:
                        try:
                            bet_amount = int(text)
                            if bet_amount > 1 and bet_amount <= player_usd:
                                player_usd -= bet_amount
                                player_usd = round(player_usd, 2)
                                game_started = True
                                betting = True
                                revealed_cells.clear()
                                grid = initialize_grid()
                                game_over = False
                                current_multiplier = 1.0
                                cashout_value = round(bet_amount * current_multiplier, 2) 
                            else:
                                print("Invalid bet amount.")
                        except ValueError:
                            print("Please enter a valid number.")
                    else:
                        if game_started:
                            player_usd += cashout_value 
                            player_usd = round(player_usd, 2) 
                            revealed_cells = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)}
                            game_over = True
                            game_started = False
                            betting = False  
                            multiplier_displays.clear()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if event.unicode.isdigit():
                            text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
                x, y = event.pos
                col = int((x - GRID_X) // (CELL_SIZE + CELL_MARGIN))
                row = int((y - GRID_Y) // (CELL_SIZE + CELL_MARGIN))

                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if (row, col) not in revealed_cells:
                        if grid[row][col] == -1:
                            revealed_cells = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)}
                            game_over = True
                            game_started = False
                            betting = False 
                            multiplier_displays.clear() 
                        else:
                            revealed_cells.add((row, col))
                            if current_multiplier == 1.0:
                                current_multiplier = 1.09 
                            else:
                                increment = current_multiplier * 0.15 
                                current_multiplier += increment
                            cashout_value = round(bet_amount * current_multiplier, 2)
                            multiplier_displays.append(((row, col), current_multiplier, pygame.time.get_ticks()))

        pygame.display.flip()
        clock.tick(30)

main()
