import threading
from server.server import YahtzeeServer


# -------------------------------------------------------------------
# Démarre le serveur Yahtzee dans un thread séparé.
#
# Cette méthode crée une instance du serveur Yahtzee, puis démarre
# son exécution dans un thread séparé. Cela permet au serveur de fonctionner
# en arrière-plan sans bloquer le reste du programme.
#
# :return: Aucun retour. Lance le serveur dans un thread séparé.
# -------------------------------------------------------------------

def demarrer_serveur():
    server = YahtzeeServer()  # Crée une instance du serveur Yahtzee.
    server.demarrer()  # Démarre le serveur pour qu'il écoute les connexions.


if __name__ == "__main__":  # Vérifie si ce script est exécuté directement (et non importé).
    print("Démarrage du serveur...")  # Affiche un message pour informer que le serveur démarre.
    server_thread = threading.Thread(target=demarrer_serveur)  # Crée un thread pour démarrer le serveur.
    server_thread.start()  # Lance le thread qui démarre le serveur.
