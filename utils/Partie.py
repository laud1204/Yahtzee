import random
import threading
import time

from utils.FeuilleScore import FeuilleScore


class Partie:
    def __init__(self, required_players , player, socket ):
        self.players = [{'name': player, 'socket': socket}]
        self.scores = {player : 0}
        self.feuilles_scores = {player : FeuilleScore()}
        self.required_players = required_players
        self.game_started = False
        self.turn_lock = threading.Lock()
        self.current_turn = 0
        self.max_turns = 13
    def information_partie(self):
        return f"Nombre de joueurs: {len(self.players)} / {self.required_players} - Tour actuel: {self.current_turn} / {self.max_turns} - Joueurs: {', '.join([player['name'] for player in self.players])} - Partie commencée: {self.game_started}"
    def broadcast(self, message):
        # -------------------------------------------------------------------
        # Envoie un message à tous les joueurs connectés.
        #
        # :param message: Message à envoyer.
        # -------------------------------------------------------------------
        disconnected_players = []
        for player in self.players:
            try:
                player["socket"].send(message.encode())
            except (BrokenPipeError, ConnectionResetError):
                print(f"Le joueur {player['name']} a été déconnecté.")
                disconnected_players.append(player)

        for player in disconnected_players:
            self.players.remove(player)
            del self.scores[player["name"]]
            del self.feuilles_scores[player["name"]]

    def attendre_joueurs(self):
        # -------------------------------------------------------------------
        # Attend que le nombre requis de joueurs se connecte avant de commencer la partie.
        # -------------------------------------------------------------------
        while len(self.players) < self.required_players:
            self.broadcast(f"Serveur : En attente de {self.required_players - len(self.players)} joueur(s) pour démarrer la partie...\n")
            time.sleep(2)

        self.game_started = True

        self.broadcast("Tous les joueurs sont connectés. La partie commence!\n")
        self.tour()

    def rejoindre_partie(self, player, socket):
        # -------------------------------------------------------------------
        # Ajoute un joueur à la partie.
        #
        # :param player: Nom du joueur à ajouter.
        # :param socket: Socket du joueur à ajouter.
        # -------------------------------------------------------------------
        if len(self.players) >= self.required_players:
            socket.send("Serveur : La partie est déjà pleine.\n".encode())
            return
        self.players.append({'name': player, 'socket': socket})
        self.scores[player] = 0
        self.feuilles_scores[player] = FeuilleScore()
    def tour(self):
        # -------------------------------------------------------------------
        # Gère le déroulement d'un tour pour chaque joueur de la partie.
        #
        # Cette méthode s'assure que chaque joueur joue à tour de rôle. Elle
        # envoie un message au joueur concerné lorsque c'est son tour et appelle
        # la méthode pour effectuer le tour du joueur. Elle augmente le compteur
        # de tours après chaque action. Quand le nombre maximum de tours est
        # atteint, elle appelle la méthode pour annoncer le vainqueur.
        #
        # :param client_socket: Socket du client correspondant au joueur en cours.
        # :param player_name: Nom du joueur en cours.
        # -------------------------------------------------------------------
        while self.current_turn < self.max_turns * len(self.players):
            with self.turn_lock:
                player_index = self.current_turn % len(self.players)
                player_name = self.players[player_index]['name']
                client_socket = self.players[player_index]['socket']
                print(f"{player_name} est en train de jouer.")
                client_socket.send(f"Serveur : C'est votre tour, {player_name}.\n".encode())
                self.jouer_tour(client_socket, player_name)
                self.current_turn += 1

        if self.current_turn >= self.max_turns * len(self.players):
            self.annoncer_vainqueur()

    def jouer_tour(self, client_socket, player_name):
        # -------------------------------------------------------------------
        # Gère le tour d'un joueur, incluant le lancer des dés, les relances,
        # le choix de la figure à remplir et le calcul du score.
        #
        # Cette méthode :
        # - Lance les dés pour le joueur.
        # - Offre au joueur jusqu'à deux relances des dés.
        # - Affiche les résultats après chaque lancer.
        # - Permet au joueur de choisir une figure à remplir avec le score obtenu.
        # - Calcule et enregistre le score pour la figure choisie.
        # - Diffuse les points marqués à tous les joueurs et affiche le tableau des scores.
        #
        # :param client_socket: Socket du client correspondant au joueur en cours.
        # :param player_name: Nom du joueur en cours.
        # -------------------------------------------------------------------
        dice = [random.randint(1, 6) for _ in range(5)]
        client_socket.send(f"Serveur : Résultat initial des dés: {dice}\n".encode())

        for _ in range(2):
            client_socket.send("Serveur : Voulez-vous relancer des dés ? (O/N):".encode())
            response = client_socket.recv(1024).decode().strip().upper()
            if response == "O":
                client_socket.send("Serveur : Indiquez les indices des dés à relancer (ex: 1,3,5):".encode())
                indices = client_socket.recv(1024).decode().strip()
                if indices:
                    indices = list(map(int, indices.split(',')))
                    for i in indices:
                        dice[i - 1] = random.randint(1, 6)
                client_socket.send(f"Serveur : Résultat après relance: {dice}\n".encode())
            else:
                break

        # Correction de la construction de la chaîne à envoyer
        figures_disponibles = [
            figure for figure, score in self.feuilles_scores[player_name].scores.items() if score is None
        ]
        tableau_meilleur_score = self.feuilles_scores[player_name].afficher_score(dice)
        client_socket.send(str(tableau_meilleur_score).encode())
        time.sleep(0.5)
        client_socket.send(("Serveur :  Choisissez une figure à remplir:"+ ",".join(figures_disponibles)+":\n").encode())

        while True:
            figure = client_socket.recv(1024).decode().strip()
            if figure not in self.feuilles_scores[player_name].scores:
                client_socket.send("Serveur : Figure invalide, tour ignoré.\n".encode())
            if self.feuilles_scores[player_name].scores[figure] is not None:
                client_socket.send("Serveur : Figure déjà remplie.\n".encode())
                client_socket.send(
                    ("Serveur :  Choisissez une figure à remplir:" + ",".join(figures_disponibles) + ":\n").encode())

            else:
                break




        score = self.feuilles_scores[player_name].calculer_score(figure, dice)
        self.feuilles_scores[player_name].noter_score(figure, score)
        self.scores[player_name] = sum(
            v for v in self.feuilles_scores[player_name].scores.values() if v is not None
        )
        client_socket.send(f"Serveur : Points ajoutés: {score}. Score total: {self.scores[player_name]}\n".encode())
        self.broadcast(f"{player_name} a marqué {score} points pour la figure {figure}.\n")
        self.afficher_tableauScore()


    def afficher_tableauScore(self):
        # -------------------------------------------------------------------
        # Affiche et diffuse le tableau des scores actuels des joueurs.
        #
        # Cette méthode :
        # - Génère un tableau formaté avec les noms des joueurs et leurs scores respectifs.
        # - Diffuse le tableau des scores à tous les joueurs connectés.
        # - Affiche le tableau des scores sur le serveur.
        #
        # :return: Aucun retour. Le tableau est affiché et diffusé.
        # ------------------------------------------------------------------
        header = f"{'Nom du joueur':<20}{'Score':<10}"
        separator = "-" * len(header)
        rows = [f"{name:<20}{score:<10}" for name, score in self.scores.items()]
        score_table = f"\n{header}\n{separator}\n" + "\n".join(rows) + "\n"
        self.broadcast(score_table)
        print(f"Tableau des scores actuel:\n{score_table}")

    def annoncer_vainqueur(self):
        # -------------------------------------------------------------------
        # Annonce le gagnant de la partie en affichant le tableau final des scores.
        #
        # Cette méthode :
        # - Détermine le joueur avec le score le plus élevé.
        # - Génère un tableau formaté des scores de tous les joueurs.
        # - Diffuse le message final à tous les joueurs connectés avec le nom du gagnant.
        # - Affiche le message final sur le serveur.
        #
        # :return: Aucun retour. Le tableau des scores et le message du gagnant sont diffusés et affichés.
        # -------------------------------------------------------------------
        winner = max(self.scores, key=self.scores.get)
        max_score = self.scores[winner]
        header = f"{'Nom du joueur':<20}{'Score':<10}"
        separator = "-" * len(header)
        rows = [f"{name:<20}{score:<10}" for name, score in self.scores.items()]
        score_table = f"\n{header}\n{separator}\n" + "\n".join(rows) + "\n"
        final_message = "La partie est terminée!\n\n" + score_table
        final_message += f"\nLe gagnant est {winner} avec un score de {max_score} points! Félicitations!\n"
        self.broadcast(final_message)
        print(final_message)