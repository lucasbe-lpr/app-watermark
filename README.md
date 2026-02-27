# ⌗ WATERMARK_GEN

Outil de watermarking vidéo pour les réseaux sociaux. Upload une vidéo + un logo PNG, génère un rendu prêt à publier en conservant la qualité maximale.

## Fonctionnalités

- Logo en haut à droite, 15% de la largeur, marges 5%/7%
- Qualité quasi-lossless (CRF 18, audio passthrough)
- Prévisualisation thumbnail avant rendu
- Barre de progression en temps réel
- Aucune donnée stockée (RGPD)

## Déploiement sur Streamlit Cloud (gratuit)

1. **Fork / push ce repo sur GitHub**

2. **Aller sur** [share.streamlit.io](https://share.streamlit.io) → "New app"

3. Sélectionner ton repo GitHub, branch `main`, fichier `app.py`

4. Cliquer **Deploy** — c'est tout !

> `packages.txt` installe automatiquement FFmpeg sur le serveur Streamlit Cloud.

## Utilisation en local

```bash
pip install -r requirements.txt
# FFmpeg doit être installé sur ta machine :
# macOS  → brew install ffmpeg
# Ubuntu → sudo apt install ffmpeg
# Windows → https://ffmpeg.org/download.html

streamlit run app.py
```

## Structure du projet

```
watermark_app/
├── app.py           # Application principale
├── requirements.txt # Dépendances Python
├── packages.txt     # Dépendances système (FFmpeg pour Streamlit Cloud)
└── README.md
```

## Logique de placement du logo

```
W_logo   = W_target × 0.15
Margin_X = W_target × 0.05
Margin_Y = H_target × 0.07
X = W_target - W_logo - Margin_X
Y = Margin_Y
```

## Qualité vidéo

- Codec : H.264 (`libx264`)
- CRF 18 → quasi-lossless (0 = lossless, 23 = défaut, 18 = très haute qualité)
- Audio : copié tel quel (aucune recompression)
- `-movflags +faststart` → lecture web optimisée
