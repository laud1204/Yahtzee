import socket
import threading

class Client:
    # -------------------------------------------------------------------
    # Classe représentant un client qui se connecte à un serveur de jeu
    # et interagit avec celui-ci.
    #
    # Attributs :
    # - adresse_serveur : Adresse IP du serveur auquel le client se connecte.
    # - port : Port du serveur.
    # - nom : Nom du client.
    # - thread_client : Thread dédié à la réception des messages du serveur.
    # - client_socket : Socket de communication avec le serveur.
    # -------------------------------------------------------------------

    def __init__(self, adresse_serveur: str, port: int, nom: str):
        # -------------------------------------------------------------------
        # Initialise un client avec l'adresse et le port du serveur,
        # ainsi que le nom du client.
        #
        # :param adresse_serveur: Adresse IP du serveur.
        # :param port: Port du serveur.
        # :param nom: Nom du client.
        # -------------------------------------------------------------------
        self.adresse_serveur = adresse_serveur
        self.port = port
        self.nom = nom
        self.thread_client = None  # Thread pour la réception des messages
        self.client_socket = None  # Socket pour la communication avec le serveur

    def se_connecter(self):
        # -------------------------------------------------------------------
        # Se connecte au serveur et démarre un thread pour recevoir les
        # messages du serveur.
        # -------------------------------------------------------------------
        try:
            # Création de la socket et connexion au serveur
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.adresse_serveur, self.port))
            print(f"{self.nom} est connecté au serveur à {self.adresse_serveur}:{self.port}")

            # Démarrage d'un thread pour recevoir les messages du serveur
            self.thread_client = threading.Thread(target=self.recevoir_messages)
            self.thread_client.start()
        except Exception as e:
            print(f"Erreur lors de la connexion au serveur: {e}")

    def envoyer_message(self, message: str):
        # -------------------------------------------------------------------
        # Envoie un message au serveur.
        #
        # :param message: Message à envoyer au serveur.
        # -------------------------------------------------------------------
        try:
            if self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def recevoir_messages(self):
        # -------------------------------------------------------------------
        # Reçoit et affiche les messages envoyés par le serveur.
        # Ferme la connexion si aucun message n'est reçu.
        # -------------------------------------------------------------------
        try:
            while True:
                # Lecture des données envoyées par le serveur
                data = self.client_socket.recv(1024)
                if not data:  # Si aucun message n'est reçu, arrêter la boucle
                    break
                print(f"Message du serveur: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
        finally:
            # Ferme la connexion avec le serveur
            self.client_socket.close()
            print("Connexion fermée avec le serveur")

    def jouer_tour(self):
        # -------------------------------------------------------------------
        # Simule l'action de jouer un tour en envoyant une action au serveur.
        #
        # Demande une action à l'utilisateur et l'envoie au serveur.
        # -------------------------------------------------------------------
        action = input("Entrez votre action (par exemple, 'lancer dés'): ")
        self.envoyer_message(f"{self.nom}: {action}")

    def demarrer_client(self):
        # -------------------------------------------------------------------
        # Démarre le client, se connecte au serveur et gère les interactions
        # en boucle jusqu'à une interruption de l'utilisateur.
        # -------------------------------------------------------------------
        self.se_connecter()  # Connexion au serveur
        while True:
            try:
                # Demande au client de jouer son tour
                self.jouer_tour()
            except KeyboardInterrupt:
                # Gestion de la déconnexion via Ctrl+C
                print("Déconnexion demandée par l'utilisateur.")
                break
        # Ferme la connexion avec le serveur
        self.client_socket.close()
