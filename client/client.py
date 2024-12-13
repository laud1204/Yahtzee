import socket

class YahtzeeClient:
    def __init__(self, host='127.0.0.1', port=65430):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connexion au serveur réussie.")
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            exit()

    def send_data(self, data):
        try:
            self.client_socket.send(data.encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")

    def receive_data(self):
        try:
            return self.client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Erreur lors de la réception des données: {e}")
            return None

    def handle_input(self, prompt, validation_fn=None):
        while True:
            user_input = input(prompt).strip()
            if validation_fn is None or validation_fn(user_input):
                return user_input
            print("Entrée invalide. Veuillez réessayer.")

    def start_game(self):
        print("Bienvenue dans le jeu de Yahtzee!")
        while True:
            try:
                data = self.receive_data()
                if not data:
                    print("Déconnexion du serveur.")
                    break

                print(data)  # Afficher le message reçu du serveur

                if "Entrez votre nom" in data:
                    user_input = self.handle_input(">> ")
                    self.send_data(user_input)

                elif "Combien de joueurs vont participer?" in data:
                    def validate_player_count(input_str):
                        return input_str.isdigit() and int(input_str) > 1

                    user_input = self.handle_input(">> ", validate_player_count)
                    self.send_data(user_input)

                elif "Voulez-vous relancer des dés" in data:
                    def validate_yes_no(input_str):
                        return input_str.upper() in ['O', 'N']

                    user_input = self.handle_input("(O/N): ", validate_yes_no).upper()
                    self.send_data(user_input)

                elif "Indiquez les indices des dés à relancer" in data:
                    user_input = self.handle_input("Entrez les indices des dés à relancer (ex: 1,3,5 ou rien pour conserver tous les dés): ")
                    self.send_data(user_input)

                elif "Choisissez une figure à remplir" in data:
                    while True:
                        user_input = self.handle_input(">> ")
                        if user_input  in ['1', '2', '3', '4', '5', '6', 'Brelan', 'Petite Suite', 'Grande Suite', 'Full', 'Yahtzee', 'Chance']:
                            break
                        print("Figure invalide. Veuillez réessayer.")
                    self.send_data(user_input)

                elif "Points ajoutés" in data:
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

