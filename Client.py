import socket
import threading

class Client:
    def __init__(self, adresse_serveur: str, port: int, nom: str):
        self.adresse_serveur = adresse_serveur
        self.port = port
        self.nom = nom
        self.thread_client = None
        self.client_socket = None

    def se_connecter(self):
        # Connexion au serveur
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.adresse_serveur, self.port))
            print(f"{self.nom} est connecté au serveur à {self.adresse_serveur}:{self.port}")
            self.thread_client = threading.Thread(target=self.recevoir_messages)
            self.thread_client.start()
        except Exception as e:
            print(f"Erreur lors de la connexion au serveur: {e}")

    def envoyer_message(self, message: str):
        # Envoyer un message au serveur
        try:
            if self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def recevoir_messages(self):
        # Recevoir des messages du serveur
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Message du serveur: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
        finally:
            self.client_socket.close()
            print("Connexion fermée avec le serveur")

    def jouer_tour(self):
        # Simule l'action de jouer un tour
        action = input("Entrez votre action (par exemple, 'lancer dés'): ")
        self.envoyer_message(f"{self.nom}: {action}")

    def demarrer_client(self):
        # Démarre le client et se connecte au serveur
        self.se_connecter()
        while True:
            try:
                self.jouer_tour()
            except KeyboardInterrupt:
                print("Déconnexion demandée par l'utilisateur.")
                break
        self.client_socket.close()
