import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io

st.set_page_config(
    page_title="Luluflix v1.0",
    page_icon="🖥️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

:root {
  --win-bg:        #c0c0c0;
  --win-dark:      #808080;
  --win-darker:    #404040;
  --win-white:     #ffffff;
  --win-black:     #000000;
  --win-titlebar:  #000080;
  --win-title-txt: #ffffff;
  --win-face:      #c0c0c0;
  --win-highlight: #ffffff;
  --win-shadow:    #808080;
  --win-dshadow:   #404040;
  --win-blue:      #0000ff;
  --win-green:     #008000;
  --win-red:       #ff0000;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background: var(--win-bg) !important;
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 13px !important;
}

.block-container {
  background: transparent !important;
  padding: 1rem 1.5rem 3rem !important;
  max-width: 680px !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── BARRE DE MENU DU HAUT ── */
.menubar {
  background: var(--win-face);
  border-top: 2px solid var(--win-highlight);
  border-left: 2px solid var(--win-highlight);
  border-right: 2px solid var(--win-dshadow);
  border-bottom: 2px solid var(--win-dshadow);
  padding: 2px 4px;
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 8px;
  font-size: 11px;
}
.menu-item {
  padding: 2px 8px;
  cursor: default;
}
.menu-item:hover {
  background: var(--win-titlebar);
  color: var(--win-white);
}

/* ── FENÊTRE PRINCIPALE ── */
.win-window {
  background: var(--win-face);
  border-top: 2px solid var(--win-highlight);
  border-left: 2px solid var(--win-highlight);
  border-right: 2px solid var(--win-dshadow);
  border-bottom: 2px solid var(--win-dshadow);
  margin-bottom: 8px;
}
.win-titlebar {
  background: var(--win-titlebar);
  color: var(--win-title-txt);
  padding: 3px 6px 3px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  font-weight: bold;
  user-select: none;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
}
.titlebar-btns {
  display: flex;
  gap: 2px;
}
.tbtn {
  width: 16px; height: 14px;
  background: var(--win-face);
  border-top: 1px solid var(--win-highlight);
  border-left: 1px solid var(--win-highlight);
  border-right: 1px solid var(--win-dshadow);
  border-bottom: 1px solid var(--win-dshadow);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: var(--win-black);
  cursor: default;
  font-family: 'Marlett', 'Share Tech Mono', monospace;
}
.win-body {
  padding: 10px 12px 12px;
}

/* ── GROUPBOX / PANEL ── */
.groupbox {
  border-top: 1px solid var(--win-shadow);
  border-left: 1px solid var(--win-shadow);
  border-right: 1px solid var(--win-highlight);
  border-bottom: 1px solid var(--win-highlight);
  padding: 12px 10px 10px;
  margin-bottom: 10px;
  position: relative;
}
.groupbox-label {
  position: absolute;
  top: -8px; left: 8px;
  background: var(--win-face);
  padding: 0 4px;
  font-size: 11px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
}

/* ── INSET / SUNKEN ── */
.inset {
  border-top: 1px solid var(--win-shadow);
  border-left: 1px solid var(--win-shadow);
  border-right: 1px solid var(--win-highlight);
  border-bottom: 1px solid var(--win-highlight);
  background: var(--win-white);
  padding: 6px 8px;
  margin-bottom: 6px;
  font-size: 12px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
}

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {
  background: transparent !important;
}
[data-testid="stFileUploader"] section {
  background: var(--win-white) !important;
  border-top: 1px solid var(--win-shadow) !important;
  border-left: 1px solid var(--win-shadow) !important;
  border-right: 1px solid var(--win-highlight) !important;
  border-bottom: 1px solid var(--win-highlight) !important;
  border-radius: 0 !important;
  padding: 14px 10px !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  outline: 1px dotted var(--win-black) !important;
  outline-offset: 2px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 12px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] small {
  color: var(--win-darker) !important;
  font-size: 10px !important;
}
/* Bouton Browse — style Win95 */
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
  background: var(--win-face) !important;
  border-top: 2px solid var(--win-highlight) !important;
  border-left: 2px solid var(--win-highlight) !important;
  border-right: 2px solid var(--win-dshadow) !important;
  border-bottom: 2px solid var(--win-dshadow) !important;
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 11px !important;
  padding: 3px 12px !important;
  border-radius: 0 !important;
  cursor: default !important;
  min-width: 75px !important;
  text-align: center !important;
}
[data-testid="stFileUploader"] button:hover {
  background: var(--win-face) !important;
}
[data-testid="stFileUploader"] button:active {
  border-top: 2px solid var(--win-dshadow) !important;
  border-left: 2px solid var(--win-dshadow) !important;
  border-right: 2px solid var(--win-highlight) !important;
  border-bottom: 2px solid var(--win-highlight) !important;
}
[data-testid="stFileUploaderFileName"] {
  color: var(--win-black) !important;
  font-size: 11px !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
}

/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 2px solid var(--win-shadow) !important;
  gap: 0 !important;
  margin-bottom: 10px !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: var(--win-face) !important;
  border-top: 2px solid var(--win-highlight) !important;
  border-left: 2px solid var(--win-highlight) !important;
  border-right: 2px solid var(--win-shadow) !important;
  border-bottom: none !important;
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 12px !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  padding: 4px 16px !important;
  margin-right: 3px !important;
  margin-bottom: -2px !important;
  border-radius: 0 !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--win-face) !important;
  color: var(--win-black) !important;
  border-bottom: 2px solid var(--win-face) !important;
  padding-top: 6px !important;
  font-weight: bold !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {
  display: none !important;
  background: transparent !important;
}

