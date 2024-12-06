import socket

# Paramètres du client
HOST = '127.0.0.1'
PORT = 65430


def main():
    """Client de jeu."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print("Bienvenue dans le jeu de Yahtzee!")
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break  # Déconnexion du serveur

            print(data)  # Afficher le message reçu du serveur

            # Cas spécifiques pour les actions demandées par le serveur
            if "Entrez votre nom" in data:
                user_input = input(">> ")
                client.send(user_input.encode())
            elif "Combien de joueurs vont participer?" in data:
                while True:
                    try:
                        user_input = input(">> ")
                        if int(user_input) > 1:
                            client.send(user_input.encode())
                            break
                        else:
                            print("Le nombre de joueurs doit être au moins 2.")
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer un nombre entier.")
            elif "Voulez-vous relancer des dés" in data:
                user_input = input("(O/N): ").strip().upper()
                while user_input not in ['O', 'N']:
                    user_input = input("Réponse invalide. (O/N): ").strip().upper()
                client.send(user_input.encode())
            elif "Indiquez les indices des dés à relancer" in data:
                user_input = input("Entrez les indices des dés à relancer (ex: 1,3,5 ou rien pour conserver tous les dés): ").strip()
                client.send(user_input.encode())
            elif "Choisissez un chiffre" in data:
                user_input = input("Entrez un chiffre (1-6): ").strip()
                while not user_input.isdigit() or int(user_input) not in range(1, 7):
                    user_input = input("Entrée invalide. Entrez un chiffre entre 1 et 6: ").strip()
                client.send(user_input.encode())
            elif "La partie est terminée" in data:
                print("Merci d'avoir joué!")
                break
            else:
                # Si le message ne nécessite pas de réponse utilisateur
                continue

        except Exception as e:
            print(f"Erreur: {e}")
            break

    client.close()


if __name__ == "__main__":
    main()
