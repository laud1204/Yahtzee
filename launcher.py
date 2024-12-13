import threading
from server.server import YahtzeeServer
from client.client import YahtzeeClient

def start_server():
    server = YahtzeeServer()
    server.start_server()

def start_client():
    client = YahtzeeClient()
    client.connect()
    client.start_game()

def main():
    print("Bienvenue dans le jeu Yahtzee !")
    print("1. Lancer le serveur")
    print("2. Lancer un client (joueur)")
    choice = input("Entrez votre choix (1 ou 2) : ").strip()

    if choice == "1":
        print("Démarrage du serveur...")
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
    elif choice == "2":
        print("Démarrage du client...")
        start_client()
    else:
        print("Choix invalide. Relancez le programme et choisissez 1 ou 2.")

if __name__ == "__main__":
    main()
