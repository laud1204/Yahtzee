import socket
import threading
from typing import List
from utils.Partie import Partie


# -------------------------------------------------------------------
# Classe représentant le serveur Yahtzee.
#
# Cette classe gère les connexions réseau des joueurs, la création de
# parties, la gestion des joueurs, et la gestion des parties en cours.
# Elle démarre également un serveur de chat pour les interactions entre
# les joueurs.
#
# :return: Aucun retour. Démarre et gère les parties de Yahtzee et le chat.
# -------------------------------------------------------------------

class YahtzeeServer:

    # -------------------------------------------------------------------
    # Initialise le serveur Yahtzee.
    #
    # Cette méthode initialise le serveur en configurant l'adresse et le
    # port de connexion, en créant le socket de serveur et en initialisant
    # une liste de parties.
    #
    # :param host: L'adresse IP du serveur (par défaut '127.0.0.1').
    # :param port: Le port sur lequel le serveur écoute (par défaut 65430).
    # -------------------------------------------------------------------

    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host  # L'adresse IP où le serveur écoute.
        self.port = port  # Le port du serveur pour les connexions des joueurs.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket de serveur.
        self.parties: List[Partie] = []  # Liste des parties en cours.

    # -------------------------------------------------------------------
    # Démarre le serveur pour écouter les connexions des joueurs et du chat.
    #
    # Cette méthode démarre deux threads : un pour gérer les connexions
    # des joueurs et un autre pour démarrer le serveur de chat. Elle
    # écoute les connexions entrantes des joueurs et crée des threads
    # pour gérer chaque connexion.
    #
    # :return: Aucun retour. Lance l'écoute des connexions et la gestion du chat.
    # -------------------------------------------------------------------

    def demarrer(self):
        # Démarre l'écoute des connexions des joueurs.
        def demarrer_jeu():
            self.server_socket.bind((self.host, self.port))  # Lie le serveur à l'adresse et au port spécifiés.
            self.server_socket.listen(5)  # Le serveur commence à écouter les connexions entrantes (max 5).
            print(f"Le serveur Yahtzee est en écoute sur {self.host}:{self.port}")

            # Accepte les connexions des clients et crée un thread pour gérer chaque joueur.
            while True:
                client_socket, addr = self.server_socket.accept()
                client_handler = threading.Thread(target=self.gerer_joueur, args=(client_socket, addr))
                threading.Thread(
                    target=self.supprimer_partie_si_terminee).start()  # Vérifie les parties terminées en parallèle.
                client_handler.start()

        # Démarre le serveur de chat.
        def demarrer_chat():
            chat_server = ChatServer()  # Crée une instance du serveur de chat.
            chat_server.demarrer()  # Lance le serveur de chat.

        threading.Thread(target=demarrer_chat).start()  # Démarre le serveur de chat dans un thread.
        threading.Thread(target=demarrer_jeu).start()  # Démarre le serveur de jeu dans un thread.

    # -------------------------------------------------------------------
    # Gère la connexion et les interactions avec un joueur.
    #
    # Cette méthode permet à un joueur de se connecter, de choisir de
    # créer une nouvelle partie ou de rejoindre une partie existante.
    # Elle gère également l'entrée du nombre de joueurs nécessaires
    # pour la création d'une partie et ajoute la partie à la liste des
    # parties en attente.
    #
    # :param client_socket: Socket du client.
    # :param addr: Adresse du client.
    # :return: Aucun retour. Gère les interactions avec un joueur.
    # -------------------------------------------------------------------
    def gerer_joueur(self, client_socket, addr):
        try:
            client_socket.send("Serveur : Entrez votre nom:".encode())
            player_name = client_socket.recv(1024).decode().strip()

            client_socket.send(
                "Serveur : Vous souhaitez créer une nouvelle partie ou rejoindre une partie existante? (C/R): ".encode())
            response = client_socket.recv(1024).decode().strip().upper()
            if response == "C":
                client_socket.send("Serveur : Combien de joueurs vont participer? ".encode())
                while True:
                    try:
                        required_players = int(client_socket.recv(1024).decode().strip())
                        if required_players > 1:
                            break
                        else:
                            client_socket.send(
                                "Serveur : Le nombre de joueurs doit être au moins 2. Réessayez: ".encode())
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

    # -------------------------------------------------------------------
    # Supprime une partie de la liste des parties si elle est terminée.
    #
    # Cette méthode vérifie chaque partie dans la liste des parties en
    # cours et supprime celles qui sont terminées.
    #
    # :return: Aucun retour. Supprime les parties terminées.
    # -------------------------------------------------------------------

    def supprimer_partie_si_terminee(self):
        parties_terminees = [partie for partie in self.parties if
                             partie.est_terminee()]  # Trouve les parties terminées.
        for partie in parties_terminees:
            self.parties.remove(partie)  # Supprime les parties terminées de la liste.
            print(f"La partie {partie} est terminée et a été supprimée.")