/* ── SPECS ── */
.specs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  margin-bottom: 10px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
}
.specs-table td {
  padding: 2px 8px;
  border: 1px solid var(--win-shadow);
}
.specs-table td:first-child {
  background: var(--win-face);
  color: var(--win-darker);
  width: 38%;
}
.specs-table td:last-child {
  background: var(--win-white);
  font-weight: bold;
}

/* ── PREVIEW ── */
.preview-inset {
  border-top: 1px solid var(--win-shadow);
  border-left: 1px solid var(--win-shadow);
  border-right: 1px solid var(--win-highlight);
  border-bottom: 1px solid var(--win-highlight);
  background: #000;
  margin-bottom: 10px;
  overflow: hidden;
}
.preview-caption {
  background: var(--win-titlebar);
  color: var(--win-white);
  font-size: 10px;
  padding: 1px 6px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
}

/* ── BUTTONS ── */
div.stButton > button {
  background: var(--win-face) !important;
  border-top: 2px solid var(--win-highlight) !important;
  border-left: 2px solid var(--win-highlight) !important;
  border-right: 2px solid var(--win-dshadow) !important;
  border-bottom: 2px solid var(--win-dshadow) !important;
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 12px !important;
  font-weight: bold !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  padding: 4px 20px !important;
  border-radius: 0 !important;
  min-width: 120px !important;
  cursor: default !important;
  width: auto !important;
  display: block !important;
  margin: 0 auto !important;
  transition: none !important;
}
div.stButton > button:hover {
  background: var(--win-face) !important;
}
div.stButton > button:active,
div.stButton > button:focus {
  border-top: 2px solid var(--win-dshadow) !important;
  border-left: 2px solid var(--win-dshadow) !important;
  border-right: 2px solid var(--win-highlight) !important;
  border-bottom: 2px solid var(--win-highlight) !important;
  outline: 1px dotted var(--win-black) !important;
  outline-offset: -4px !important;
}
div.stButton > button:disabled {
  color: var(--win-shadow) !important;
  text-shadow: 1px 1px 0 var(--win-white) !important;
}

div[data-testid="stDownloadButton"] > button {
  background: var(--win-face) !important;
  border-top: 2px solid var(--win-highlight) !important;
  border-left: 2px solid var(--win-highlight) !important;
  border-right: 2px solid var(--win-dshadow) !important;
  border-bottom: 2px solid var(--win-dshadow) !important;
  color: var(--win-black) !important;
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 12px !important;
  font-weight: bold !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  padding: 4px 20px !important;
  border-radius: 0 !important;
  width: auto !important;
  display: block !important;
  margin: 0 auto !important;
}

/* ── PROGRESS ── */
div[data-testid="stProgress"] > div {
  background: var(--win-white) !important;
  border-top: 1px solid var(--win-shadow) !important;
  border-left: 1px solid var(--win-shadow) !important;
  border-right: 1px solid var(--win-highlight) !important;
  border-bottom: 1px solid var(--win-highlight) !important;
  border-radius: 0 !important;
  height: 16px !important;
}
div[data-testid="stProgress"] > div > div {
  background: var(--win-titlebar) !important;
  border-radius: 0 !important;
  height: 100% !important;
}
div[data-testid="stProgress"] p {
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 10px !important;
  color: var(--win-darker) !important;
}

/* ── STATUS ── */
.status-bar {
  background: var(--win-face);
  border-top: 1px solid var(--win-shadow);
  padding: 2px 6px;
  font-size: 11px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  display: flex;
  align-items: center;
  gap: 4px;
}
.status-panel {
  border-top: 1px solid var(--win-shadow);
  border-left: 1px solid var(--win-shadow);
  border-right: 1px solid var(--win-highlight);
  border-bottom: 1px solid var(--win-highlight);
  padding: 1px 8px;
  font-size: 11px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  flex: 1;
}
.msg-ok   { color: var(--win-green); }
.msg-warn { color: var(--win-darker); }
.msg-err  { color: var(--win-red); font-weight: bold; }
.msg-idle { color: var(--win-shadow); }

