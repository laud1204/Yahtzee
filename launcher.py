# launcher.py
import os
from server.server import start_server
from client.client import main as start_client

def main():
    print("Bienvenue dans le jeu Yahtzee !")
    print("1. Lancer le serveur")
    print("2. Lancer un client (joueur)")
    choice = input("Entrez votre choix (1 ou 2) : ").strip()

    if choice == "1":
        print("Démarrage du serveur...")
        start_server()
    elif choice == "2":
        print("Démarrage du client...")
        start_client()
    else:
        print("Choix invalide. Relancez le programme et choisissez 1 ou 2.")

if __name__ == "__main__":
    main()