# -------------------------------------------------------------------
# Classe représentant le serveur de chat.
#
# Cette classe gère les connexions réseau des clients de chat et
# permet la communication en temps réel entre les joueurs.
#
# :return: Aucun retour. Gère les connexions et le chat entre les clients.
# -------------------------------------------------------------------

class ChatServer:

    # -------------------------------------------------------------------
    # Initialise le serveur de chat.
    #
    # Cette méthode initialise le serveur de chat en configurant l'adresse
    # et le port de connexion, et en créant le socket de serveur.
    #
    # :param host: L'adresse IP du serveur de chat (par défaut '127.0.0.1').
    # :param port: Le port sur lequel le serveur de chat écoute (par défaut 65431).
    # -------------------------------------------------------------------

    def __init__(self, host='127.0.0.1', port=65431):
        self.host = host  # L'adresse IP du serveur de chat.
        self.port = port  # Le port du serveur de chat pour les connexions.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket du serveur de chat.
        self.clients = []  # Liste des clients connectés au chat.

    # -------------------------------------------------------------------
    # Démarre le serveur de chat pour écouter les connexions des clients.
    #
    # Cette méthode démarre un thread pour écouter les connexions entrantes
    # des clients. Lorsqu'un client se connecte, un thread est créé pour
    # gérer la communication avec ce client.
    #
    # :return: Aucun retour. Lance l'écoute des connexions et gère les clients.
    # -------------------------------------------------------------------

    def demarrer(self):
        def demarrer_chat():
            self.server_socket.bind((self.host, self.port))  # Lie le serveur de chat à l'adresse et au port spécifiés.
            self.server_socket.listen(5)  # Le serveur commence à écouter les connexions (max 5).
            print(f"Le serveur de chat est en écoute sur {self.host}:{self.port}")
            while True:
                client_socket, addr = self.server_socket.accept()  # Accepte les connexions des clients.
                client_handler = threading.Thread(target=self.gerer_chat, args=(
                    client_socket, addr))  # Crée un thread pour gérer chaque client.
                client_handler.start()

        threading.Thread(target=demarrer_chat).start()  # Démarre le serveur de chat dans un thread.

    # -------------------------------------------------------------------
    # Gère la connexion et les interactions avec un client de chat.
    #
    # Cette méthode reçoit les messages d'un client, puis les envoie à
    # tous les autres clients connectés. Elle permet ainsi la communication
    # en temps réel entre les clients du chat.
    #
    # :param client_socket: Socket du client.
    # :param addr: Adresse du client.
    # :return: Aucun retour. Gère les messages et la communication entre les clients.
    # -------------------------------------------------------------------

    def gerer_chat(self, client_socket, addr):
        try:
            print(f"Connexion établie avec {addr}")
            self.clients.append(
                {"name": f"Joueur {len(self.clients) + 1}", "socket": client_socket})  # Ajoute le client à la liste.
            while True:
                data = client_socket.recv(1024).decode()  # Récupère le message du client.
                if not data:
                    break  # Si le client se déconnecte, quitte la boucle.
                print(f"Message de {addr}: {data}")  # Affiche le message du client.
                name = [client["name"] for client in self.clients if client["socket"] == client_socket][
                    0]  # Trouve le nom du client.
                for client in self.clients:  # Envoie le message à tous les autres clients.
                    if client["socket"] != client_socket:
                        try:
                            client["socket"].send(f'{name}: {data}'.encode())
                        except (BrokenPipeError, ConnectionResetError):
                            pass  # Ignore les erreurs si un client est déconnecté.
                            print(f"Le client à l'adresse {addr} s'est déconnecté.")
        except (BrokenPipeError, ConnectionResetError):
            print(f"Le client à l'adresse {addr} s'est déconnecté.")
        finally:
            client_socket.close()  # Ferme la connexion.
            self.clients.remove(client_socket)  # Retire le client de la liste.
            print(f"Connexion avec {addr} fermée.")


if __name__ == "__main__":
    server = YahtzeeServer()
    server.demarrer()
