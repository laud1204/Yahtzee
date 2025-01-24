from utils.CalculateurDeScore import CalculateurDeScore
from utils.Tableau import Tableau


class FeuilleScore:
    # -------------------------------------------------------------------
    # Classe gérant les scores d'un joueur dans une partie de Yahtzee.
    #
    # Attributs :
    # - scores : Dictionnaire contenant les scores pour chaque figure.
    # - remplissage : Indique quelles figures ont déjà été remplies.
    # -------------------------------------------------------------------

    def __init__(self):
        # -------------------------------------------------------------------
        # Initialise les scores pour chaque figure et l'état de remplissage.
        # - Les scores sont initialisés à None, sauf pour le bonus qui est à 0.
        # - Le remplissage indique si une figure a déjà été utilisée.
        # -------------------------------------------------------------------
        self.scores = {
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': None,
            '6': None,
            'Brelan': None,
            'Carré': None,
            'Full': None,
            'Petite suite': None,
            'Grande suite': None,
            'Yahtzee': None,
            'Chance': None,
            'Bonus Section Supérieure': 0  # Bonus initialisé à 0
        }
        self.remplissage = {key: False for key in self.scores}  # Pour savoir si la figure est remplie ou non

    def noter_score(self, figure: str, valeur: int) -> None:
        # -------------------------------------------------------------------
        # Note le score pour une figure donnée et vérifie le bonus si besoin.
        #
        # :param figure: Nom de la figure à remplir (ex : '1', 'Brelan').
        # :param valeur: Score à attribuer à la figure.
        # -------------------------------------------------------------------
        if figure in self.scores and self.scores[figure] is None:
            self.scores[figure] = valeur
            print(f"Score de {valeur} noté pour la figure {figure}")

            # Vérifie si la figure appartient à la section supérieure
            if figure in ['1', '2', '3', '4', '5', '6']:
                if self.verifier_bonus_section_superieure():
                    print("Félicitations ! Vous avez atteint le bonus de la section supérieure (+35 points)")
        else:
            print(f"Figure {figure} déjà remplie ou inexistante")

    def afficher_score(self, des: list[int]) -> str:
        # -------------------------------------------------------------------
        # Affiche le tableau des scores réalisés et des scores théoriques.
        #
        # :param des: Liste des valeurs des dés actuels pour calculer les scores théoriques.
        # -------------------------------------------------------------------
        scores_theoriques = {
            figure: self.calculer_score(figure, des)
            for figure in self.scores.keys()
            if figure != "Bonus Section Supérieure"
        }

        # Calcul du score global réalisé
        total_score = sum(
            score for score in self.scores.values() if score is not None
        )

        # Prépare les données pour le tableau
        figures_tableau = [
            (
                figure,
                self.scores[figure] if self.scores[figure] is not None else "Non réalisée",
                scores_theoriques.get(figure, "N/A") if figure != "Bonus Section Supérieure" else "N/A",
            )
            for figure in self.scores.keys()
        ]

        tableau = Tableau(headers=["Figure", "Score réalisé", "Score théorique"], data=figures_tableau)
        return tableau.afficher()

    def verifier_bonus_section_superieure(self) -> bool:
        # -------------------------------------------------------------------
        # Vérifie si le joueur a atteint le bonus de la section supérieure.
        #
        # :return: True si le bonus est ajouté, sinon False.
        # -------------------------------------------------------------------
        # Calcul du score total de la section supérieure
        section_sup_score = sum(
            self.scores[str(i)] for i in range(1, 7) if self.scores[str(i)] is not None
        )

        # Ajout du bonus si le score total atteint ou dépasse 63
        if section_sup_score >= 63 and self.scores['Bonus Section Supérieure'] == 0:
            self.scores['Bonus Section Supérieure'] = 35
            return True  # Bonus ajouté
        return False

    def calculer_score(self, figure: str, des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score théorique pour une figure donnée.
        #
        # :param figure: Nom de la figure à calculer (ex : '1', 'Brelan').
        # :param des: Liste des valeurs des dés.
        # :return: Score calculé pour la figure.
        # -------------------------------------------------------------------
        calculateur = CalculateurDeScore()
        if figure == '1':
            return calculateur.calculer_un(des)
        elif figure == '2':
            return calculateur.calculer_deux(des)
        elif figure == '3':
            return calculateur.calculer_trois(des)
        elif figure == '4':
            return calculateur.calculer_quatre(des)
        elif figure == '5':
            return calculateur.calculer_cinq(des)
        elif figure == '6':
            return calculateur.calculer_six(des)
        elif figure == 'Brelan':
            return calculateur.calculer_brelan(des)
        elif figure == 'Carré':
            return calculateur.calculer_carre(des)
        elif figure == 'Full':
            return calculateur.calculer_full(des)
        elif figure == 'Petite suite':
            return calculateur.calculer_petite_suite(des)
        elif figure == 'Grande suite':
            return calculateur.calculer_grande_suite(des)
        elif figure == 'Yahtzee':
            return calculateur.calculer_yahtzee(des)
        elif figure == 'Chance':
            return calculateur.calculer_chance(des)
        else:
            raise ValueError(f"Figure inconnue : {figure}")