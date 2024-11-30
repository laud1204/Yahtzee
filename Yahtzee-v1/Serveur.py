import socket
import threading
from multiprocessing import Process

class Serveur:
    # -------------------------------------------------------------------
    # Classe représentant un serveur de jeu pour gérer les connexions
    # clients et les communications dans une partie de Yahtzee.
    #
    # Attributs :
    # - adresse : Adresse IP du serveur.
    # - port : Port d'écoute du serveur.
    # - clients : Liste des clients connectés au serveur.
    # - jeu : Instance du jeu Yahtzee associée au serveur (non implémentée ici).
    # - processus_serveur : Processus indépendant pour faire fonctionner
    #   le serveur en arrière-plan.
    # -------------------------------------------------------------------

    def __init__(self, adresse: str, port: int):
        # -------------------------------------------------------------------
        # Initialise le serveur avec une adresse IP et un port.
        #
        # :param adresse: Adresse IP du serveur.
        # :param port: Port d'écoute du serveur.
        # -------------------------------------------------------------------
        self.adresse = adresse
        self.port = port
        self.clients = []  # Liste des clients connectés
        self.jeu = None  # Instance du jeu Yahtzee
        self.processus_serveur = None  # Processus pour le serveur

    def attendre_connexions(self):
        # -------------------------------------------------------------------
        # Attend les connexions entrantes des clients.
        #
        # Configure une socket d'écoute pour accepter les connexions et
        # démarre un thread dédié pour chaque client.
        # -------------------------------------------------------------------
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.adresse, self.port))
            s.listen()
            print(f"Serveur en attente de connexions sur {self.adresse}:{self.port}")

            while True:
                # Accepte une connexion client
                client_socket, client_address = s.accept()
                print(f"Connexion acceptée de {client_address}")

                # Crée un thread pour gérer la connexion client
                client_thread = threading.Thread(target=self.gerer_connexion_client, args=(client_socket,))
                client_thread.start()

                # Ajoute la socket du client à la liste des clients
                self.clients.append(client_socket)

    def gerer_connexion_client(self, client_socket):
        # -------------------------------------------------------------------
        # Gère les communications avec un client connecté.
        #
        # Lit les messages envoyés par le client et renvoie une réponse
        # appropriée. Ferme la connexion lorsque le client se déconnecte.
        #
        # :param client_socket: Socket représentant la connexion client.
        # -------------------------------------------------------------------
        try:
            while True:
                # Reçoit un message du client
                message = self.recevoir_message(client_socket)
                if not message:  # Si le message est vide, arrêter la connexion
                    break
                print(f"Message reçu: {message}")

                # Envoie une réponse au client
                self.envoyer_message(client_socket, f"Echo: {message}")
        except Exception as e:
            print(f"Erreur lors de la gestion du client: {e}")
        finally:
            # Ferme la connexion avec le client
            client_socket.close()
            print("Connexion fermée avec le client")

    def envoyer_message(self, client_socket, message: str):
        # -------------------------------------------------------------------
        # Envoie un message au client.
        #
        # :param client_socket: Socket représentant la connexion client.
        # :param message: Message à envoyer au client.
        # -------------------------------------------------------------------
        try:
            client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def recevoir_message(self, client_socket) -> str:
        # -------------------------------------------------------------------
        # Reçoit un message envoyé par un client.
        #
        # :param client_socket: Socket représentant la connexion client.
        # :return: Le message reçu sous forme de chaîne de caractères,
        #          ou une chaîne vide en cas d'erreur.
        # -------------------------------------------------------------------
        try:
            data = client_socket.recv(1024)  # Reçoit jusqu'à 1024 octets
            return data.decode('utf-8') if data else ""
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return ""

    def demarrer_serveur(self):
        # -------------------------------------------------------------------
        # Démarre le serveur en tant que processus indépendant.
        #
        # Cette méthode lance un processus distinct pour gérer les connexions
        # entrantes, permettant ainsi au serveur de fonctionner en arrière-plan.
        # -------------------------------------------------------------------
        self.processus_serveur = Process(target=self.attendre_connexions)
        self.processus_serveur.start()
        print("Serveur démarré en tant que processus indépendant")
