import threading
from server.server import YahtzeeServer

def demarrer_serveur():
    server = YahtzeeServer()
    server.demarrer()


if __name__ == "__main__":
    print("Démarrage du serveur...")
    server_thread = threading.Thread(target=demarrer_serveur)
    server_thread.start()