/* ── FOOTER / STATUSBAR ── */
.app-statusbar {
  background: var(--win-face);
  border-top: 2px solid var(--win-shadow);
  padding: 3px 8px;
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  color: var(--win-darker);
  margin-top: 16px;
}
.statusbar-cell {
  border-top: 1px solid var(--win-shadow);
  border-left: 1px solid var(--win-shadow);
  border-right: 1px solid var(--win-highlight);
  border-bottom: 1px solid var(--win-highlight);
  padding: 1px 10px;
}

/* Spinner */
div[data-testid="stSpinner"] p {
  font-family: 'Share Tech Mono', 'Courier New', monospace !important;
  font-size: 11px !important;
  color: var(--win-darker) !important;
}
</style>
""", unsafe_allow_html=True)

# ── BARRE DE MENU ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="menubar">
  <span class="menu-item">Fichier</span>
  <span class="menu-item">Edition</span>
  <span class="menu-item">Affichage</span>
  <span class="menu-item">Aide</span>
</div>
""", unsafe_allow_html=True)

# ── FENÊTRE PRINCIPALE ─────────────────────────────────────────────────────────
st.markdown("""
<div class="win-window">
  <div class="win-titlebar">
    <span>🖥️ Luluflix v1.0 — Watermark Tool</span>
    <div class="titlebar-btns">
      <div class="tbtn">_</div>
      <div class="tbtn">□</div>
      <div class="tbtn">✕</div>
    </div>
  </div>
  <div class="win-body" style="padding-bottom:4px;">
""", unsafe_allow_html=True)

# ── HELPERS ────────────────────────────────────────────────────────────────────

def composite_logo(base: Image.Image, logo_path: str) -> Image.Image:
    W, H = base.size
    logo_w = int(W * 0.15)
    logo = Image.open(logo_path).convert("RGBA")
    ratio = logo_w / logo.width
    logo = logo.resize((logo_w, int(logo.height * ratio)), Image.LANCZOS)
    x = W - logo_w - int(W * 0.05)
    y = int(H * 0.07)
    out = base.convert("RGBA")
    out.paste(logo, (x, y), logo)
    return out

def get_video_info(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=0", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            info[k.strip()] = v.strip()
    w = int(info.get("width", 0))
    h = int(info.get("height", 0))
    dur = float(info.get("duration", 0))
    fps_raw = info.get("r_frame_rate", "25/1")
    try:
        num, den = fps_raw.split("/")
        fps = round(float(num) / float(den), 2)
    except Exception:
        fps = 25.0
    return {"width": w, "height": h, "duration": dur, "fps": fps}

def make_thumbnail(video_path: str, logo_path: str, info: dict) -> Image.Image:
    result = subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ], capture_output=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGBA")
    return composite_logo(frame, logo_path).convert("RGB")

def render_video(video_path, logo_path, output_path, info, progress_cb=None):
    W, H = info["width"], info["height"]
    logo_w = int(W * 0.15)
    x = W - logo_w - int(W * 0.05)
    y = int(H * 0.07)
    filter_complex = f"[1:v]scale={logo_w}:-1[logo];[0:v][logo]overlay={x}:{y}"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path, "-i", logo_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy", "-movflags", "+faststart",
        "-progress", "pipe:1", output_path
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    total = info["duration"]
    while True:
        line = process.stdout.readline()
        if not line: break
        if line.strip().startswith("out_time_ms="):
            try:
                ms = int(line.strip().split("=")[1])
                if total > 0 and progress_cb:
                    progress_cb(min(ms / 1_000_000 / total, 1.0))
            except Exception:
                pass
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(process.stderr.read())

