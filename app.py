import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io

st.set_page_config(
    page_title="Luluflix",
    page_icon="▶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Azeret+Mono:wght@300;400;500;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --bg:        #0a0a0f;
  --bg2:       #0f0f17;
  --green:     #00ff41;
  --green-dim: #007a1f;
  --red:       #ff2d55;
  --white:     #e8e8f0;
  --muted:     #3a3a4a;
  --border:    #1a1a2e;
  --amber:     #ffbe0b;
  --cyan:      #00d9f5;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background: var(--bg) !important;
  color: var(--white) !important;
  font-family: 'Azeret Mono', monospace !important;
}

.block-container {
  background: var(--bg) !important;
  padding: 0 2rem 5rem !important;
  max-width: 760px !important;
}

/* SCANLINES */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 3px,
    rgba(0,0,0,0.18) 3px,
    rgba(0,0,0,0.18) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* NOISE GRAIN */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: -200%;
  width: 400%;
  height: 400%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  opacity: 0.4;
  pointer-events: none;
  z-index: 9998;
  animation: grain 0.5s steps(2) infinite;
}
@keyframes grain {
  0%,100% { transform: translate(0,0); }
  25%      { transform: translate(-1%,-2%); }
  50%      { transform: translate(1%,1%); }
  75%      { transform: translate(-2%,1%); }
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ══════════════════════════════
   HEADER
══════════════════════════════ */
.site-header {
  position: relative;
  padding: 4rem 0 0;
  margin-bottom: 0;
  overflow: hidden;
}
.site-header-bg {
  position: absolute;
  top: 0; left: -2rem; right: -2rem;
  height: 100%;
  background: linear-gradient(180deg, #0f0f1f 0%, transparent 100%);
  z-index: 0;
}

.title-row {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-end;
  gap: 0;
}
.title-main {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(6rem, 22vw, 11rem);
  line-height: 0.85;
  color: var(--white);
  letter-spacing: 0.01em;
  animation: flicker 8s infinite;
}
@keyframes flicker {
  0%,95%,97%,100% { opacity: 1; }
  96%             { opacity: 0.6; }
  96.5%           { opacity: 0.95; }
}
.title-accent {
  color: var(--green);
  text-shadow: 0 0 30px #00ff4177, 0 0 80px #00ff4133;
}

.header-meta {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-top: 0.6rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--muted);
}
.header-badge {
  font-size: 0.55rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--bg);
  background: var(--green);
  padding: 0.2rem 0.5rem;
  font-weight: 700;
  font-family: 'Azeret Mono', monospace;
}
.header-status {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  color: var(--muted);
}
.blink {
  animation: blink 1.1s step-end infinite;
  color: var(--green);
}
@keyframes blink { 50% { opacity: 0; } }

/* ══════════════════════════════
   TABS
══════════════════════════════ */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--muted) !important;
  gap: 0 !important;
  margin: 2rem 0 0 !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
  color: var(--muted) !important;
  font-family: 'Azeret Mono', monospace !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  padding: 0.7rem 2rem 0.7rem 0 !important;
  transition: color 0.15s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--green) !important;
  border-bottom: 2px solid var(--green) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--white) !important;
}

/* ══════════════════════════════
   SECTION NUMBERS
══════════════════════════════ */
.section-block {
  position: relative;
  margin-top: 2.5rem;
}
.section-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 5rem;
  line-height: 1;
  color: var(--border);
  position: absolute;
  top: -1.2rem;
  left: -0.5rem;
  z-index: 0;
  pointer-events: none;
  user-select: none;
}
.section-label {
  position: relative;
  z-index: 1;
  font-size: 0.58rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--cyan);
  margin-bottom: 0.6rem;
  padding-left: 0.2rem;
  font-family: 'Azeret Mono', monospace;
}

/* ══════════════════════════════
   UPLOAD TERMINAL
══════════════════════════════ */
[data-testid="stFileUploader"] {
  background: transparent !important;
  position: relative;
  z-index: 1;
}
[data-testid="stFileUploader"] section {
  background: var(--bg2) !important;
  border: 1px solid var(--muted) !important;
  border-radius: 0 !important;
  padding: 1.6rem 1.4rem !important;
  transition: border-color 0.2s, background 0.2s !important;
  position: relative !important;
}
/* coin supérieur gauche style terminal */
[data-testid="stFileUploader"] section::before {
  content: '> _';
  position: absolute;
  top: 0.5rem;
  left: 0.7rem;
  font-family: 'Space Mono', monospace;
  font-size: 0.55rem;
  color: var(--green-dim);
  letter-spacing: 0.1em;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  border-color: var(--green) !important;
  background: #0d1a0d !important;
  box-shadow: 0 0 20px #00ff411a inset !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--white) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.78rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] small {
  color: var(--muted) !important;
  font-size: 0.62rem !important;
}
/* Browse button */
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
  background: transparent !important;
  border: 1px solid var(--green) !important;
  color: var(--green) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.1em !important;
  padding: 0.35rem 0.9rem !important;
  border-radius: 0 !important;
  transition: all 0.15s !important;
  margin-top: 0.4rem !important;
}
[data-testid="stFileUploader"] button:hover {
  background: var(--green) !important;
  color: var(--bg) !important;
}
[data-testid="stFileUploaderFileName"] {
  color: var(--amber) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.72rem !important;
}

