<p align="center">
  <img src="https://github.com/lucasbe-lpr/app-watermark/blob/main/luluflix.png?raw=true" height="52" alt="Luluflix" />
</p>

<h1 align="center">Watermark Tool</h1>

<p align="center">
  Outil interne pour incruster le logo Luluflix sur vos vidéos et photos,<br/>
  extraire une capture d'écran ou découper un segment vidéo.<br/>
  <strong>Aucune donnée n'est conservée sur un serveur.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
</p>

---

## Fonctionnalités

| Onglet | Description |
|--------|-------------|
| **Vidéo** | Incrustation du logo Luluflix en coin haut-droit, export MP4 H.264 |
| **Photo** | Incrustation du logo sur PNG / JPG, export sans perte |
| **Capture** | Extraction d'une frame précise depuis une vidéo, export PNG |
| **Découpe** | Découpe d'un segment vidéo par points de début et de fin, sans réencodage |

---

## Lancer en local

**Prérequis** : Python 3.10+, FFmpeg installé sur le système.

```bash
# Cloner le dépôt
git clone https://github.com/lucasbe-lpr/app-watermark.git
cd app-watermark

# Installer les dépendances Python
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'app s'ouvre automatiquement sur [http://localhost:8501](http://localhost:8501).

---

## Déploiement sur Streamlit Cloud

1. Forker ou pusher ce dépôt sur votre compte GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Sélectionner le dépôt, la branche `main` et le fichier `app.py`
4. Cliquer sur **Deploy** — FFmpeg est installé automatiquement via `packages.txt`

---

## Structure du projet

```
app-watermark/
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
├── packages.txt        # Paquets système (ffmpeg)
├── luluflix.png        # Logo header
├── flavicon.png        # Watermark incrusté
└── logo.png            # Favicon onglet navigateur
```

---

## Stack technique

| Composant | Rôle |
|-----------|------|
| [Streamlit](https://streamlit.io) | Interface web |
| [FFmpeg](https://ffmpeg.org) | Encodage vidéo, extraction de frames, découpe |
| [Pillow](https://python-pillow.org) | Traitement d'image, incrustation du logo |

---

## Placement du logo

Le logo est positionné automatiquement en haut à droite de chaque média :

- **Largeur** : 15 % de la largeur totale du média
- **Position X** : `largeur − taille_logo − 5 % de la largeur`
- **Position Y** : `7 % de la hauteur`

---

<p align="center">
  Fait avec ♥ par <strong>Lucas Bessonnat</strong>
</p>
