import pygame
import threading
import socket

# Variables
HOST = '192.168.1.137' 
PORT = 1234
FONT_SIZE = 32
MESSAGE_LIMIT = 20 

pygame.init()
font = pygame.font.Font(None, FONT_SIZE)

# Classe ChatManager pour gérer le chat
class ChatManager:
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.messages = []

        # Définir la hauteur de la boîte de messages (85% de la hauteur de l'écran)
        self.message_box_height = int(self.height * 0.85)
        self.message_box = pygame.Rect(0, 0, self.width // 6, self.message_box_height)

        # Créer une zone de saisie sous la boîte de messages
        self.input_area_height = self.height - self.message_box_height  # La hauteur restante
        self.input_area = pygame.Rect(0, self.message_box_height, self.width // 6, self.input_area_height)

        # Centrer la boîte de saisie horizontalement dans la zone de saisie
        input_box_width = self.input_area.width - 20
        input_box_height = 40
        self.input_box = pygame.Rect(
            self.input_area.x + (self.input_area.width - input_box_width) // 2,
            self.input_area.y + (self.input_area.height - input_box_height) // 2,
            input_box_width,
            input_box_height
        )

        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''

        # Configuration du socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Demander un pseudonyme
        self.nickname = input("Choisissez un pseudonyme (max 15 caractères) : ")
        self.client.send(self.nickname.encode('utf-8'))

        # Démarrer le thread de réception des messages
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        """Méthode pour recevoir des messages du serveur."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.messages.append(message)
                    if len(self.messages) > MESSAGE_LIMIT:
                        self.messages.pop(0)
            except Exception as e:
                print("Erreur lors de la réception du message :", e)
                self.client.close()
                break

    def handle_event(self, event):
        """Gérer les événements de Pygame, comme les clics et la saisie de texte."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activer ou désactiver la zone de saisie en fonction du clic
            if self.input_box.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.send_message()  # Envoyer le message lors de l'appui sur Entrée
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Effacer le dernier caractère
            elif len(self.text) < 75:
                self.text += event.unicode  # Ajouter le caractère saisi

    def send_message(self):
        """Envoyer le message au serveur si le texte n'est pas vide."""
        if self.text.strip():
            formatted_message = f"{self.nickname}: {self.text}"
            self.client.send(formatted_message.encode('utf-8'))
            self.text = ''

    def render_text(self, text, rect, color):
        """Afficher le texte dans un rectangle spécifique avec un comportement de défilement."""
        txt_surface = font.render(text, True, color)
        
        # Réduire le texte si la largeur dépasse celle du rectangle
        while txt_surface.get_width() > rect.width:
            text = text[1:]
            txt_surface = font.render(text, True, color)

        self.surface.blit(txt_surface, (rect.x + 5, rect.y + (rect.height - txt_surface.get_height()) // 2))

    def wrap_text(self, text, max_width):
        """Découper le texte en plusieurs lignes pour ne pas dépasser une largeur maximale."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            wrapped_lines.append(current_line.strip())

        return wrapped_lines

    def update(self):
        """Mettre à jour l'état (aucune logique supplémentaire ici)."""
        pass

    def draw(self):
        """Dessiner les éléments graphiques à l'écran."""
        # Dessiner la boîte de messages avec une hauteur réduite
        pygame.draw.rect(self.surface, (50, 50, 50), self.message_box)

        # Dessiner les messages
        current_y = self.message_box.y + 5
        for msg in self.messages:
            wrapped_lines = self.wrap_text(msg, self.message_box.width - 10)
            for line in wrapped_lines:
                msg_surface = font.render(line, True, (255, 255, 255))
                self.surface.blit(msg_surface, (self.message_box.x + 5, current_y))
                current_y += msg_surface.get_height() + 2

            current_y += 5
            pygame.draw.line(self.surface, (255, 255, 255), 
                             (self.message_box.x + 5, current_y), 
                             (self.message_box.x + self.message_box.width - 5, current_y), 1)
            current_y += 5

        # Dessiner la zone de saisie sous la boîte de messages
        pygame.draw.rect(self.surface, (60, 60, 60), self.input_area)

        # Dessiner la boîte de saisie centrée dans la zone de saisie
        pygame.draw.rect(self.surface, self.color, self.input_box, 2)
        self.render_text(self.text, self.input_box, self.color)
