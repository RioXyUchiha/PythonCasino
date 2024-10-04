# Librairies
import pygame_widgets
import pygame
import sys
import json
import os
import random
import socket
import threading

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()

# Variables
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
window_width, window_height = int(screen_width / 1.1), int(screen_height / 1.1)
grid_size, cell_size, cell_margin = 5, 80, 10
grid_width = grid_size * (cell_size + cell_margin) - cell_margin
grid_height = grid_size * (cell_size + cell_margin) - cell_margin
json_file_path = "player_data.json"
images_dir = "Images"
bombs = 1

# Couleurs
white = pygame.Color('white')
gray = pygame.Color('gray20')
gray_dark = pygame.Color('gray30')
red = pygame.Color('red')
yellow = pygame.Color('yellow')
black = pygame.Color('black')

# Charge les images
def load_images():
    images = {
        "star": pygame.transform.smoothscale(pygame.image.load(os.path.join(images_dir, "star.png")), (cell_size // 1.5, cell_size // 1.5)),
        "bomb": pygame.transform.smoothscale(pygame.image.load(os.path.join(images_dir, "bomb.png")), (cell_size // 1.5, cell_size // 1.5)),
        "saturn": pygame.transform.smoothscale(pygame.image.load(os.path.join(images_dir, "saturn.png")), (cell_size // 1.5, cell_size // 1.5)),
    }
    return images

# Charge l'argent du joueur
def load_player_usd():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, "r") as file:
                usd = json.load(file).get("usd", 0)
                return round(usd, 2)  # Arrondi à deux décimales
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON: {e}")
    return 0

# Sauvegarde l'argent du joueur
def save_player_usd(usd):
    try:
        with open(json_file_path, "w") as file:
            json.dump({"usd": round(usd, 2)}, file)  # Arrondi à deux décimales
    except IOError as e:
        print(f"Error saving JSON: {e}")

# Initialisation de la grille de jeu
def initialize_grid(number_of_bombs):
    global bombs
    bombs = number_of_bombs
    grid = [[0] * grid_size for _ in range(grid_size)]
    for _ in range(bombs):
        bomb_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        while grid[bomb_pos[0]][bomb_pos[1]] != 0:
            print(grid[bomb_pos[0]][bomb_pos[1]])
            bomb_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        grid[bomb_pos[0]][bomb_pos[1]] = -1  # Placement d'une bombe

    return grid

# Création de la grille
def create_grid(screen, grid, revealed_cells, images, grid_x, grid_y):
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(grid_x + col * (cell_size + cell_margin), grid_y + row * (cell_size + cell_margin), cell_size, cell_size)
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

# Créer un texte
def create_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Créer le texte de multiplicateur
def create_multiplier_text(screen, multiplier_text, pos):
    font = pygame.font.SysFont(None, 36) 
    text_surface = font.render(multiplier_text, True, white)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

# Boucle principale du jeu
def main():
    frame_width = window_width // 1.5
    frame_height = window_height // 1.5
    frame_x = (window_width - frame_width) // 2
    frame_y = (window_height - frame_height) // 2

    left_panel_width = frame_width // 4
    right_panel_width = frame_width - left_panel_width
    panel_height = frame_height - 40 
    separation = 20

    left_panel_x = frame_x
    left_panel_y = frame_y
    right_panel_x = left_panel_x + left_panel_width + separation
    right_panel_y = frame_y

    grid_x = right_panel_x + (right_panel_width - grid_width) // 2
    grid_y = right_panel_y + (panel_height - grid_height) // 2

    images = load_images()
    player_usd = load_player_usd()
    grid = initialize_grid(1)
    revealed_cells = set()
    game_over = False
    game_started = False
    bet_amount = 0
    current_multiplier = 1.0
    cashout_value = 0
    multiplier_displays = []

    # Affichage de la fenêtre
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 30)
    bet_input_box = pygame.Rect(left_panel_x + 10, left_panel_y + 50, 100, 30)
    bet_button = pygame.Rect(left_panel_x + 10, left_panel_y + 100, 100, 30)
    bet_button.width = 270
    bet_button.height = 50
    slider = Slider(screen, int(left_panel_y) + 150, int(left_panel_x) + 110, 250, 20, min=1, max=24, step=1)
    slider.setValue(1)
    color_active = pygame.Color('goldenrod2')
    color_inactive = pygame.Color('white')
    color = color_inactive
    active = False
    text = ''
    betting = False

    clock = pygame.time.Clock()

    while True:
        screen.fill(gray_dark)

        # Création des rectangles gauche et droite
        pygame.draw.rect(screen, gray, (left_panel_x, left_panel_y, left_panel_width, panel_height))
        pygame.draw.rect(screen, gray, (right_panel_x, right_panel_y, right_panel_width, panel_height))

        # Affichage de l'argent du joueur
        player_usd_text = f"{round(player_usd, 2):.2f} USD"
        player_usd_width, _ = font.size(player_usd_text)
        player_usd_x = window_width // 2 - player_usd_width // 2
        create_text(screen, player_usd_text, font, white, player_usd_x, 10)

        # Création de la grille
        create_grid(screen, grid, revealed_cells, images, grid_x, grid_y)

        bomb_text = f"Number of Bombs: {slider.getValue()}"

        # ACréation de texte
        create_text(screen, "Bet Amount:", font, white, left_panel_x + 10, left_panel_y + 20)
        create_text(screen, bomb_text, font, white, left_panel_x + 10, left_panel_y + 200)

        # Texte du bouton de mise et de retrait
        bet_text = "BET" if not game_started else "CASH OUT"
        cashout_text = f"{round(cashout_value, 2):.2f} USD" if game_started else text if text else "0"

        pygame.draw.rect(screen, "green2" if betting else "goldenrod2", bet_button)

        # Affichage des textes du bouton et du montant de retrait
        bet_text_width, bet_text_height = font.size(bet_text)
        cashout_text_width, cashout_text_height = font.size(cashout_text)

        create_text(screen, bet_text, font, white, bet_button.centerx - bet_text_width // 2, bet_button.centery - bet_text_height // 2 - 10)
        create_text(screen, cashout_text, font, white, bet_button.centerx - cashout_text_width // 2, bet_button.centery + bet_text_height // 2 - 10)

        # Affichage du texte de mise
        text_bet_surface = font.render(text, True, "white")
        width = max(270, text_bet_surface.get_width() + 10)
        bet_input_box.width = width
        screen.blit(text_bet_surface, (bet_input_box.x + 5, bet_input_box.y + 5))
        pygame.draw.rect(screen, color, bet_input_box, 2)

        # Affichage des multiplicateurs
        current_time = pygame.time.get_ticks()
        for display in multiplier_displays[:]:
            cell_pos, multiplier_value, display_time = display
            if current_time - display_time < 1000:
                row, col = cell_pos
                cell_center = (grid_x + col * (cell_size + cell_margin) + cell_size // 2, grid_y + row * (cell_size + cell_margin) + cell_size // 2)
                create_multiplier_text(screen, f"x{multiplier_value:.2f}", cell_center)
            else:
                multiplier_displays.remove(display)

        # Vérification de la fin de la partie
        if game_started:
            all_non_bomb_cells_revealed = len(revealed_cells) == (grid_size * grid_size - bombs)
            # print(all_non_bomb_cells_revealed, bombs)
            if all_non_bomb_cells_revealed:
                revealed_cells = {(r, c) for r in range(grid_size) for c in range(grid_size)}
                player_usd += cashout_value
                player_usd = round(player_usd, 2)
                game_over = True
                game_started = False
                betting = False
                multiplier_displays.clear()

        # Gestion des événements
        for event in pygame.event.get():
            # Quitte le jeu
            if event.type == pygame.QUIT:
                save_player_usd(player_usd)
                pygame.quit()
                sys.exit()
            
            # Gestion des clics de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Gestion de la boîte de saisie pour le montant de la mise
                if bet_input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False 
                color = color_active if active else color_inactive

                # Gestion du bouton de mise
                if bet_button.collidepoint(event.pos):
                    if not game_started: 
                        try:
                            bet_amount = int(text)
                            # Vérifie que la mise est valide et que le joueur a suffisamment d'argent
                            if bet_amount >= 1 and bet_amount <= player_usd:
                                player_usd -= bet_amount
                                player_usd = round(player_usd, 2)
                                game_started = True
                                betting = True
                                revealed_cells.clear()
                                grid = initialize_grid(slider.getValue())
                                print(bombs)
                                game_over = False
                                current_multiplier = 1.0
                                cashout_value = round(bet_amount * current_multiplier, 2)
                            else:
                                print("Invalid bet amount.")
                        except ValueError:
                            print("Please enter something.")
                    else:  # Si le jeu a commencé
                        player_usd += cashout_value
                        player_usd = round(player_usd, 2) 
                        revealed_cells = {(r, c) for r in range(grid_size) for c in range(grid_size)} # Révèle toutes les cellules pour terminer le jeu
                        game_over = True
                        game_started = False
                        betting = False
                        multiplier_displays.clear()

            # Gestion des entrées du clavier
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False 
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if event.unicode.isdigit():
                            text += event.unicode  # Ajoute le caractère saisi au texte

            # Gestion des clics de la souris pour révéler les cellules
            if event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
                x, y = event.pos
                col = int((x - grid_x) // (cell_size + cell_margin))  # Calcule la colonne de la cellule cliquée
                row = int((y - grid_y) // (cell_size + cell_margin))  # Calcule la ligne de la cellule cliquée

                # Vérifie que la cellule cliquée est dans les limites de la grille
                if 0 <= row < grid_size and 0 <= col < grid_size:
                    if (row, col) not in revealed_cells:
                        if grid[row][col] == -1:  # Si une bombe est trouvée
                            revealed_cells = {(r, c) for r in range(grid_size) for c in range(grid_size)}  # Révèle toutes les cellules
                            game_over = True
                            game_started = False
                            betting = False
                            multiplier_displays.clear()
                        else:
                            revealed_cells.add((row, col))
                            if current_multiplier == 1.0:
                                current_multiplier = 1.05
                            else:
                                increment = current_multiplier * 0.1
                                current_multiplier += increment
                            cashout_value = round(bet_amount * current_multiplier, 2)
                            multiplier_displays.append(((row, col), current_multiplier, pygame.time.get_ticks()))

            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()
            clock.tick(60)

main()