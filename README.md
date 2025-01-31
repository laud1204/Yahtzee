# **Yahtzee - Jeu Multijoueur en Python**

## **Description**
Ce projet est une implémentation en Python du célèbre jeu de dés **Yahtzee**, où plusieurs joueurs peuvent se connecter à un serveur central pour jouer ensemble. Le programme est divisé en deux composants : un **serveur** qui gère le jeu et des **clients** qui représentent les joueurs.

---

## **Structure du projet**
Le projet est structuré comme suit :

```
Yahtzee/
│
├── server/
│   ├── server.py         # Code du serveur
│
├── client/
│   ├── client.py         # Code du client (joueur)
│
├── utils/
│   ├── score.py          # Gestion des scores
│   ├── tableau.py        # Affichage des scores
│
├── launch_server.py      # Script pour démarrer le serveur
├── launch_client.py      # Script pour démarrer un client
├── README.md             # Documentation (ce fichier)
```

---

## **Installation**
1. **Cloner le projet :**
   ```bash
   git clone https://github.com/votre-utilisateur/Yahtzee.git
   cd Yahtzee
   ```

2. **Vérifier l'environnement Python :**
    - Assurez-vous d'avoir **Python 3.8** ou une version ultérieure installée.

3. **Installer les dépendances (si nécessaire) :**
    - Ce projet n'a pas de dépendances externes pour l'instant, mais assurez-vous que Python est bien configuré.

---

## **Exécution**

### **Étape 1 : Lancer le serveur**
Sur la machine qui hébergera le serveur, exécutez :
```bash
python launch_server.py
```
Le serveur démarre et attend que les joueurs se connectent.

### **Étape 2 : Lancer un client**
Sur une autre machine (ou la même), lancez :
```bash
python launch_client.py
```
Le client demandera l'adresse IP du serveur et d'autres informations nécessaires pour rejoindre la partie.

---

## **Règles du jeu**
- Chaque joueur peut lancer 5 dés et relancer certains dés jusqu'à 2 fois par tour.
- Après 3 lancers maximum, le joueur choisit un chiffre à comptabiliser pour son score.
- Le jeu se termine après un nombre fixe de tours pour chaque joueur.
- Le serveur calcule le score total et annonce le gagnant à la fin de la partie.

---

## **Notes importantes**
1. **Multijoueur :** Ce jeu fonctionne en mode multijoueur. Assurez-vous que le serveur est actif avant de lancer des clients.
2. **Déconnexion :** Si un joueur se déconnecte, son score est retiré, mais le jeu continue pour les autres participants.
3. **Debugging :** Si vous rencontrez des erreurs, assurez-vous que tous les scripts sont dans leurs emplacements respectifs (`server/`, `client/`, `utils/`).

---

## **Auteur**
- Créé par : Lauretta Delmas, Bastien Cabanié, Oussama Guelagli
---

