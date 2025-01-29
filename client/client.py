import socket

class YahtzeeClient:
    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        """
        Établit une connexion avec le serveur Yahtzee.
        """
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connexion au serveur réussie.")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            exit()

    def envoyer_donnees(self, data):
        """
        Envoie des données encodées au serveur.
        """
        try:
            self.client_socket.send(data.encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")

    def recevoir_donnees(self):
        """
        Reçoit des données du serveur, les décode et les retourne.
        """
        try:
            return self.client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")
            return None

    def gestion_entree(self, prompt, validation_fn=None):
        """
        Gère les saisies utilisateur avec validation optionnelle.
        """
        while True:
            user_input = input(prompt).strip()
            if validation_fn is None or validation_fn(user_input):
                return user_input
            print("Entrée invalide. Veuillez réessayer.")

    def gestion_prompt(self, message):
        """
        Gère les différents messages envoyés par le serveur et les réponses du client.
        """
        if "Serveur :" in message:
            # Messages système ou liés au jeu
            if "Entrez votre nom" in message:
                return self.gestion_entree(">> ")

            elif "Vous souhaitez créer une nouvelle partie ou rejoindre une partie existante?" in message:
                return self.gestion_entree(">> ")
            elif "Choisissez une partie à rejoindre" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 0)
            elif "Choix invalide. Entrez un nombre valide" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 0)
            elif "Combien de joueurs vont participer?" in message:
                return self.gestion_entree(">> ", lambda x: x.isdigit() and int(x) > 1)
            elif "Voulez-vous relancer des dés" in message:
                return self.gestion_entree(">> ", lambda x: x.upper() in ['O', 'N']).upper()
            elif "Indiquez les indices des dés à relancer" in message:
                return self.gestion_entree("Entrez les indices des dés à relancer (ex: 1,3,5 ou rien pour conserver tous les dés): ")
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


# Exemple d'exécution (non inclus dans un script si utilisé comme module)
if __name__ == "__main__":
    client = YahtzeeClient()
    client.connexion()
    client.gestion_jeu()
