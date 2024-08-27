import pygame
import sys
import json
import os

pygame.init()

# Variables
window_width = 960
window_height = 520
json_file_path = "player_data.json"

def load_player_usd():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
                return data.get("usd", 0)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors de la lecture du fichier JSON : {e}")
    return 0

def save_player_usd(usd):
    try:
        with open(json_file_path, "w") as file:
            json.dump({"usd": usd}, file)
    except IOError as e:
        print(f"Erreur lors de l'écriture dans le fichier JSON : {e}")
# adasdawdggafaa
player_usd = load_player_usd()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Casino")

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill("gray20")
    
    usd_text = font.render(f"{player_usd} USD", True, "white")
    screen.blit(usd_text, (window_width - usd_text.get_width() - 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

save_player_usd(player_usd)
pygame.quit()
sys.exit()