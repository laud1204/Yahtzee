import socket
import threading
from tkinter import *


# -------------------------------------------------------------------
# Classe représentant le client Yahtzee.
#
# Cette classe gère les connexions réseau avec les serveurs de jeu et de chat,
# ainsi que la gestion des échanges de données avec le serveur. Elle permet
# également de répondre aux prompts du serveur pendant la partie et d'envoyer
# des messages dans le chat intégré au jeu.
#
# :raises Exception: En cas d'erreur lors de la connexion ou des échanges de données.
# :return: Aucun retour. Gère les interactions avec le serveur et le chat.
# -------------------------------------------------------------------
class YahtzeeClient:
    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    # -------------------------------------------------------------------
    # Établit une connexion avec le serveur Yahtzee pour le jeu.
    #
    # Cette méthode tente de se connecter au serveur de jeu à l'adresse et au
    # port spécifiés. En cas d'échec, elle affiche un message d'erreur et termine
    # le programme.
    #
    # :raises Exception: Si la connexion échoue, une exception est levée.
    # :return: Aucun retour. Affiche un message de succès ou d'échec.
    # -------------------------------------------------------------------

    def connexion(self):
        try:
            self.client_socket.connect((self.host, self.port))  # Connexion au serveur de jeu
            print("Connexion au serveur réussie.")  # Message de confirmation
        except Exception as e:
            print(f"Erreur de connexion : {e}")  # En cas d'échec, affiche l'erreur
            exit()

    # -------------------------------------------------------------------
    # Établit une connexion avec le serveur de chat.
    #
    # Cette méthode tente de se connecter au serveur de chat à l'adresse et
    # au port spécifiés (port + 1). En cas d'échec, elle affiche un message
    # d'erreur et termine le programme.
    #
    # :raises Exception: Si la connexion échoue, une exception est levée.
    # :return: Aucun retour. Affiche un message de succès ou d'échec.
    # -------------------------------------------------------------------

    def connexion_chat(self):
        try:
            self.client_chat_socket.connect((self.host, self.port + 1))  # Connexion au serveur de chat
            print("Connexion au serveur de chat réussie.")  # Message de confirmation
        except Exception as e:
            print(f"Erreur de connexion : {e}")  # En cas d'échec, affiche l'erreur
            exit()

    # -------------------------------------------------------------------
    # Envoie des données encodées au serveur de chat.
    #
    # Cette méthode envoie les données au serveur de chat après les avoir
    # encodées. Elle est utilisée pour l'envoi de messages dans le chat.
    #
    # :raises Exception: Si l'envoi échoue, une exception est levée.
    # :return: Aucun retour. Affiche un message d'erreur en cas de problème.
    # -------------------------------------------------------------------

    def envoyer_donnees_chat(self, data):
        try:
            self.client_chat_socket.send(data.encode())  # Envoie les données encodées
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")  # En cas d'échec, affiche l'erreur

    # -------------------------------------------------------------------
    # Envoie des données encodées au serveur de jeu.
    #
    # Cette méthode envoie les données au serveur de jeu après les avoir
    # encodées. Elle est utilisée pour envoyer des commandes ou des réponses
    # pendant la partie.
    #
    # :raises Exception: Si l'envoi échoue, une exception est levée.
    # :return: Aucun retour. Affiche un message d'erreur en cas de problème.
    # -------------------------------------------------------------------

    def envoyer_donnees(self, data):
        try:
            self.client_socket.send(data.encode())  # Envoie les données encodées
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")  # En cas d'échec, affiche l'erreur

    # -------------------------------------------------------------------
    # Reçoit des données du serveur de chat.
    #
    # Cette méthode reçoit des données envoyées par le serveur de chat,
    # les décode et les retourne pour un traitement ultérieur. Elle est
    # utilisée pour écouter les messages envoyés dans le chat.
    #
    # :raises Exception: Si la réception échoue, une exception est levée.
    # :return: Les données reçues après décodage, ou None en cas d'erreur.
    # -------------------------------------------------------------------

    def recevoir_donnees_chat(self):
        try:
            return self.client_chat_socket.recv(1024).decode()  # Reçoit et décode les données
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")  # En cas d'échec, affiche l'erreur
            return None

    # -------------------------------------------------------------------
    # Reçoit des données du serveur de jeu.
    #
    # Cette méthode reçoit des données envoyées par le serveur de jeu,
    # les décode et les retourne pour un traitement ultérieur. Elle est
    # utilisée pour écouter les messages ou commandes envoyées par le serveur.
    #
    # :raises Exception: Si la réception échoue, une exception est levée.
    # :return: Les données reçues après décodage, ou None en cas d'erreur.
    # -------------------------------------------------------------------

    def recevoir_donnees(self):
        try:
            return self.client_socket.recv(1024).decode()  # Reçoit et décode les données
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")  # En cas d'échec, affiche l'erreur
            return None

    # -------------------------------------------------------------------
    # Gère les saisies utilisateur avec validation optionnelle.
    #
    # Cette méthode permet de saisir des informations de l'utilisateur avec
    # une validation optionnelle de l'entrée. Elle répète la saisie si
    # l'entrée est invalide selon la fonction de validation fournie.
    #
    # :param prompt: Le message à afficher pour inviter l'utilisateur à entrer une donnée.
    # :param validation_fn: Fonction optionnelle pour valider l'entrée de l'utilisateur.
    # :return: La saisie de l'utilisateur si valide.
    # -------------------------------------------------------------------

    def gestion_entree(self, prompt, validation_fn=None):
        while True:
            user_input = input(prompt).strip()  # Demande la saisie utilisateur
            if validation_fn is None or validation_fn(user_input):  # Valide l'entrée si nécessaire
                return user_input  # Retourne la saisie si valide
            print("Entrée invalide. Veuillez réessayer.")  # Si invalide, redemande l'entrée

    # -------------------------------------------------------------------
    # Gère les messages envoyés par le serveur et les réponses du client.
    #
    # Cette méthode traite les messages du serveur, détermine si l'utilisateur
    # doit saisir quelque chose en fonction du message reçu et retourne la saisie
    # appropriée. Elle gère également l'affichage des messages de chat.
    #
    # :param message: Le message reçu du serveur à traiter.
    # :return: La réponse de l'utilisateur ou None si aucun traitement particulier.
    # -------------------------------------------------------------------

    def gestion_prompt(self, message):
        if "Serveur :" in message:  # Si le message provient du serveur de jeu
            # Traite les différents types de prompts envoyés par le serveur
            if "Entrez votre nom" in message:
                return self.gestion_entree(">> ")
            # Autres conditions spécifiques aux messages du serveur (création de partie, etc.)

            elif "Vous souhaitez créer une nouvelle partie ou rejoindre une partie existante?" in message:
                return self.gestion_entree(">> ")
            elif "Choisissez une partie à rejoindre" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 0)
            elif "La partie est déjà pleine" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 0)
            elif "Choix invalide" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 0)
            elif "Combien de joueurs vont participer?" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 1)
            elif "Voulez-vous relancer des dés" in message:
                return self.gestion_entree(">> ", lambda x: x.upper() in ['O', 'N']).upper()
            elif "Indiquez les indices des dés à relancer" in message:
                return self.gestion_entree(
                    "Entrez les indices des dés à relancer (ex: 1,3,5 ou rien pour conserver tous les dés): ")
            elif "Choisissez une figure à remplir" in message:
                return self.gestion_entree(
                    ">> ",
                    lambda x: x.capitalize() in ['1', '2', '3', '4', '5', '6', 'Brelan', 'Petite suite', 'Grande suite',
                                                 'Full', 'Yahtzee', 'Chance', 'Carré']
                ).capitalize()
            else:
                return None  # Aucun traitement particulier
        else:
            # Messages provenant du chat
            print(f"[Chat] {message}")  # Affiche les messages de chat reçus
            return None

    # -------------------------------------------------------------------
    # Gère le déroulement complet du jeu de Yahtzee et l'intégration du chat.
    #
    # Cette méthode gère l'interaction avec le serveur de jeu pendant toute la
    # durée de la partie, en traitant les messages du serveur et en permettant
    # au joueur de répondre aux prompts. Elle permet aussi d'envoyer des messages
    # dans le chat.
    #
    # :return: Aucun retour, gère l'ensemble du jeu et du chat.
    # -------------------------------------------------------------------
    def gestion_jeu(self):
        """
        Gère le déroulement complet du jeu de Yahtzee et l'intégration du chat.
        """
        print("Bienvenue dans le jeu de Yahtzee!")
        print("Vous pouvez écrire 'chat: <votre message>' pour discuter avec les autres joueurs.")
        while True:
            try:
                # Écoute les messages entrants
                data = self.recevoir_donnees()
                if not data:
                    print("Déconnexion du serveur.")
                    break

                # Traite le message reçu
                print(data)
                user_input = self.gestion_prompt(data)
                if user_input is not None:
                    self.envoyer_donnees(user_input)

                # Permet à l'utilisateur d'envoyer des messages de chat à tout moment
                # chat_message = input("Message (laisser vide pour passer) : ").strip()
                # if chat_message.lower().startswith("chat:"):
                #     self.envoyer_donnees(chat_message)

                if "La partie est terminée" in data:
                    print("Merci d'avoir joué!")
                    break

            except Exception as e:
                print(f"Erreur : {e}")
                break

        self.client_socket.close()


