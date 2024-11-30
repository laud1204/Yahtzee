import socket
import threading
from multiprocessing import Process

class Serveur:
    def __init__(self, adresse: str, port: int):
        self.adresse = adresse
        self.port = port
        self.clients = []  # Liste des clients connectés
        self.jeu = None  # Instance du jeu Yahtzee
        self.processus_serveur = None  # Processus pour le serveur

    def attendre_connexions(self):
        # Créer une socket d'écoute pour accepter les connexions des clients
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.adresse, self.port))
            s.listen()
            print(f"Serveur en attente de connexions sur {self.adresse}:{self.port}")

            while True:
                client_socket, client_address = s.accept()
                print(f"Connexion acceptée de {client_address}")
                client_thread = threading.Thread(target=self.gerer_connexion_client, args=(client_socket,))
                client_thread.start()
                self.clients.append(client_socket)

    def gerer_connexion_client(self, client_socket):
        # Gérer les communications avec un client
        try:
            while True:
                message = self.recevoir_message(client_socket)
                if not message:
                    break
                print(f"Message reçu: {message}")
                self.envoyer_message(client_socket, f"Echo: {message}")
        except Exception as e:
            print(f"Erreur lors de la gestion du client: {e}")
        finally:
            client_socket.close()
            print("Connexion fermée avec le client")

    def envoyer_message(self, client_socket, message: str):
        # Envoyer un message au client
        try:
            client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def recevoir_message(self, client_socket) -> str:
        # Recevoir un message du client
        try:
            data = client_socket.recv(1024)
            return data.decode('utf-8') if data else ""
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return ""

    def demarrer_serveur(self):
        # Démarrer le serveur en tant que processus indépendant
        self.processus_serveur = Process(target=self.attendre_connexions)
        self.processus_serveur.start()
        print("Serveur démarré en tant que processus indépendant")