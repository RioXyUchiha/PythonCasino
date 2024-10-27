import pygame
import sys
import re  # Importation de l'expression régulière pour la validation de l'e-mail
from Database import create_connection, insert_player, get_player

# Initialisation de Pygame
pygame.init()

# Variables
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login/Register System")

# Police de caractères
font = pygame.font.SysFont(None, 36)

# Champs de saisie
input_box_username = pygame.Rect(300, 150, 200, 40)
input_box_email = pygame.Rect(300, 220, 200, 40)
input_box_password = pygame.Rect(300, 290, 200, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
username_text = ''
email_text = ''
password_text = ''
active_input = None

# Fonction pour dessiner du texte
def draw_text(text, pos, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Fonction pour dessiner un bouton
def draw_button(text, rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    draw_text(text, (rect.x + 10, rect.y + 10))

# Fonction pour vérifier la validité de l'adresse e-mail
def is_valid_email(email):
    """ Vérifie si l'adresse e-mail est valide et se termine par @gmail.com. """
    regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(regex, email) is not None

def main():
    global active_input, username_text, email_text, password_text

    # Connexion à la base de données
    conn = create_connection()
    if not conn:
        print("Échec de la connexion à la base de données.")
        sys.exit()

    # Boucle principale du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn.close()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active_input == 'username':
                    if event.key == pygame.K_RETURN:
                        if username_text and email_text and password_text:  # Vérifier si les champs sont remplis
                            if is_valid_email(email_text):  # Validation de l'e-mail
                                insert_player(conn, username_text, email_text, password_text)
                                username_text = ''
                                email_text = ''
                                password_text = ''
                                conn.close()  # Fermer la connexion
                                pygame.quit()  # Quitter Pygame
                                sys.exit()     # Quitter le programme
                            else:
                                print("L'e-mail doit se terminer par @gmail.com.")
                        else:
                            print("Veuillez remplir tous les champs.")
                    elif event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif active_input == 'email':
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        email_text += event.unicode
                elif active_input == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if login_button.collidepoint(event.pos):
                        # Appel de la fonction de connexion
                        if username_text and password_text:  # Vérifier si les champs sont remplis
                            player = get_player(conn, username_text)
                            if player:  # Supposant que get_player retourne None si non trouvé
                                username_text = ''
                                email_text = ''
                                password_text = ''
                                conn.close()  # Fermer la connexion
                                pygame.quit()  # Quitter Pygame
                                sys.exit()     # Quitter le programme
                            else:
                                print("Utilisateur non trouvé.")
                    elif register_button.collidepoint(event.pos):
                        # Appel de la fonction d'enregistrement
                        if username_text and email_text and password_text:  # Vérifier si les champs sont remplis
                            if is_valid_email(email_text):  # Validation de l'e-mail
                                insert_player(conn, username_text, email_text, password_text)
                                username_text = ''
                                email_text = ''
                                password_text = ''
                                conn.close()  # Fermer la connexion
                                pygame.quit()  # Quitter Pygame
                                sys.exit()     # Quitter le programme
                            else:
                                print("L'e-mail doit se terminer par @gmail.com.")
                        else:
                            print("Veuillez remplir tous les champs.")
                    else:
                        if input_box_username.collidepoint(event.pos):
                            active_input = 'username'
                        elif input_box_email.collidepoint(event.pos):
                            active_input = 'email'
                        elif input_box_password.collidepoint(event.pos):
                            active_input = 'password'
                        else:
                            active_input = None

        # Dessin
        screen.fill(WHITE)
        
        # Dessiner les étiquettes
        draw_text("Nom d'utilisateur :", (200, 150))
        draw_text("E-mail :", (200, 220))
        draw_text("Mot de passe :", (200, 290))
        
        # Dessiner les champs de saisie
        pygame.draw.rect(screen, color_active if active_input == 'username' else color_inactive, input_box_username)
        pygame.draw.rect(screen, color_active if active_input == 'email' else color_inactive, input_box_email)
        pygame.draw.rect(screen, color_active if active_input == 'password' else color_inactive, input_box_password)

        # Rendre le texte à l'intérieur des champs de saisie
        draw_text(username_text, (input_box_username.x + 5, input_box_username.y + 5))
        draw_text(email_text, (input_box_email.x + 5, input_box_email.y + 5))
        draw_text('*' * len(password_text), (input_box_password.x + 5, input_box_password.y + 5))  # Cacher le mot de passe

        # Dessiner les boutons
        login_button = pygame.Rect(300, 370, 200, 50)
        register_button = pygame.Rect(300, 440, 200, 50)
        draw_button("Connexion", login_button)
        draw_button("Inscription", register_button)

        pygame.display.flip()

if __name__ == "__main__":
    main()