/* ══════════════════════════════
   SPECS
══════════════════════════════ */
.specs-band {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border: 1px solid var(--muted);
  margin: 1.8rem 0;
  background: var(--bg2);
}
.spec-item {
  padding: 0.8rem 1rem;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.spec-item:last-child { border-right: none; }
.spec-key {
  font-size: 0.48rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'Azeret Mono', monospace;
}
.spec-val {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.4rem;
  color: var(--green);
  line-height: 1;
  letter-spacing: 0.03em;
}

/* ══════════════════════════════
   PREVIEW
══════════════════════════════ */
.preview-shell {
  border: 1px solid var(--muted);
  background: #000;
  margin-bottom: 1.5rem;
}
.preview-topbar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
}
.preview-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--muted);
}
.preview-dot.g { background: var(--green); box-shadow: 0 0 5px var(--green); }
.preview-title-bar {
  font-family: 'Space Mono', monospace;
  font-size: 0.52rem;
  color: var(--muted);
  letter-spacing: 0.12em;
  margin-left: 0.3rem;
}

/* ══════════════════════════════
   BUTTONS
══════════════════════════════ */
div.stButton > button {
  width: 100% !important;
  background: transparent !important;
  border: 1px solid var(--white) !important;
  color: var(--white) !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 1.35rem !important;
  letter-spacing: 0.12em !important;
  padding: 0.7rem 1rem !important;
  border-radius: 0 !important;
  transition: all 0.15s !important;
  line-height: 1 !important;
}
div.stButton > button:hover {
  background: var(--white) !important;
  color: var(--bg) !important;
  box-shadow: 0 0 25px rgba(232,232,240,0.15) !important;
}
div.stButton > button:disabled {
  border-color: var(--muted) !important;
  color: var(--muted) !important;
}

div[data-testid="stDownloadButton"] > button {
  width: 100% !important;
  background: var(--green) !important;
  border: none !important;
  color: var(--bg) !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 1.35rem !important;
  letter-spacing: 0.12em !important;
  padding: 0.7rem 1rem !important;
  border-radius: 0 !important;
  font-weight: 400 !important;
  box-shadow: 0 0 30px #00ff4133 !important;
  line-height: 1 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: #33ff6a !important;
}

/* ══════════════════════════════
   PROGRESS
══════════════════════════════ */
div[data-testid="stProgress"] > div {
  background: var(--border) !important;
  border-radius: 0 !important;
  height: 4px !important;
}
div[data-testid="stProgress"] > div > div {
  background: var(--green) !important;
  border-radius: 0 !important;
  box-shadow: 0 0 8px var(--green) !important;
}
div[data-testid="stProgress"] p {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.6rem !important;
  color: var(--muted) !important;
  letter-spacing: 0.12em !important;
}

