import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io
import urllib.request

st.set_page_config(
    page_title="luluflix",
    page_icon="▶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

LOGO_URL       = "https://github.com/lucasbe-lpr/app-watermark/blob/main/luluflix.png?raw=true"
DEFAULT_WM_URL = "https://github.com/lucasbe-lpr/app-watermark/blob/main/flavicon.png?raw=true"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&family=Roboto+Condensed:wght@400;500;700&display=swap');

:root {
  --blue:      #0068B1;
  --blue-dim:  #e8f2fb;
  --blue-text: #0058a0;
  --white:     #ffffff;
  --bg:        #fafafa;
  --ink:       #111111;
  --sub:       #555555;
  --muted:     #999999;
  --border:    #e4e4e4;
  --border-mid:#d0d0d0;
  --green:     #166534;
  --green-bg:  #f0fdf4;
  --green-bd:  #bbf7d0;
  --red:       #991b1b;
  --red-bg:    #fff1f1;
  --red-bd:    #fecaca;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background: var(--white) !important;
  color: var(--ink) !important;
  font-family: 'Roboto', sans-serif !important;
  font-weight: 400 !important;
}

.block-container {
  background: var(--white) !important;
  padding: 0 2rem 5rem !important;
  max-width: 600px !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── HEADER ── */
.site-header {
  padding: 2rem 0 1.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.8rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-header img { height: 44px; width: auto; display: block; }
.site-header-right {
  font-size: 0.7rem;
  color: var(--muted);
  font-family: 'Roboto', sans-serif;
  letter-spacing: 0.01em;
}

/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  margin-bottom: 1.8rem !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 1.5px solid transparent !important;
  margin-bottom: -1px !important;
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  padding: 0.6rem 1.4rem 0.6rem 0 !important;
  transition: color 0.12s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--ink) !important;
  font-weight: 500 !important;
  border-bottom: 1.5px solid var(--blue) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: var(--sub) !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {
  display: none !important;
  background: transparent !important;
}

/* ── UPLOADER ── */
[data-testid="stFileUploader"] {
  background: transparent !important;
  margin-bottom: 1.6rem !important;
}
[data-testid="stFileUploader"] section {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 1.6rem 1.4rem !important;
  transition: border-color 0.15s, background 0.15s !important;
  cursor: pointer !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  border-color: var(--blue) !important;
  background: var(--blue-dim) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
  text-align: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: var(--sub) !important;
  font-weight: 500 !important;
}
/* Bouton "Browse files" — pill minimaliste */
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
  background: var(--white) !important;
  border: 1px solid var(--border-mid) !important;
  color: var(--sub) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 400 !important;
  padding: 0.28rem 0.9rem !important;
  border-radius: 999px !important;
  transition: all 0.12s !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06) !important;
}
[data-testid="stFileUploader"] button:hover {
  border-color: var(--blue) !important;
  color: var(--blue) !important;
  background: var(--white) !important;
}
/* Nom du fichier chargé */
[data-testid="stFileUploaderFileName"] {
  color: var(--ink) !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
}
/* Croix de suppression — discrète */
[data-testid="stFileUploaderDeleteBtn"] button,
button[title="Remove file"] {
  background: transparent !important;
  border: none !important;
  color: var(--muted) !important;
  padding: 2px 4px !important;
  border-radius: 4px !important;
  font-size: 0.75rem !important;
  transition: color 0.12s, background 0.12s !important;
  box-shadow: none !important;
}
[data-testid="stFileUploaderDeleteBtn"] button:hover,
button[title="Remove file"]:hover {
  color: var(--red) !important;
  background: var(--red-bg) !important;
}

/* ── SPECS ── */
.specs-row {
  display: flex;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.6rem;
  background: var(--bg);
}
.spec-cell {
  flex: 1;
  padding: 0.75rem 1rem;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.18rem;
}
.spec-cell:last-child { border-right: none; }
.spec-k {
  font-size: 0.58rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--muted);
}
.spec-v {
  font-size: 0.92rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.2;
}

