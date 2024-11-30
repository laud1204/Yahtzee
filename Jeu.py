from De import De
from Joueur import Joueur


class Jeu:
    # -------------------------------------------------------------------
    # Classe gérant le déroulement d'une partie de Yahtzee.
    #
    # Attributs :
    # - FIGURES_VALIDES : Liste des figures valides dans le jeu.
    # - joueurs : Liste des joueurs participant à la partie.
    # - des : Liste de 5 objets De représentant les dés.
    # - tour_actuel : Indique le tour actuel de la partie.
    # -------------------------------------------------------------------

    FIGURES_VALIDES = ['Brelan', 'Carré', 'Full', 'Petite Suite', 'Grande Suite',
                       'Yahtzee', 'Chance', '1', '2', '3', '4', '5', '6']

    def __init__(self, joueurs: list):
        # -------------------------------------------------------------------
        # Initialise un objet Jeu avec les joueurs et les dés.
        #
        # :param joueurs: Liste des joueurs participant à la partie.
        # -------------------------------------------------------------------
        self.joueurs = joueurs  # Liste des joueurs participant au jeu
        self.des = [De() for _ in range(5)]  # Initialisation des dés
        self.tour_actuel = 0  # Tour actuel du jeu

    def lancer_des(self, des_a_relancer: list[int]) -> list[int]:
        # -------------------------------------------------------------------
        # Lance les dés spécifiés par leurs indices.
        #
        # :param des_a_relancer: Liste des indices des dés à relancer.
        # :return: Liste des valeurs des dés après le lancer.
        # -------------------------------------------------------------------
        for i in des_a_relancer:
            if 0 <= i < len(self.des):
                self.des[i].__init__()
        return [de.valeur for de in self.des]

    def effectuer_premier_lancer(self):
        # -------------------------------------------------------------------
        # Effectue le premier lancer avec tous les dés.
        #
        # :return: Liste des valeurs des dés après le premier lancer.
        # -------------------------------------------------------------------
        return self.lancer_des(list(range(5)))

    def effectuer_relancers(self) -> list[int]:
        # -------------------------------------------------------------------
        # Permet au joueur de relancer les dés s'il le souhaite.
        #
        # :return: Liste des valeurs des dés après les relancers.
        # -------------------------------------------------------------------
        lancers_restants = 2
        while lancers_restants > 0:
            choix = input("Voulez-vous relancer des dés ? (oui/non) ").strip().lower()
            if choix == 'non':
                break
            elif choix == 'oui':
                des_a_relancer = self.demander_des_a_relancer()
                self.lancer_des([i - 1 for i in des_a_relancer])
                print(f"Résultat des dés: {[de.valeur for de in self.des]}")
                lancers_restants -= 1
            else:
                print("Veuillez répondre par 'oui' ou 'non'.")
        return [de.valeur for de in self.des]

    def demander_des_a_relancer(self) -> list[int]:
        # -------------------------------------------------------------------
        # Demande au joueur quels dés relancer.
        #
        # :return: Liste des indices des dés que le joueur souhaite relancer.
        # -------------------------------------------------------------------
        while True:
            try:
                des_a_relancer = [int(i) for i in input(
                    "Quels dés voulez-vous relancer (1-5, séparés par des espaces) ? ").split()]
                if all(1 <= i <= 5 for i in des_a_relancer):
                    return list(set(des_a_relancer))  # Supprime les doublons
                else:
                    print("Veuillez entrer des indices valides entre 1 et 5.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer des numéros de dés valides (1-5, séparés par des espaces).")

    def choisir_figure(self, joueur: Joueur, des_actuels: list[int]):
        # -------------------------------------------------------------------
        # Permet au joueur de choisir une figure à remplir ou rayer.
        #
        # :param joueur: Objet Joueur représentant le joueur en cours.
        # :param des_actuels: Liste des valeurs des dés actuels.
        # -------------------------------------------------------------------
        while True:
            figure = input("Quelle figure voulez-vous remplir ou rayer ? ").strip()
            if figure in self.FIGURES_VALIDES:
                if joueur.feuille_score.scores[figure] is None:
                    score = joueur.feuille_score.calculer_score(figure, des_actuels)
                    joueur.feuille_score.noter_score(figure, score)
                    joueur.feuille_score.afficher_score(des_actuels)
                    break
                else:
                    print("Cette figure est déjà remplie. Veuillez en choisir une autre.")
            else:
                print(f"Figure invalide : {figure}. Veuillez entrer une figure valide.")

    def gerer_tour_joueur(self, joueur: Joueur):
        # -------------------------------------------------------------------
        # Gère un tour complet pour un joueur.
        #
        # :param joueur: Objet Joueur représentant le joueur en cours.
        # -------------------------------------------------------------------
        print(f"\nTour de {joueur.nom}")
        des_actuels = self.effectuer_premier_lancer()
        print(f"Résultat des dés: {des_actuels}")
        des_actuels = self.effectuer_relancers()
        print(f"Résultat final des dés: {des_actuels}")
        joueur.feuille_score.afficher_score(des_actuels)
        self.choisir_figure(joueur, des_actuels)

    def tour(self):
        # -------------------------------------------------------------------
        # Gère un tour complet pour tous les joueurs.
        # -------------------------------------------------------------------
        for joueur in self.joueurs:
            self.gerer_tour_joueur(joueur)
        self.tour_actuel += 1

    def afficher_scores(self):
        # -------------------------------------------------------------------
        # Affiche les scores actuels de tous les joueurs.
        # -------------------------------------------------------------------
        print("\nScores actuels des joueurs :")
        for joueur in self.joueurs:
            score_total = sum(score for score in joueur.feuille_score.scores.values() if score is not None)
            print(f"{joueur.nom} : {score_total}")