# -------------------------------------------------------------------
# Classe représentant l'interface graphique du chat pour Yahtzee.
#
# Cette classe crée une interface graphique utilisant Tkinter, permettant
# à l'utilisateur d'interagir avec le chat du jeu Yahtzee. Elle gère
# l'envoi et la réception de messages ainsi que l'affichage des conversations.
#
# :return: Aucun retour. Lance et gère l'interface graphique du chat.
# -------------------------------------------------------------------

class ChatGUI:
    # -------------------------------------------------------------------
    # Initialise l'interface graphique du chat.
    #
    # Cette méthode crée l'interface graphique du chat en utilisant Tkinter.
    # Elle configure les éléments de l'interface (fenêtre, zone de texte,
    # bouton d'envoi, etc.), initialise le client de jeu Yahtzee, et lance
    # un thread pour gérer le client et la connexion au serveur.
    #
    # :return: Aucun retour. Lance l'interface graphique et le client de jeu.
    # -------------------------------------------------------------------

    def __init__(self):
        self.root = Tk()  # Crée la fenêtre principale de l'interface
        self.root.title("Chat")  # Définit le titre de la fenêtre

        # Définition des couleurs et polices pour l'interface
        BG_COLOR = "#17202A"
        TEXT_COLOR = "#EAECEE"
        FONT = "Helvetica 14"
        FONT_BOLD = "Helvetica 13 bold"

        # Création de la zone de texte pour afficher les messages
        self.txt = Text(self.root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)

        # Création de la zone de saisie pour l'utilisateur
        self.e = Entry(self.root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
        self.e.grid(row=2, column=0)

        # Création du bouton "Send" pour envoyer un message
        send_btn = Button(self.root, text="Send", font=FONT_BOLD, bg="#ABB2B9", command=self.send)
        send_btn.grid(row=2, column=1)

        self.txt.insert(END, "Bienvenue dans le chat de Yahtzee!\n")  # Message d'accueil dans la zone de texte

        # Initialisation du client de jeu Yahtzee et du thread pour le client
        self.client = YahtzeeClient()
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    # -------------------------------------------------------------------
    # Envoie un message dans le chat.
    #
    # Cette méthode récupère le texte saisi par l'utilisateur, l'affiche
    # dans la zone de texte et l'envoie au serveur de chat. Elle efface
    # ensuite la zone de saisie pour préparer un nouveau message.
    #
    # :return: Aucun retour. Le message est envoyé au serveur de chat.
    # -------------------------------------------------------------------

    def send(self):
        user_input = self.e.get()  # Récupère le texte saisi par l'utilisateur
        if user_input.strip():  # Si le message n'est pas vide
            self.txt.insert(END, f"\nVous -> {user_input}")  # Affiche le message dans la zone de texte
            self.client.envoyer_donnees_chat(user_input)  # Envoie le message au serveur de chat
            self.e.delete(0, END)  # Efface le champ de saisie après l'envoi

    # -------------------------------------------------------------------
    # Lance le client et gère les connexions réseau.
    #
    # Cette méthode établit les connexions avec le serveur de jeu et le serveur
    # de chat, puis démarre un thread pour écouter les messages entrants du
    # serveur de chat. Elle lance ensuite la gestion du jeu de Yahtzee.
    #
    # :return: Aucun retour. Démarre le client et la gestion du jeu.
    # -------------------------------------------------------------------

    def run_client(self):
        self.client.connexion()
        self.client.connexion_chat()

        def recevoir_messages():
            print("En attente de messages...")
            while True:
                data = self.client.recevoir_donnees_chat()
                if data:
                    self.txt.insert(END, f"\n{data}")

        threading.Thread(target=recevoir_messages, daemon=True).start()
        self.client.gestion_jeu()

    # -------------------------------------------------------------------
    # Lance la boucle principale de l'interface graphique Tkinter.
    #
    # Cette méthode démarre la boucle d'événements de Tkinter, permettant à
    # l'interface graphique de rester active et de gérer les interactions
    # avec l'utilisateur (envoi de messages, réception de messages, etc.).
    #
    # :return: Aucun retour. Maintient l'interface graphique active.
    # -------------------------------------------------------------------
    def run(self):
        self.root.mainloop()


# Exemple d'exécution (non inclus dans un script si utilisé comme module)
if __name__ == "__main__":
    client = YahtzeeClient()
    client.connexion()
    client.gestion_jeu()
