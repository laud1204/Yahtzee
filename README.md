# **Yahtzee - Jeu Multijoueur en Python**

## **Description**
Ce projet est une implémentation en Python du célèbre jeu de dés **Yahtzee**, où plusieurs joueurs peuvent se connecter à un serveur central pour jouer ensemble. Le programme vous permet de choisir si vous voulez être un serveur ou un joueur (client).

---

## **Structure du projet**
Le projet est structuré comme suit :

```
Yahtzee-v1/
│
├── server/
│   ├── server.py         # Code du serveur
│
├── client/
│   ├── client.py         # Code du client (joueur)
│
├── launcher.py           # Script principal pour lancer le serveur ou un joueur
├── README.md             # Documentation (ce fichier)
```

---

## **Installation**
1. **Cloner le projet :**
   ```bash
   git clone https://github.com/votre-utilisateur/Yahtzee-v1.git
   cd Yahtzee-v1
   ```

2. **Vérifier l'environnement Python :**
    - Assurez-vous d'avoir **Python 3.8** ou une version ultérieure installée.

3. **Installer les dépendances (si nécessaires) :**
    - Ce projet n'a pas de dépendances externes pour l'instant, mais assurez-vous que Python est bien configuré.

---

## **Exécution**

### **Étape 1 : Lancer le Launcher**
Le fichier `launcher.py` est utilisé pour décider si vous voulez exécuter le serveur ou devenir un joueur. Lancer le script :

```bash
python launcher.py
```

### **Étape 2 : Choisissez une option**
Le programme affichera le menu suivant :
```
Bienvenue dans le jeu Yahtzee !
1. Lancer le serveur
2. Lancer un client (joueur)
Entrez votre choix (1 ou 2) :
```

#### **Option 1 : Lancer le serveur**
- Si vous choisissez l'option **1**, le serveur démarrera.
- Une fois lancé, le serveur attend que les joueurs se connectent.
- **Astuce :** Notez l'adresse IP de la machine exécutant le serveur si les clients se connectent depuis d'autres machines.

#### **Option 2 : Lancer un client (joueur)**
- Si vous choisissez l'option **2**, le client démarrera.
- Entrez votre nom lorsque demandé, puis suivez les instructions affichées dans le terminal pour jouer.

---

## **Exemple de scénario**

### **1. Serveur**
- Exécutez le script `launcher.py` sur la machine qui hébergera le jeu et choisissez **1**.
- Le serveur démarre et écoute sur l'adresse **127.0.0.1:65430** (par défaut).
- Le premier joueur connecté au serveur spécifie combien de joueurs participeront.

### **2. Joueur**
- Sur une autre machine (ou le même ordinateur), lancez `launcher.py` et choisissez **2**.
- Entrez l'adresse IP du serveur (si nécessaire) et suivez les étapes pour jouer.

---

## **Règles du jeu**
- Chaque joueur peut lancer 5 dés et relancer certains dés jusqu'à 2 fois par tour.
- Après 3 lancers maximum, le joueur choisit un chiffre à comptabiliser pour son score.
- Le jeu se termine après un nombre fixe de tours pour chaque joueur.
- Le serveur calcule le score total et annonce le gagnant à la fin de la partie.

---

## **Notes importantes**
1. **Plusieurs joueurs :** Ce jeu fonctionne en mode multijoueur. Assurez-vous que le serveur est actif avant de lancer des clients.
2. **Déconnexion :** Si un joueur se déconnecte, son score est retiré, mais le jeu continue pour les autres participants.
3. **Debugging :** Si vous rencontrez des erreurs, assurez-vous que tous les scripts sont dans leurs emplacements respectifs (`server/`, `client/`).

---

## **Auteur**
- Créé par : Lauretta Delmas, Bastien Cabanié, Oussama Guelagli
---