import threading
from server.server import YahtzeeServer
from client.client import YahtzeeClient

def demarrer_serveur():
    server = YahtzeeServer()
    server.demarrer()

def demarrer_client():
    client = YahtzeeClient()
    client.connexion()
    client.gestion_jeu()

def main():
    print("Bienvenue dans le jeu Yahtzee !")
    print("1. Lancer le serveur")
    print("2. Lancer un client (joueur)")
    choice = input("Entrez votre choix (1 ou 2) : ").strip()

    if choice == "1":
        print("Démarrage du serveur...")
        server_thread = threading.Thread(target=demarrer_serveur)
        server_thread.start()
    elif choice == "2":
        print("Démarrage du client...")
        demarrer_client()
    else:
        print("Choix invalide. Relancez le programme et choisissez 1 ou 2.")

if __name__ == "__main__":
    main()