/* ── APERÇU ── */
.preview-wrap {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.2rem;
  background: #f0f0f0;
}
.preview-bar {
  padding: 0.35rem 0.85rem;
  border-bottom: 1px solid var(--border);
  background: var(--white);
  font-size: 0.62rem;
  color: var(--muted);
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ── BOUTON PRINCIPAL (mutable) ── */
div.stButton > button {
  width: 100% !important;
  background: var(--blue) !important;
  border: none !important;
  color: var(--white) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  padding: 0 1.4rem !important;
  height: 38px !important;
  border-radius: 999px !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  transition: background 0.15s, box-shadow 0.15s, transform 0.1s !important;
  box-shadow: 0 1px 2px rgba(0,104,177,0.18), 0 2px 8px rgba(0,104,177,0.12) !important;
  cursor: pointer !important;
}
div.stButton > button:hover {
  background: #005fa8 !important;
  box-shadow: 0 2px 4px rgba(0,104,177,0.22), 0 4px 12px rgba(0,104,177,0.16) !important;
  transform: translateY(-1px) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }
div.stButton > button:disabled {
  background: var(--border) !important;
  color: var(--muted) !important;
  box-shadow: none !important;
  cursor: default !important;
  transform: none !important;
}

/* Bouton vert "Télécharger" après encodage */
div.stDownloadButton > button,
div[data-testid="stDownloadButton"] > button {
  width: 100% !important;
  background: #16a34a !important;
  border: none !important;
  color: #fff !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  padding: 0 1.4rem !important;
  height: 38px !important;
  border-radius: 999px !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  transition: background 0.15s, box-shadow 0.15s, transform 0.1s !important;
  box-shadow: 0 1px 2px rgba(22,163,74,0.2), 0 2px 8px rgba(22,163,74,0.12) !important;
}
div.stDownloadButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
  background: #15803d !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 4px rgba(22,163,74,0.25), 0 4px 12px rgba(22,163,74,0.15) !important;
}
div.stDownloadButton > button:active,
div[data-testid="stDownloadButton"] > button:active {
  transform: translateY(0) !important;
}

/* ── PROGRESS natif masqué ── */
div[data-testid="stProgress"] { display: none !important; }

/* ── SPINNER ENCODAGE ── */
.encoding-wrap {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.5rem 0;
  margin: 0.5rem 0;
}
.encoding-ring {
  width: 16px; height: 16px;
  border: 2px solid var(--border);
  border-top-color: var(--blue);
  border-radius: 50%;
  flex-shrink: 0;
  animation: spin 0.75s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.encoding-text {
  font-size: 0.8rem;
  color: var(--sub);
  font-family: 'Roboto', sans-serif;
}

/* ── FAKE PROGRESS BAR — pur CSS, animée ── */
.fake-progress-wrap {
  margin: 0.6rem 0 0.4rem;
}
.fake-progress-track {
  height: 3px;
  background: var(--border);
  border-radius: 99px;
  overflow: hidden;
}
.fake-progress-bar {
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--blue-dim), var(--blue), var(--blue-dim));
  background-size: 200% 100%;
  animation: indeterminate 1.4s ease-in-out infinite;
}
@keyframes indeterminate {
  0%   { background-position: 200% center; }
  100% { background-position: -200% center; }
}
/* ── STATUS ── */
.status {
  font-size: 0.78rem;
  padding: 0.5rem 0;
  margin: 0.5rem 0;
  font-family: 'Roboto', sans-serif;
  color: var(--muted);
  line-height: 1.4;
}
.status-ok  { color: var(--green); }
.status-err { color: var(--red); }
.status-idle { color: var(--muted); }

/* ── FOOTER ── */
.site-footer {
  margin-top: 4rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.7rem;
  color: var(--muted);
}
.footer-name { color: var(--sub); font-weight: 500; }

