class CalculateurDeScore:
    # -------------------------------------------------------------------
    # Classe contenant des méthodes statiques pour calculer les scores
    # des différentes figures dans une partie de Yahtzee.
    # -------------------------------------------------------------------

    @staticmethod
    def calculer_un(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '1'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 1.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 1)

    @staticmethod
    def calculer_deux(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '2'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 2.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 2)

    @staticmethod
    def calculer_trois(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '3'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 3.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 3)

    @staticmethod
    def calculer_quatre(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '4'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 4.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 4)

    @staticmethod
    def calculer_cinq(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '5'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 5.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 5)

    @staticmethod
    def calculer_six(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure '6'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés ayant la valeur 6.
        # -------------------------------------------------------------------
        return sum(valeur for valeur in des if valeur == 6)

    @staticmethod
    def calculer_brelan(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Brelan'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés si au moins 3 dés ont la même valeur,
        #          sinon 0.
        # -------------------------------------------------------------------
        for valeur in set(des):
            if des.count(valeur) >= 3:
                return sum(des)
        return 0

    @staticmethod
    def calculer_carre(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Carré'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des dés si au moins 4 dés ont la même valeur,
        #          sinon 0.
        # -------------------------------------------------------------------
        for valeur in set(des):
            if des.count(valeur) >= 4:
                return sum(des)
        return 0

    @staticmethod
    def calculer_full(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Full'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: 25 si les dés contiennent un brelan et une paire,
        #          sinon 0.
        # -------------------------------------------------------------------
        valeurs_uniques = set(des)
        if len(valeurs_uniques) == 2 and any(des.count(valeur) == 3 for valeur in valeurs_uniques):
            return 25
        return 0

    @staticmethod
    def calculer_petite_suite(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Petite suite'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: 30 si les dés contiennent une suite de 4 valeurs
        #          consécutives, sinon 0.
        # -------------------------------------------------------------------
        suites_possibles = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        valeurs_uniques = set(des)
        for suite in suites_possibles:
            if suite.issubset(valeurs_uniques):
                return 30
        return 0

    @staticmethod
    def calculer_grande_suite(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Grande suite'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: 40 si les dés contiennent une suite de 5 valeurs
        #          consécutives, sinon 0.
        # -------------------------------------------------------------------
        suites_possibles = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
        valeurs_uniques = set(des)
        for suite in suites_possibles:
            if suite == valeurs_uniques:
                return 40
        return 0

    @staticmethod
    def calculer_yahtzee(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Yahtzee'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: 50 si tous les dés ont la même valeur, sinon 0.
        # -------------------------------------------------------------------
        if len(set(des)) == 1:
            return 50
        return 0

    @staticmethod
    def calculer_chance(des: list[int]) -> int:
        # -------------------------------------------------------------------
        # Calcule le score pour la figure 'Chance'.
        #
        # :param des: Liste des valeurs des dés.
        # :return: Somme des valeurs des dés.
        # -------------------------------------------------------------------
        return sum(des)