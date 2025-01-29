from client.client import YahtzeeClient

def demarrer_client():
    client = YahtzeeClient()
    client.connexion()
    client.gestion_jeu()

if __name__ == "__main__":
    print("Démarrage du client...")
    demarrer_client()
