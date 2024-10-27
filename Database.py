import mysql.connector
from mysql.connector import Error
import hashlib

def create_connection():
    """Créer une connexion à la base de données."""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',         
            user='root',     
            password='Pa$$w0rd',  
            database='players'   
        )
        if connection.is_connected():
            print("Connecté à MySQL Server version", connection.get_server_info())
            create_table(connection) 
            return connection
    except Error as e:
        print("Erreur lors de la connexion à MySQL", e)
    return None

def create_table(connection):
    """Créer la table des joueurs si elle n'existe pas."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE player (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usd DECIMAL(10, 2),
            email VARCHAR(255),
            username VARCHAR(50),
            password VARCHAR(255),
            `rank` ENUM('user', 'admin', 'moderator') DEFAULT 'user'
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Valider les changements
        print("Table des joueurs créée ou déjà existante.")
    except Error as e:
        print("Erreur lors de la création de la table", e)
    finally:
        cursor.close()  # S'assurer que le curseur est fermé

def hash_password(password):
    """Hacher un mot de passe pour un stockage sécurisé."""
    return hashlib.sha256(password.encode()).hexdigest()

def insert_player(connection, username, email, password, usd=0.00, rank='user'):
    """Insere un nouveau player dans la table players."""
    hashed_password = hash_password(password)
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO player (username, email, password, usd, `rank`)  -- Escaping `rank`
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (username, email, hashed_password, usd, rank))
        connection.commit()
        print("Player inserted successfully.")
    except Error as e:
        print("Error inserting player", e)
    finally:
        cursor.close()

def get_player(connection, username):
    """Récupérer les détails d'un joueur par son nom d'utilisateur."""
    try:
        cursor = connection.cursor()
        select_query = "SELECT * FROM player WHERE username = %s;"
        cursor.execute(select_query, (username,))
        player = cursor.fetchone()
        if player:
            print("Joueur trouvé :", player)
        else:
            print("Joueur non trouvé.")
    except Error as e:
        print("Erreur lors de la récupération du joueur", e)
    finally:
        cursor.close()

def update_player(connection, username, new_email=None, new_rank=None):
    """Mettre à jour l'email ou le rang d'un joueur."""
    try:
        cursor = connection.cursor()
        update_query = "UPDATE player SET "
        updates = []
        parameters = []

        if new_email:
            updates.append("email = %s")
            parameters.append(new_email)
        if new_rank:
            updates.append("rank = %s")
            parameters.append(new_rank)

        if updates:
            update_query += ", ".join(updates) + " WHERE username = %s;"
            parameters.append(username)
            cursor.execute(update_query, parameters)
            connection.commit()
            print("Joueur mis à jour avec succès.")
        else:
            print("Aucune mise à jour fournie.")
    except Error as e:
        print("Erreur lors de la mise à jour du joueur", e)
    finally:
        cursor.close()

def delete_player(connection, username):
    """Supprimer un joueur par son nom d'utilisateur."""
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM player WHERE username = %s;"
        cursor.execute(delete_query, (username,))
        connection.commit()
        print("Joueur supprimé avec succès.")
    except Error as e:
        print("Erreur lors de la suppression du joueur", e)
    finally:
        cursor.close()

def list_players(connection):
    """Lister tous les joueurs dans la base de données."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM player;")
        players = cursor.fetchall()
        for player in players:
            print(player)
    except Error as e:
        print("Erreur lors de la liste des joueurs", e)
    finally:
        cursor.close()