/* ══════════════════════════════
   STATUS
══════════════════════════════ */
.status {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  padding: 0.6rem 0.8rem;
  border-left: 2px solid;
  margin: 0.8rem 0;
  line-height: 1.6;
}
.status::before { margin-right: 0.5rem; }
.status-ok   { border-color: var(--green); color: var(--green); background: #001a00; }
.status-ok::before { content: '✓'; }
.status-warn { border-color: var(--amber); color: var(--amber); background: #1a1200; }
.status-warn::before { content: '⧖'; }
.status-err  { border-color: var(--red);   color: var(--red);   background: #1a0000; }
.status-err::before  { content: '✗'; }
.status-idle { border-color: var(--border); color: var(--muted); }
.status-idle::before { content: '○'; }

/* ══════════════════════════════
   FOOTER
══════════════════════════════ */
.footer {
  margin-top: 5rem;
  padding: 1.2rem 0;
  border-top: 1px solid var(--muted);
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 1rem;
}
.footer-name {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  letter-spacing: 0.08em;
  color: var(--green);
}
.footer-legal {
  font-family: 'Azeret Mono', monospace;
  font-size: 0.5rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  text-align: right;
}

/* Spinner */
div[data-testid="stSpinner"] p {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.62rem !important;
  color: var(--muted) !important;
  letter-spacing: 0.1em !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
  <div class="site-header-bg"></div>
  <div class="title-row">
    <span class="title-main">LULU<span class="title-accent">FLIX</span></span>
  </div>
  <div class="header-meta">
    <span class="header-badge">v1.0</span>
    <span class="header-status">WATERMARK ENGINE <span class="blink">█</span></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────

def composite_logo(base: Image.Image, logo_path: str) -> Image.Image:
    W, H = base.size
    logo_w = int(W * 0.15)
    logo = Image.open(logo_path).convert("RGBA")
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
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

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k in ["thumbnail", "rendered_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ── TABS ───────────────────────────────────────────────────────────────────────
tab_v, tab_p = st.tabs(["// VIDÉO", "// PHOTO"])

# ══════════════════════ VIDÉO ══════════════════════════════════════════════════
with tab_v:

    st.markdown("""
    <div class="section-block">
      <span class="section-num">01</span>
      <p class="section-label">Fichier source</p>
    </div>
    """, unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposez votre vidéo ici",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu"
    )

    st.markdown("""
    <div class="section-block">
      <span class="section-num">02</span>
      <p class="section-label">Logo PNG transparent</p>
    </div>
    """, unsafe_allow_html=True)
    logo_v = st.file_uploader(
        "Déposez votre logo ici",
        type=["png"],
        key="vl"
    )

    if video_file and logo_v:
        tmp = tempfile.mkdtemp()
        vp = os.path.join(tmp, "src" + os.path.splitext(video_file.name)[1])
        lp = os.path.join(tmp, "logo.png")
        with open(vp, "wb") as f: f.write(video_file.read())
        with open(lp, "wb") as f: f.write(logo_v.read())

        nfo = get_video_info(vp)
        dur_s = f"{int(nfo['duration']//60)}:{int(nfo['duration']%60):02d}"

        st.markdown(f"""
        <div class="specs-band">
          <div class="spec-item">
            <span class="spec-key">Largeur</span>
            <span class="spec-val">{nfo['width']}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Hauteur</span>
            <span class="spec-val">{nfo['height']}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Durée</span>
            <span class="spec-val">{dur_s}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">FPS</span>
            <span class="spec-val">{nfo['fps']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.thumbnail is None:
            with st.spinner("// chargement aperçu..."):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown("""
        <div class="preview-shell">
          <div class="preview-topbar">
            <div class="preview-dot"></div>
            <div class="preview-dot"></div>
            <div class="preview-dot g"></div>
            <span class="preview-title-bar">PREVIEW — FRAME 0001</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("GÉNÉRER LE RENDU", key="vbtn",
                     disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_p, ph_s = st.empty(), st.empty()
            bar = ph_p.progress(0.0, text="")
            ph_s.markdown('<div class="status status-warn">TRAITEMENT EN COURS...</div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo,
                             lambda p: bar.progress(p, text=f"// {int(p*100)}% ENCODÉ"))
                bar.progress(1.0, text="// 100% ENCODÉ")
                ph_s.markdown('<div class="status status-ok">RENDER COMPLETE — FICHIER PRÊT</div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">ERREUR: {e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button(
                "↓ TÉLÉCHARGER LA VIDÉO",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="vdl"
            )
    else:
        st.markdown('<div class="status status-idle">EN ATTENTE D\'INPUT...</div>', unsafe_allow_html=True)

# ══════════════════════ PHOTO ══════════════════════════════════════════════════
with tab_p:

    st.markdown("""
    <div class="section-block">
      <span class="section-num">01</span>
      <p class="section-label">Image source</p>
    </div>
    """, unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposez votre image ici",
        type=["png", "jpg", "jpeg"],
        key="pu"
    )

    st.markdown("""
    <div class="section-block">
      <span class="section-num">02</span>
      <p class="section-label">Logo PNG transparent</p>
    </div>
    """, unsafe_allow_html=True)
    logo_p = st.file_uploader(
        "Déposez votre logo ici",
        type=["png"],
        key="pl"
    )

    if photo_file and logo_p:
        base = Image.open(photo_file)
        W, H = base.size
        tmp2 = tempfile.mkdtemp()
        lp2 = os.path.join(tmp2, "logo.png")
        with open(lp2, "wb") as f: f.write(logo_p.read())

        fmt = (base.format or photo_file.name.rsplit(".", 1)[-1]).upper()
        st.markdown(f"""
        <div class="specs-band">
          <div class="spec-item">
            <span class="spec-key">Largeur</span>
            <span class="spec-val">{W}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Hauteur</span>
            <span class="spec-val">{H}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Format</span>
            <span class="spec-val">{fmt}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Logo</span>
            <span class="spec-val">{int(W*0.15)}px</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        result_img = composite_logo(base, lp2)

        st.markdown("""
        <div class="preview-shell">
          <div class="preview-topbar">
            <div class="preview-dot"></div>
            <div class="preview-dot"></div>
            <div class="preview-dot g"></div>
            <span class="preview-title-bar">PREVIEW — OUTPUT</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)

        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result_img.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result_img.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"

        st.markdown('<div class="status status-ok">OUTPUT READY</div>', unsafe_allow_html=True)
        st.download_button(
            "↓ TÉLÉCHARGER LA PHOTO",
            data=buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="pdl"
        )
    else:
        st.markdown('<div class="status status-idle">EN ATTENTE D\'INPUT...</div>', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span class="footer-name">LUCAS BESSONNAT</span>
  <span class="footer-legal">Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
