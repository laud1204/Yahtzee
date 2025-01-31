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


    def demarrer(self):
        # -------------------------------------------------------------------
        # Démarre le serveur pour écouter les connexions entrantes des joueurs.
        # -------------------------------------------------------------------
        def demarrer_jeu():
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Le serveur Yahtzee est en écoute sur {self.host}:{self.port}")

            while True:
                client_socket, addr = self.server_socket.accept()
                client_handler = threading.Thread(target=self.gerer_joueur, args=(client_socket, addr))
                threading.Thread(target=self.supprimer_partie_si_terminee).start()
                client_handler.start()

        def demarrer_chat():
            chat_server = ChatServer()
            chat_server.demarrer()



        threading.Thread(target=demarrer_chat).start()
        threading.Thread(target=demarrer_jeu).start()






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
                        if 1 <= choice <= len(self.parties) and self.parties[choice - 1].peut_rejoindre():
                            # Si le choix est valide, on sort de la boucle
                            self.parties[choice - 1].rejoindre_partie(player_name, client_socket)

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





        except (BrokenPipeError, ConnectionResetError):
            print(f"Le joueur à l'adresse {addr} s'est déconnecté.")
    def supprimer_partie_si_terminee(self):
        # -------------------------------------------------------------------
        # Supprime une partie de la liste des parties si elle
        # est terminée.
        # -------------------------------------------------------------------
        parties_terminees = [partie for partie in self.parties if partie.est_terminee()]
        for partie in parties_terminees:
            self.parties.remove(partie)
            print(f"La partie {partie} est terminée et a été supprimée.")



class ChatServer:
    def __init__(self, host='127.0.0.1', port=65431):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []

    def demarrer(self):
        # -------------------------------------------------------------------
        # Démarre le serveur pour écouter les connexions entrantes des clients.
        # -------------------------------------------------------------------
        def demarrer_chat():
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Le serveur de chat est en écoute sur {self.host}:{self.port}")

            while True:
                client_socket, addr = self.server_socket.accept()
                client_handler = threading.Thread(target=self.gerer_chat, args=(client_socket, addr))
                client_handler.start()

        threading.Thread(target=demarrer_chat).start()

    def gerer_chat(self, client_socket, addr):
        # -------------------------------------------------------------------
        # Gère la connexion et les interactions avec un client donné.
        #
        # :param client_socket: Socket du client.
        # :param addr: Adresse du client.
        # -------------------------------------------------------------------
        try:
            print(f"Connexion établie avec {addr}")
            self.clients.append({"name": f"Joueur {len(self.clients) + 1}", "socket": client_socket})
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Message de {addr}: {data}")
                print()
                # trouver le nom du client qui a envoyé le message
                name = [client["name"] for client in self.clients if client["socket"] == client_socket][0]
                for client in self.clients:
                    if client["socket"] != client_socket:
                        try:
                            client["socket"].send(f'{name}: {data}'.encode())
                        except (BrokenPipeError, ConnectionResetError):
                            pass

                            print(f"Le client à l'adresse {addr} s'est déconnecté.")
        except (BrokenPipeError, ConnectionResetError):
            print(f"Le client à l'adresse {addr} s'est déconnecté.")
        finally:
            client_socket.close()
            try:

                self.clients.remove(client_socket)
            except:
                pass
            print(f"Connexion avec {addr} fermée.")





if __name__ == "__main__":
    server = YahtzeeServer()
    server.demarrer()