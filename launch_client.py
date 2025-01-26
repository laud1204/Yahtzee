from client.client import ChatGUI


def demarrer_client():
    gui = ChatGUI()
    gui.run()

if __name__ == "__main__":
    print("Démarrage du client...")
    demarrer_client()
