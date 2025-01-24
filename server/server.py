import socket
import threading
import random
import time
from typing import List

from utils.Partie import Partie
class YahtzeeServer:
    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parties : List[Partie] = []
        # self.players = []
        # self.scores = {}
        # self.feuilles_scores = {}  # Associe chaque joueur à une feuille de score
        # self.required_players = None
        # self.game_started = False
        # self.turn_lock = threading.Lock()
        # self.current_turn = 0
        # self.max_turns = 13

    def demarrer(self):
        # -------------------------------------------------------------------
        # Démarre le serveur pour écouter les connexions entrantes des joueurs.
        # -------------------------------------------------------------------
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Le serveur Yahtzee est en écoute sur {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.gerer_joueur, args=(client_socket, addr))
            client_handler.start()



    def gerer_joueur(self, client_socket, addr):
        # -------------------------------------------------------------------
        # Gère la connexion et les interactions avec un joueur donné.
        #
        # :param client_socket: Socket du client.
        # :param addr: Adresse du client.
        # -------------------------------------------------------------------
        try:
            client_socket.send("Serveur : Entrez votre nom:".encode())
            player_name = client_socket.recv(1024).decode().strip()

            client_socket.send("Serveur : Vous souhaitez créer une nouvelle partie ou rejoindre une partie existante? (C/R): ".encode())
            response = client_socket.recv(1024).decode().strip().upper()
            if response == "C":
                client_socket.send("Serveur : Combien de joueurs vont participer? ".encode())
                while True:
                    try:
                        required_players = int(client_socket.recv(1024).decode().strip())
                        if required_players > 1:
                            break
                        else:
                            client_socket.send("Serveur : Le nombre de joueurs doit être au moins 2. Réessayez: ".encode())
                    except ValueError:
                        client_socket.send("Serveur : Entrée invalide. Entrez un nombre entier: ".encode())
                print(f"{player_name} a créé une nouvelle partie pour {required_players} joueurs.")
                partie = Partie(player=player_name, socket=client_socket, required_players=required_players)
                self.parties.append(partie)

                threading.Thread(target=partie.attendre_joueurs).start()

            elif response == "R":
                for i, partie in enumerate(self.parties):

                    client_socket.send(f"Serveur : Partie {i + 1}. {partie.information_partie()}\n".encode())
                client_socket.send("Serveur : Choisissez une partie à rejoindre: ".encode())

                while True:
                    try:
                        # Recevoir et décoder la réponse du client
                        data = client_socket.recv(1024).decode().strip()
                        if not data.isdigit():
                            # Si l'entrée n'est pas un nombre
                            client_socket.send("Serveur : Entrée invalide. Entrez un nombre valide : ".encode())
                            continue

                        # Convertir l'entrée en entier
                        choice = int(data)
                        if 1 <= choice <= len(self.parties):
                            # Si le choix est valide, on sort de la boucle
                            break
                        else:
                            # Si le choix est en dehors de l'intervalle
                            client_socket.send(
                                f"Serveur : Choix invalide. Entrez un nombre entre 1 et {len(self.parties)} : ".encode())
                    except ValueError:
                        # Gestion des erreurs de conversion explicite (peu probable ici grâce à `isdigit()`)
                        client_socket.send("Serveur : Entrée invalide. Entrez un nombre valide : ".encode())
                    except Exception as e:
                        # Pour toute autre exception, fournir un message d'erreur générique et logger l'erreur côté serveur
                        print(f"Erreur inattendue : {e}")
                        client_socket.send("Serveur : Une erreur inattendue s'est produite. Réessayez : ".encode())

                # Si on atteint ici, `choice` est valide
                self.parties[choice - 1].rejoindre_partie(player_name, client_socket)


        except (BrokenPipeError, ConnectionResetError):
            print(f"Le joueur à l'adresse {addr} s'est déconnecté.")




if __name__ == "__main__":
    server = YahtzeeServer()
    server.demarrer()