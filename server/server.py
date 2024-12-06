import socket
import threading
import random
import time

# Paramètres du serveur
HOST = '127.0.0.1'
PORT = 65430

# Liste des joueurs et leurs scores
players = []
scores = {}
required_players = None  # Nombre de joueurs requis
game_started = False
turn_lock = threading.Lock()
current_turn = 0
max_turns = 6





def wait_for_players():
    """Attend jusqu'à ce que le nombre requis de joueurs soit atteint."""
    global game_started

    while len(players) < required_players:
        broadcast(f"En attente de {required_players - len(players)} joueur(s) pour démarrer la partie...\n")
        time.sleep(2)  # Pause pour éviter une surcharge de messages

    game_started = True
    broadcast("Tous les joueurs sont connectés. La partie commence!\n")


def broadcast(message):
    """Envoie un message à tous les joueurs."""
    disconnected_players = []  # Liste des joueurs déconnectés
    for player in players:
        try:
            player["socket"].send(message.encode())
        except (BrokenPipeError, ConnectionResetError):
            print(f"Le joueur {player['name']} a été déconnecté.")
            disconnected_players.append(player)

    # Supprimer les joueurs déconnectés
    for player in disconnected_players:
        players.remove(player)
        del scores[player["name"]]


def handle_client(client_socket, addr):
    """Gère les interactions avec un joueur individuel."""
    global scores, current_turn, required_players

    try:
        # Enregistrer le joueur
        client_socket.send("Entrez votre nom:".encode())
        player_name = client_socket.recv(1024).decode().strip()

        with turn_lock:
            # Si c'est le premier joueur, demander combien de joueurs sont requis
            if not players:
                client_socket.send("Vous êtes le premier joueur connecté. Combien de joueurs vont participer? ".encode())
                while True:
                    try:
                        required_players = int(client_socket.recv(1024).decode().strip())
                        if required_players > 1:
                            break
                        else:
                            client_socket.send("Le nombre de joueurs doit être au moins 2. Réessayez: ".encode())
                    except ValueError:
                        client_socket.send("Entrée invalide. Entrez un nombre entier: ".encode())

                print(f"Nombre de joueurs requis: {required_players}")

            players.append({"name": player_name, "socket": client_socket})
            scores[player_name] = 0

        print(f"{player_name} a rejoint depuis {addr}.")

        broadcast(f"{player_name} a rejoint la partie. Joueurs actuels: {[p['name'] for p in players]}")

        # Démarrer le jeu si le nombre requis de joueurs est atteint
        if len(players) == required_players and not game_started:
            threading.Thread(target=wait_for_players).start()

        while not game_started:
            time.sleep(1)  # Attendre que la partie commence

        # Déroulement du jeu
        while True:
            with turn_lock:
                if current_turn >= max_turns * len(players):
                    break  # Fin de la partie

                player_index = current_turn % len(players)
                if players[player_index]["socket"] == client_socket:
                    client_socket.send(f"C'est votre tour, {player_name}.\n".encode())
                    play_turn(client_socket, player_name)
                    current_turn += 1

        # Annonce du gagnant après la fin de tous les tours (un seul joueur doit envoyer ce message)
        if current_turn >= max_turns * len(players) and len(players) > 0:
            with turn_lock:
                # Calculer le gagnant
                winner = max(scores, key=scores.get)
                max_score = scores[winner]

                # Diffuser le résultat final
                final_message = "La partie est terminée!\n\n"
                final_message += "Tableau des scores:\n" + "\n".join([f"{name}: {score}" for name, score in scores.items()])
                final_message += f"\n\nLe gagnant est {winner} avec un score de {max_score} points! Félicitations!\n"
                broadcast(final_message)
                print(final_message)  # Afficher également sur le serveur

    except (BrokenPipeError, ConnectionResetError):
        print(f"Le joueur à l'adresse {addr} s'est déconnecté.")
    finally:
        # Supprimer le joueur de la liste s'il est déconnecté
        with turn_lock:
            for player in players:
                if player["socket"] == client_socket:
                    players.remove(player)
                    del scores[player["name"]]
                    break
        client_socket.close()


def play_turn(client_socket, player_name):
    """Effectue le tour d'un joueur."""
    dice = [random.randint(1, 6) for _ in range(5)]
    client_socket.send(f"Résultat initial des dés: {dice}\n".encode())

    for _ in range(2):  # Jusqu'à 2 relancers
        client_socket.send("Voulez-vous relancer des dés ? (O/N)".encode())
        response = client_socket.recv(1024).decode().strip().upper()
        if response == "O":
            client_socket.send("Indiquez les indices des dés à relancer (ex: 1,3,5):".encode())
            indices = client_socket.recv(1024).decode().strip()
            indices = list(map(int, indices.split(',')))
            for i in indices:
                dice[i - 1] = random.randint(1, 6)
            client_socket.send(f"Résultat après relance: {dice}\n".encode())
        else:
            break

    client_socket.send("Choisissez un chiffre (1-6) à comptabiliser:".encode())
    choice = int(client_socket.recv(1024).decode().strip())
    score = dice.count(choice) * choice
    scores[player_name] += score
    client_socket.send(f"Points ajoutés: {score}. Score total: {scores[player_name]}\n".encode())
    broadcast(f"{player_name} a marqué {score} points. Total: {scores[player_name]}.\n")

    # Générer et diffuser le tableau des scores
    score_table = "Tableau des scores:\n" + "\n".join([f"{name}: {score}" for name, score in scores.items()])
    broadcast(score_table + "\n")

    # Afficher le tableau des scores dans la console du serveur
    print(f"Tour terminé. Tableau des scores actuel:\n{score_table}")


def start_server():
    """Démarre le serveur."""
    global current_turn

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Le serveur Yahtzee est en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