# ── SESSION STATE ───────────────────────────────────────────────────────────────
for k in ["thumbnail", "rendered_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ── TABS ────────────────────────────────────────────────────────────────────────
tab_v, tab_p = st.tabs(["📹 Vidéo", "🖼 Photo"])

# ═══════════════════════════════ VIDÉO ════════════════════════════════════════
with tab_v:

    st.markdown("""
    <div class="groupbox">
      <span class="groupbox-label">Fichier source</span>
    """, unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposer la vidéo ici ou cliquer sur Parcourir",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="groupbox">
      <span class="groupbox-label">Logo (PNG transparent)</span>
    """, unsafe_allow_html=True)
    logo_v = st.file_uploader(
        "Déposer le logo ici ou cliquer sur Parcourir",
        type=["png"],
        key="vl"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if video_file and logo_v:
        tmp = tempfile.mkdtemp()
        vp = os.path.join(tmp, "src" + os.path.splitext(video_file.name)[1])
        lp = os.path.join(tmp, "logo.png")
        with open(vp, "wb") as f: f.write(video_file.read())
        with open(lp, "wb") as f: f.write(logo_v.read())

        nfo = get_video_info(vp)
        dur_s = f"{int(nfo['duration']//60)}:{int(nfo['duration']%60):02d}"

        st.markdown(f"""
        <div class="groupbox">
          <span class="groupbox-label">Propriétés</span>
          <table class="specs-table">
            <tr><td>Résolution :</td><td>{nfo['width']} x {nfo['height']} px</td></tr>
            <tr><td>Durée :</td><td>{dur_s}</td></tr>
            <tr><td>Fréquence :</td><td>{nfo['fps']} fps</td></tr>
            <tr><td>Largeur logo :</td><td>{int(nfo['width']*0.15)} px (15%)</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.thumbnail is None:
            with st.spinner("Calcul de l'aperçu en cours..."):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown("""
        <div class="groupbox">
          <span class="groupbox-label">Aperçu</span>
          <div class="preview-inset">
            <div class="preview-caption">Aperçu.bmp — première image avec logo</div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("OK  Générer le rendu", key="vbtn",
                     disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_p, ph_s = st.empty(), st.empty()
            bar = ph_p.progress(0.0, text="")
            ph_s.markdown('<div class="status-bar"><div class="status-panel msg-warn">⧖ Encodage en cours, veuillez patienter...</div></div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo,
                             lambda p: bar.progress(p, text=f"Encodage : {int(p*100)}%"))
                bar.progress(1.0, text="Terminé : 100%")
                ph_s.markdown('<div class="status-bar"><div class="status-panel msg-ok">✓ Encodage terminé. Fichier prêt au téléchargement.</div></div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status-bar"><div class="status-panel msg-err">ERREUR : {e}</div></div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button(
                "💾  Enregistrer sous...",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="vdl"
            )

    else:
        st.markdown('<div class="status-bar"><div class="status-panel msg-idle">En attente — sélectionner une vidéo et un logo.</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════ PHOTO ════════════════════════════════════════
with tab_p:

    st.markdown("""
    <div class="groupbox">
      <span class="groupbox-label">Fichier source</span>
    """, unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposer l'image ici ou cliquer sur Parcourir",
        type=["png", "jpg", "jpeg"],
        key="pu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="groupbox">
      <span class="groupbox-label">Logo (PNG transparent)</span>
    """, unsafe_allow_html=True)
    logo_p = st.file_uploader(
        "Déposer le logo ici ou cliquer sur Parcourir",
        type=["png"],
        key="pl"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if photo_file and logo_p:
        base = Image.open(photo_file)
        W, H = base.size
        tmp2 = tempfile.mkdtemp()
        lp2 = os.path.join(tmp2, "logo.png")
        with open(lp2, "wb") as f: f.write(logo_p.read())

        fmt = (base.format or photo_file.name.rsplit(".", 1)[-1]).upper()
        st.markdown(f"""
        <div class="groupbox">
          <span class="groupbox-label">Propriétés</span>
          <table class="specs-table">
            <tr><td>Résolution :</td><td>{W} x {H} px</td></tr>
            <tr><td>Format :</td><td>{fmt}</td></tr>
            <tr><td>Largeur logo :</td><td>{int(W*0.15)} px (15%)</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        result_img = composite_logo(base, lp2)

        st.markdown("""
        <div class="groupbox">
          <span class="groupbox-label">Aperçu</span>
          <div class="preview-inset">
            <div class="preview-caption">Aperçu.bmp — image avec logo</div>
        """, unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result_img.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result_img.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"

        st.markdown('<div class="status-bar"><div class="status-panel msg-ok">✓ Traitement terminé. Prêt à enregistrer.</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "💾  Enregistrer sous...",
            data=buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="pdl"
        )
    else:
        st.markdown('<div class="status-bar"><div class="status-panel msg-idle">En attente — sélectionner une image et un logo.</div></div>', unsafe_allow_html=True)

# ── FERMETURE FENÊTRE ──────────────────────────────────────────────────────────
st.markdown('</div></div>', unsafe_allow_html=True)

# ── BARRE DE STATUT BAS ────────────────────────────────────────────────────────
st.markdown("""
<div class="app-statusbar">
  <div class="statusbar-cell">Lucas Bessonnat</div>
  <div class="statusbar-cell">Aucune donnée n'est conservée sur un serveur</div>
  <div class="statusbar-cell">Luluflix v1.0</div>
</div>
""", unsafe_allow_html=True)