div[data-testid="stSpinner"] p {
  font-size: 0.78rem !important;
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="site-header">
  <img src="{LOGO_URL}" alt="Luluflix" />
  <span class="site-header-right">watermark tool</span>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ────────────────────────────────────────────────────────────────────

def get_default_logo() -> str:
    if "default_logo_path" not in st.session_state:
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "default_wm.png")
        urllib.request.urlretrieve(DEFAULT_WM_URL, path)
        st.session_state.default_logo_path = path
    return st.session_state.default_logo_path

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
tab_v, tab_p = st.tabs(["Vidéo", "Photo"])

# ═══════════════════════════════ VIDÉO ════════════════════════════════════════
with tab_v:

    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposez votre vidéo ici",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu",
        label_visibility="collapsed"
    )

    if video_file:
        lp = get_default_logo()
        tmp = tempfile.mkdtemp()
        vp = os.path.join(tmp, "src" + os.path.splitext(video_file.name)[1])
        with open(vp, "wb") as f: f.write(video_file.read())

        nfo = get_video_info(vp)
        dur_s = f"{int(nfo['duration']//60)}:{int(nfo['duration']%60):02d}"

        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{nfo['width']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{nfo['height']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Durée</span><span class="spec-v">{dur_s}</span></div>
          <div class="spec-cell"><span class="spec-k">FPS</span><span class="spec-v">{nfo['fps']}</span></div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.thumbnail is None:
            with st.spinner("Génération de l'aperçu…"):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown('<div class="preview-wrap"><div class="preview-bar">Aperçu</div>', unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if not st.session_state.rendered_bytes:
            if st.button("Générer le rendu", key="vbtn"):
                out = os.path.join(tmp, "video_ready_to_post.mp4")
                ph = st.empty()
                ph.markdown('''
                <div class="encoding-wrap">
                  <div class="encoding-ring"></div>
                  <span class="encoding-text">Encodage en cours…</span>
                </div>
                <div class="fake-progress-wrap">
                  <div class="fake-progress-track">
                    <div class="fake-progress-bar"></div>
                  </div>
                </div>
                ''', unsafe_allow_html=True)
                try:
                    render_video(vp, lp, out, nfo, progress_cb=None)
                    ph.empty()
                    with open(out, "rb") as f:
                        st.session_state.rendered_bytes = f.read()
                    st.rerun()
                except Exception as e:
                    ph.markdown(f'<div class="status status-err">Erreur : {e}</div>', unsafe_allow_html=True)
        else:
            st.download_button(
                "↓  Télécharger la vidéo",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="vdl"
            )
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo pour commencer.</div>', unsafe_allow_html=True)


# ═══════════════════════════════ PHOTO ════════════════════════════════════════
with tab_p:

    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposez votre image ici",
        type=["png", "jpg", "jpeg"],
        key="pu",
        label_visibility="collapsed"
    )

    if photo_file:
        lp2 = get_default_logo()
        base = Image.open(photo_file)
        W, H = base.size
        fmt = (base.format or photo_file.name.rsplit(".", 1)[-1]).upper()

        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{W} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{H} px</span></div>
          <div class="spec-cell"><span class="spec-k">Format</span><span class="spec-v">{fmt}</span></div>
          <div class="spec-cell"><span class="spec-k">Logo</span><span class="spec-v">{int(W*0.15)} px</span></div>
        </div>
        """, unsafe_allow_html=True)

        result_img = composite_logo(base, lp2)

        st.markdown('<div class="preview-wrap"><div class="preview-bar">Aperçu</div>', unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result_img.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result_img.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"

        st.markdown('<div class="status status-ok">✓ Prêt à télécharger.</div>', unsafe_allow_html=True)
        st.download_button(
            "Télécharger la photo",
            data=buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="pdl"
        )
    else:
        st.markdown('<div class="status status-idle">Déposez une image pour commencer.</div>', unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  <span class="footer-name">© Lucas Bessonnat</span>
  <span>Aucune donnée n'est conservée sur un serveur.</span>
</div>
""", unsafe_allow_html=True)
