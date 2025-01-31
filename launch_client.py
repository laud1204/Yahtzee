from client.client import ChatGUI


# -------------------------------------------------------------------
# Démarre le client de chat.
#
# Cette méthode crée une instance de l'interface graphique du chat
# et lance son exécution. Elle permet ainsi à l'utilisateur d'interagir
# avec le client de chat à travers l'interface graphique.
#
# :return: Aucun retour. Lance l'interface graphique du chat.
# -------------------------------------------------------------------

def demarrer_client():
    gui = ChatGUI()  # Crée une instance de l'interface graphique du chat.
    gui.run()  # Lance l'interface graphique du chat et attend les actions de l'utilisateur.


if __name__ == "__main__":  # Vérifie si ce script est exécuté directement (et non importé).
    print("Démarrage du client...")  # Affiche un message pour informer que le client démarre.
    demarrer_client()  # Appelle la fonction pour démarrer le client de chat.
