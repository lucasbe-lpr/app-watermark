# 🖥️ Luluflix v1.0 — Watermark Tool

Outil d'incrustation de logo pour vidéos et photos, prêt à déployer gratuitement sur Streamlit Cloud.

---

## Ce que ça fait

- Incruste un logo PNG (transparent) en **haut à droite** de chaque frame d'une vidéo ou d'une photo
- Respecte les règles de placement pour les réseaux sociaux : logo à **15% de la largeur**, marges de **5% (X) et 7% (Y)**
- Export vidéo **quasi sans perte** (H.264, CRF 18, audio copié intact)
- Export photo en PNG sans perte ou JPEG qualité 97
- **Aucune donnée stockée** — tout est traité en mémoire, rien ne reste sur le serveur

---

## Déploiement (gratuit, 3 minutes)

### 1. Mettre les fichiers sur GitHub

Crée un nouveau repo GitHub public et pousse ces 4 fichiers :

```
app.py
requirements.txt
packages.txt
README.md
```

### 2. Déployer sur Streamlit Cloud

1. Va sur **[share.streamlit.io](https://share.streamlit.io)**
2. Connecte ton compte GitHub
3. Clique sur **"New app"**
4. Sélectionne ton repo, branche `main`, fichier principal `app.py`
5. Clique **Deploy**

> Streamlit Cloud installe automatiquement FFmpeg grâce au fichier `packages.txt`. Aucune configuration supplémentaire.

---

## Utilisation en local

**Prérequis :** Python 3.9+, FFmpeg installé sur ta machine.

```bash
# Installer FFmpeg
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows → https://ffmpeg.org/download.html

# Installer les dépendances Python
pip install -r requirements.txt

# Lancer l'app
streamlit run app.py
```

L'app s'ouvre automatiquement sur `http://localhost:8501`.

---

## Utilisation

1. **Onglet Vidéo ou Photo** selon ton fichier source
2. Dépose (ou parcours) ta vidéo / image
3. Dépose ton logo PNG (avec canal alpha/transparence)
4. Un aperçu s'affiche automatiquement avec le logo positionné
5. Pour la vidéo : clique sur **"OK Générer le rendu"** et attends la barre de progression
6. Clique sur **"💾 Enregistrer sous..."** pour télécharger

---

## Logique de placement du logo

Pour une image ou vidéo de dimensions `W × H` :

```
Largeur logo  = W × 0.15
Marge X       = W × 0.05
Marge Y       = H × 0.07

Position X    = W - Largeur logo - Marge X
Position Y    = Marge Y
```

---

## Stack technique

| Composant | Outil |
|-----------|-------|
| Interface | Streamlit |
| Traitement vidéo | FFmpeg (libx264, CRF 18) |
| Traitement image | Pillow |
| Déploiement | Streamlit Cloud (gratuit) |

---

*Lucas Bessonnat — Aucune donnée n'est conservée sur un serveur*
