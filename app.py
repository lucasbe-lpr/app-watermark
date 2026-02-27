import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io

st.set_page_config(
    page_title="Luluflix",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100;0,9..144,300;1,9..144,100;1,9..144,300&family=Instrument+Sans:wght@300;400;500&display=swap');

:root {
  --bg-base:    #14100d;
  --bg-mid:     #1c1612;
  --glass:      rgba(255,248,235,0.045);
  --glass-h:    rgba(255,248,235,0.07);
  --border:     rgba(255,220,160,0.10);
  --border-h:   rgba(255,220,160,0.25);
  --amber:      #e8b96a;
  --amber-glow: rgba(232,185,106,0.18);
  --white:      #f5ede0;
  --muted:      rgba(245,237,224,0.38);
  --muted2:     rgba(245,237,224,0.18);
  --green:      #6fcf8e;
  --green-glow: rgba(111,207,142,0.15);
  --red:        #e07070;
  --warn:       #d4a843;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background: var(--bg-base) !important;
  color: var(--white) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-weight: 300 !important;
}

.block-container {
  background: transparent !important;
  padding: 0 2rem 5rem !important;
  max-width: 720px !important;
}

/* Ambient glow background */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  top: -20vh; left: 50%;
  transform: translateX(-50%);
  width: 70vw; height: 60vh;
  background: radial-gradient(ellipse at center,
    rgba(200,140,60,0.07) 0%,
    rgba(180,100,40,0.04) 40%,
    transparent 70%);
  pointer-events: none;
  z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  bottom: -10vh; right: -10vw;
  width: 50vw; height: 50vh;
  background: radial-gradient(ellipse at center,
    rgba(60,100,180,0.05) 0%,
    transparent 65%);
  pointer-events: none;
  z-index: 0;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── HEADER ── */
.site-header {
  padding: 4.5rem 0 2.5rem;
  text-align: center;
  position: relative;
  z-index: 1;
}
.header-eyebrow {
  font-family: 'Instrument Sans', sans-serif;
  font-size: 0.58rem;
  font-weight: 400;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 1rem;
  opacity: 0.8;
}
.header-title {
  font-family: 'Fraunces', serif;
  font-weight: 100;
  font-style: italic;
  font-size: clamp(4.5rem, 16vw, 8.5rem);
  line-height: 0.88;
  color: var(--white);
  letter-spacing: -0.02em;
  margin: 0;
}
.header-title span {
  color: var(--amber);
  font-weight: 300;
}
.header-divider {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, var(--border-h), transparent);
  margin: 1.8rem auto 0;
}

/* ── GLASS CARD ── */
.glass-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 12px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, background 0.2s;
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,220,160,0.2) 30%,
    rgba(255,220,160,0.2) 70%,
    transparent);
}
.glass-card:hover {
  background: var(--glass-h);
  border-color: var(--border-h);
}
.card-label {
  font-size: 0.55rem;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 0.9rem;
  opacity: 0.9;
}

/* ── TABS ── */
div[data-testid="stTabs"] {
  position: relative;
  z-index: 1;
}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  margin: 0 0 1.8rem !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 1px solid transparent !important;
  margin-bottom: -1px !important;
  color: var(--muted) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.65rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase !important;
  padding: 0.65rem 2rem 0.65rem 0 !important;
  transition: color 0.2s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--amber) !important;
  border-bottom: 1px solid var(--amber) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--white) !important;
}
/* Supprime TOUT indicateur rouge/bleu injecté par Streamlit */
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {
  background: transparent !important;
  background-color: transparent !important;
  display: none !important;
}

/* ── UPLOADER ── */
[data-testid="stFileUploader"] {
  background: transparent !important;
}
[data-testid="stFileUploader"] section {
  background: rgba(255,248,235,0.025) !important;
  border: 1px dashed var(--border-h) !important;
  border-radius: 8px !important;
  padding: 1.6rem 1.4rem !important;
  transition: all 0.2s !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  background: rgba(232,185,106,0.05) !important;
  border-color: var(--amber) !important;
  box-shadow: 0 0 0 3px var(--amber-glow) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--muted) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.8rem !important;
  font-weight: 300 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: var(--white) !important;
  font-weight: 400 !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
  background: transparent !important;
  border: 1px solid var(--border-h) !important;
  color: var(--white) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.08em !important;
  padding: 0.35rem 1rem !important;
  border-radius: 4px !important;
  transition: all 0.15s !important;
}
[data-testid="stFileUploader"] button:hover {
  background: var(--amber-glow) !important;
  border-color: var(--amber) !important;
  color: var(--amber) !important;
}
[data-testid="stFileUploaderFileName"] {
  color: var(--amber) !important;
  font-size: 0.75rem !important;
  font-weight: 400 !important;
}

