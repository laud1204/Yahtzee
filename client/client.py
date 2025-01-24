
import socket

class YahtzeeClient:
    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        # -------------------------------------------------------------------
        # Établit une connexion avec le serveur Yahtzee.
        #
        # Cette méthode tente de se connecter au serveur en utilisant l'adresse
        # et le port spécifiés. En cas d'échec, elle affiche un message d'erreur
        # et termine le programme.
        #
        # :raises Exception: En cas d'erreur de connexion.
        # :return: Aucun retour. Affiche un message de succès ou d'erreur.
        # -------------------------------------------------------------------
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connexion au serveur réussie.")
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            exit()

    def envoyer_donnees(self, data):
        # -------------------------------------------------------------------
        # Envoie des données au serveur.
        #
        # Cette méthode envoie une chaîne de caractères encodée au serveur via
        # la socket client. En cas d'erreur, elle affiche un message d'erreur.
        #
        # :param data: Les données sous forme de chaîne à envoyer au serveur.
        # :raises Exception: En cas d'erreur lors de l'envoi des données.
        # :return: Aucun retour. Affiche un message en cas d'erreur.
        # -------------------------------------------------------------------
        try:
            self.client_socket.send(data.encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")

    def recevoir_donnees(self):
        # -------------------------------------------------------------------
        # Reçoit des données du serveur.
        #
        # Cette méthode attend de recevoir des données depuis le serveur via
        # la socket client. Elle décode les données reçues et les retourne.
        # En cas d'erreur, elle affiche un message d'erreur et retourne None.
        #
        # :return: Les données reçues sous forme de chaîne, ou None en cas d'erreur.
        # :raises Exception: En cas d'erreur lors de la réception des données.
        # -------------------------------------------------------------------
        try:
            return self.client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Erreur lors de la réception des données: {e}")
            return None

    def gestion_entree(self, prompt, validation_fn=None):
        # -------------------------------------------------------------------
        # Gère la saisie utilisateur avec une option de validation.
        #
        # Cette méthode affiche une invite utilisateur, attend une saisie,
        # et valide cette saisie avec une fonction de validation optionnelle.
        # Si la validation échoue, elle demande à l'utilisateur de réessayer.
        #
        # :param prompt: Texte affiché pour l'invite de saisie.
        # :param validation_fn: Fonction de validation (optionnelle) prenant la saisie
        #                       utilisateur et retournant True si elle est valide.
        # :return: La saisie utilisateur validée.
        # -------------------------------------------------------------------
        while True:
            user_input = input(prompt).strip()
            if validation_fn is None or validation_fn(user_input):
                return user_input
            print("Entrée invalide. Veuillez réessayer.")

    def gestion_jeu(self):
        # -------------------------------------------------------------------
        # Gère le déroulement du jeu de Yahtzee côté client.
        #
        # Cette méthode communique en continu avec le serveur pour gérer les
        # interactions du joueur, y compris la saisie du nom, le choix du nombre
        # de joueurs, le relancer des dés, le choix des figures à remplir, et
        # l'affichage des messages et scores reçus du serveur.
        #
        # La méthode gère également la déconnexion et les éventuelles erreurs
        # de communication avec le serveur.
        #
        # :raises Exception: Capture et affiche les erreurs de communication
        #                    ou d'exécution.
        # -------------------------------------------------------------------
        print("Bienvenue dans le jeu de Yahtzee!")
        while True:
            try:
                data = self.recevoir_donnees()
                if not data:
                    print("Déconnexion du serveur.")
                    break

                print(data.replace("Serveur : ", ""))
                if data.startswith("Serveur : "):
                    if "Entrez votre nom" in data:
                        user_input = self.gestion_entree(">> ")
                        self.envoyer_donnees(user_input)

                    if "Vous souhaitez créer une nouvelle partie ou rejoindre une partie existante?" in data:
                        user_input = self.gestion_entree(">> ")
                        self.envoyer_donnees(user_input)

                    if "Combien de joueurs vont participer?" in data:
                        def validate_player_count(input_str):
                            return input_str.isdigit() and int(input_str) > 1

                        user_input = self.gestion_entree(">> ", validate_player_count)
                        self.envoyer_donnees(user_input)
                    if "Choisissez une partie à rejoindre" in data:
                        user_input = self.gestion_entree(">> ")
                        self.envoyer_donnees(user_input)
                    if "Choix invalide. Réessayez." in data:
                        user_input = self.gestion_entree(">> ")
                        self.envoyer_donnees(user_input)
                    if "Entrée invalide. Entrez un nombre entier supérieur à 1." in data:
                        user_input = self.gestion_entree(">> ")
                        self.envoyer_donnees(user_input)

                    if "Voulez-vous relancer des dés" in data:
                        def validate_yes_no(input_str):
                            return input_str.upper() in ['O', 'N']

                        user_input = self.gestion_entree("(O/N): ", validate_yes_no).upper()
                        self.envoyer_donnees(user_input)

                    if "Indiquez les indices des dés à relancer" in data:
                        user_input = self.gestion_entree("Entrez les indices des dés à relancer (ex: 1,3,5 ou rien pour conserver tous les dés): ")
                        self.envoyer_donnees(user_input)

                    if "Choisissez une figure à remplir" in data:
                        while True:
                            user_input = self.gestion_entree(">> ")
                            user_input = user_input.capitalize()
                            if user_input  in ['1', '2', '3', '4', '5', '6', 'Brelan', 'Petite Suite', 'Grande Suite', 'Full', 'Yahtzee', 'Chance', "Carré"]:
                                break
                            print("Figure invalide. Veuillez réessayer.")
                        self.envoyer_donnees(user_input)

                    if "Points ajoutés" in data:
                        print(data)

                    elif "Tableau des scores" in data:
                        print(data)

                    elif "La partie est terminée" in data:
                        print("Merci d'avoir joué!")
                        break

            except Exception as e:
                print(f"Erreur: {e}")
                break

        self.client_socket.close()
