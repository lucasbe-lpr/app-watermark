import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io
import urllib.request

st.set_page_config(
    page_title="Luluflix",
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
  --blue:    #0068B1;
  --blue-bg: #f0f7fd;
  --white:   #ffffff;
  --ink:     #1a1a1a;
  --muted:   #8a8a8a;
  --border:  #ebebeb;
  --green:   #1a7a42;
  --green-bg:#f2faf5;
  --warn:    #b45309;
  --warn-bg: #fffbf0;
  --red:     #c0392b;
  --red-bg:  #fdf5f5;
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
  max-width: 640px !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── HEADER ── */
.site-header {
  padding: 2.5rem 0 1.8rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-header img {
  height: 44px;
  width: auto;
  display: block;
}
.site-header-right {
  font-size: 0.72rem;
  color: var(--muted);
  letter-spacing: 0.01em;
}

/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  margin-bottom: 2rem !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
  color: var(--muted) !important;
  font-family: 'Roboto Condensed', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  padding: 0.65rem 1.2rem 0.65rem 0 !important;
  transition: color 0.15s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--ink) !important;
  font-weight: 500 !important;
  border-bottom: 2px solid var(--blue) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--ink) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {
  display: none !important;
  background: transparent !important;
}

/* ── SECTION LABEL ── */
.section-label {
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.6rem;
}

/* ── UPLOADER ── */
[data-testid="stFileUploader"] {
  background: transparent !important;
  margin-bottom: 1.8rem !important;
}
[data-testid="stFileUploader"] section {
  background: var(--blue-bg) !important;
  border: 1.5px dashed #b8d4e8 !important;
  border-radius: 6px !important;
  padding: 2rem 1.5rem !important;
  transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  border-color: var(--blue) !important;
  background: #e6f2fb !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: var(--ink) !important;
  font-weight: 500 !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
  background: var(--white) !important;
  border: 1px solid var(--blue) !important;
  color: var(--blue) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  padding: 0.3rem 1rem !important;
  border-radius: 4px !important;
  transition: all 0.15s !important;
}
[data-testid="stFileUploader"] button:hover {
  background: var(--blue) !important;
  color: var(--white) !important;
}
[data-testid="stFileUploaderFileName"] {
  color: var(--blue) !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
}

/* ── SPECS ── */
.specs-row {
  display: flex;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.8rem;
}
.spec-cell {
  flex: 1;
  padding: 0.8rem 1rem;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.spec-cell:last-child { border-right: none; }
.spec-k {
  font-size: 0.58rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}
.spec-v {
  font-size: 1rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.2;
}

/* ── APERÇU ── */
.preview-wrap {
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  background: #f5f5f5;
}
.preview-bar {
  padding: 0.4rem 0.8rem;
  border-bottom: 1px solid var(--border);
  background: var(--white);
  font-size: 0.65rem;
  color: var(--muted);
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

/* ── BUTTONS ── */
div.stButton > button {
  width: 100% !important;
  background: var(--blue) !important;
  border: none !important;
  color: var(--white) !important;
  font-family: 'Roboto Condensed', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  padding: 0.7rem 1.5rem !important;
  border-radius: 6px !important;
  transition: background 0.15s !important;
  letter-spacing: 0.02em !important;
  text-transform: none !important;
}
div.stButton > button:hover   { background: #005a99 !important; }
div.stButton > button:disabled {
  background: var(--border) !important;
  color: var(--muted) !important;
}

div[data-testid="stDownloadButton"] > button {
  width: 100% !important;
  background: var(--white) !important;
  border: 1.5px solid var(--blue) !important;
  color: var(--blue) !important;
  font-family: 'Roboto Condensed', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  padding: 0.7rem 1.5rem !important;
  border-radius: 6px !important;
  transition: all 0.15s !important;
  letter-spacing: 0.02em !important;
  text-transform: none !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: var(--blue) !important;
  color: var(--white) !important;
}

/* ── PROGRESS — masqué, remplacé par statut animé ── */
div[data-testid="stProgress"] {
  display: none !important;
}

/* ── STATUS ── */
.status {
  font-size: 0.8rem;
  padding: 0.6rem 0.9rem;
  border-radius: 6px;
  margin: 0.8rem 0;
  font-family: 'Roboto', sans-serif;
}
.status-ok   { color: var(--green); background: var(--green-bg); }
.status-warn { color: var(--warn);  background: var(--warn-bg); }
.status-err  { color: var(--red);   background: var(--red-bg); }
.status-idle { color: var(--muted); background: var(--white); }

.status-processing {
  color: var(--blue);
  background: var(--blue-bg);
  font-family: 'Roboto', sans-serif;
  font-size: 0.8rem;
  padding: 0.65rem 0.9rem;
  border-radius: 6px;
  margin: 0.8rem 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.dot-pulse {
  display: flex;
  gap: 4px;
  align-items: center;
}
.dot-pulse span {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--blue);
  display: inline-block;
  animation: pulse 1.2s ease-in-out infinite;
}
.dot-pulse span:nth-child(2) { animation-delay: 0.2s; }
.dot-pulse span:nth-child(3) { animation-delay: 0.4s; }
@keyframes pulse {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
  40%           { transform: scale(1);   opacity: 1; }
}

/* ── FOOTER ── */
.site-footer {
  margin-top: 4rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.72rem;
  color: var(--muted);
}
.footer-name { font-weight: 500; color: var(--ink); }

div[data-testid="stSpinner"] p {
  font-size: 0.8rem !important;
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="site-header">
  <img src="{LOGO_URL}" alt="Luluflix" />
  <span class="site-header-right">Watermark Tool</span>
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

        if st.button("Générer le rendu", key="vbtn",
                     disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_s = st.empty()
            ph_s.markdown('<div class="status-processing"><div class="dot-pulse"><span></span><span></span><span></span></div>Encodage en cours…</div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo, progress_cb=None)
                ph_s.markdown('<div class="status status-ok">✓ Terminé — fichier prêt.</div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">Erreur : {e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button(
                "Télécharger la vidéo",
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
  <span class="footer-name">Lucas Bessonnat</span>
  <span>Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