/* ── SPECS ── */
.specs-band {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin: 1.4rem 0;
}
.spec-item {
  background: var(--bg-mid);
  padding: 0.9rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.spec-key {
  font-size: 0.48rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 400;
}
.spec-val {
  font-family: 'Fraunces', serif;
  font-weight: 100;
  font-size: 1.25rem;
  color: var(--white);
  line-height: 1;
}

/* ── PREVIEW ── */
.preview-shell {
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 1.4rem;
  background: #000;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.preview-topbar {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 0.9rem;
  background: rgba(255,248,235,0.04);
  border-bottom: 1px solid var(--border);
}
.pdot { width: 7px; height: 7px; border-radius: 50%; }
.pdot-r { background: rgba(255,255,255,0.12); }
.pdot-y { background: rgba(255,255,255,0.12); }
.pdot-g { background: var(--amber); opacity: 0.7; }
.preview-filename {
  font-size: 0.5rem;
  letter-spacing: 0.14em;
  color: var(--muted2);
  margin-left: 0.4rem;
  font-weight: 400;
}

/* ── BUTTONS ── */
div.stButton > button {
  width: 100% !important;
  background: var(--glass) !important;
  border: 1px solid var(--border-h) !important;
  color: var(--white) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 0.85rem 1rem !important;
  border-radius: 8px !important;
  transition: all 0.2s !important;
  backdrop-filter: blur(8px) !important;
}
div.stButton > button:hover {
  background: var(--amber-glow) !important;
  border-color: var(--amber) !important;
  color: var(--amber) !important;
  box-shadow: 0 0 20px var(--amber-glow) !important;
}
div.stButton > button:disabled {
  opacity: 0.3 !important;
  cursor: not-allowed !important;
}

div[data-testid="stDownloadButton"] > button {
  width: 100% !important;
  background: var(--green-glow) !important;
  border: 1px solid rgba(111,207,142,0.35) !important;
  color: var(--green) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 0.85rem 1rem !important;
  border-radius: 8px !important;
  transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: rgba(111,207,142,0.22) !important;
  box-shadow: 0 0 20px var(--green-glow) !important;
}

/* ── PROGRESS ── */
div[data-testid="stProgress"] > div {
  background: var(--border) !important;
  border-radius: 99px !important;
  height: 3px !important;
}
div[data-testid="stProgress"] > div > div {
  background: linear-gradient(90deg, var(--amber), var(--green)) !important;
  border-radius: 99px !important;
}
div[data-testid="stProgress"] p {
  font-size: 0.6rem !important;
  color: var(--muted) !important;
  letter-spacing: 0.1em !important;
  font-family: 'Instrument Sans', sans-serif !important;
}

/* ── STATUS ── */
.status {
  font-size: 0.65rem;
  font-weight: 300;
  letter-spacing: 0.06em;
  padding: 0.65rem 1rem;
  border-radius: 6px;
  border: 1px solid;
  margin: 0.8rem 0;
  font-family: 'Instrument Sans', sans-serif;
}
.status-ok   {
  border-color: rgba(111,207,142,0.3);
  color: var(--green);
  background: var(--green-glow);
}
.status-warn {
  border-color: rgba(212,168,67,0.3);
  color: var(--warn);
  background: rgba(212,168,67,0.07);
}
.status-err  {
  border-color: rgba(224,112,112,0.3);
  color: var(--red);
  background: rgba(224,112,112,0.07);
}
.status-idle {
  border-color: var(--border);
  color: var(--muted);
  background: transparent;
}

/* ── FOOTER ── */
.footer {
  margin-top: 5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.footer-name {
  font-family: 'Fraunces', serif;
  font-weight: 100;
  font-style: italic;
  font-size: 1rem;
  color: var(--amber);
  opacity: 0.8;
}
.footer-legal {
  font-size: 0.52rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted2);
}

/* Spinner */
div[data-testid="stSpinner"] p {
  color: var(--muted) !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.08em !important;
}

/* Ensure all content above pseudo-elements */
div[data-testid="stTabs"],
.glass-card, [data-testid="stFileUploader"],
div.stButton, div[data-testid="stDownloadButton"],
.specs-band, .preview-shell, .status, .footer {
  position: relative;
  z-index: 1;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
  <p class="header-eyebrow">Watermark Engine</p>
  <h1 class="header-title">Lulu<span>flix</span></h1>
  <div class="header-divider"></div>
</div>
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
tab_v, tab_p = st.tabs(["Vidéo", "Photo"])

# ═══════════════════════════════ VIDÉO ════════════════════════════════════════
with tab_v:

    st.markdown('<div class="glass-card"><p class="card-label">Source</p>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposez votre vidéo ici",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><p class="card-label">Logo — PNG transparent</p>', unsafe_allow_html=True)
    logo_v = st.file_uploader(
        "Déposez votre logo ici",
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
            with st.spinner("Génération de l'aperçu…"):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown("""
        <div class="preview-shell">
          <div class="preview-topbar">
            <div class="pdot pdot-r"></div>
            <div class="pdot pdot-y"></div>
            <div class="pdot pdot-g"></div>
            <span class="preview-filename">aperçu — image 0</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Générer le rendu", key="vbtn",
                     disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_p, ph_s = st.empty(), st.empty()
            bar = ph_p.progress(0.0, text="")
            ph_s.markdown('<div class="status status-warn">Traitement en cours…</div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo,
                             lambda p: bar.progress(p, text=f"{int(p*100)} %"))
                bar.progress(1.0, text="100 %")
                ph_s.markdown('<div class="status status-ok">Rendu terminé — fichier prêt.</div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">{e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button(
                "↓ Télécharger la vidéo",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="vdl"
            )

    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo et un logo pour commencer.</div>', unsafe_allow_html=True)


# ═══════════════════════════════ PHOTO ════════════════════════════════════════
with tab_p:

    st.markdown('<div class="glass-card"><p class="card-label">Source</p>', unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposez votre image ici",
        type=["png", "jpg", "jpeg"],
        key="pu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><p class="card-label">Logo — PNG transparent</p>', unsafe_allow_html=True)
    logo_p = st.file_uploader(
        "Déposez votre logo ici",
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
            <div class="pdot pdot-r"></div>
            <div class="pdot pdot-y"></div>
            <div class="pdot pdot-g"></div>
            <span class="preview-filename">aperçu — output</span>
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

        st.markdown('<div class="status status-ok">Prêt.</div>', unsafe_allow_html=True)
        st.download_button(
            "↓ Télécharger la photo",
            data=buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="pdl"
        )

    else:
        st.markdown('<div class="status status-idle">Déposez une image et un logo pour commencer.</div>', unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span class="footer-name">Lucas Bessonnat</span>
  <span class="footer-legal">Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
