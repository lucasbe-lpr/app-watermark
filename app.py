import streamlit as st
import subprocess
import tempfile
import os
import shutil
from PIL import Image
import numpy as np
import io
import time

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WATERMARK_GEN",
    page_icon="⌗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS : RÉTRO NERD ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --bg:       #0d0d0d;
  --panel:    #111111;
  --border:   #2a2a2a;
  --green:    #00ff88;
  --amber:    #ffb800;
  --red:      #ff3c3c;
  --dim:      #555555;
  --text:     #e0e0e0;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'IBM Plex Mono', monospace !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── HEADER ── */
.header-block {
  text-align: center;
  padding: 2.5rem 0 1.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
}
.header-title {
  font-family: 'VT323', monospace;
  font-size: 3.8rem;
  color: var(--green);
  letter-spacing: 0.15em;
  line-height: 1;
  text-shadow: 0 0 20px #00ff8855;
  margin: 0;
}
.header-sub {
  font-size: 0.7rem;
  color: var(--dim);
  letter-spacing: 0.3em;
  margin-top: 0.4rem;
}

/* ── PANELS ── */
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 1.5rem;
  margin-bottom: 1.2rem;
  position: relative;
}
.panel-label {
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  color: var(--amber);
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.panel-label::before { content: "▶"; font-size: 0.5rem; }

/* ── UPLOADER OVERRIDE ── */
[data-testid="stFileUploader"] {
  background: #0a0a0a !important;
  border: 1px dashed var(--border) !important;
  border-radius: 2px !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--green) !important;
}
[data-testid="stFileUploader"] label { color: var(--dim) !important; font-size: 0.75rem !important; }

/* ── BUTTON ── */
div.stButton > button {
  width: 100%;
  background: transparent !important;
  border: 1px solid var(--green) !important;
  color: var(--green) !important;
  font-family: 'VT323', monospace !important;
  font-size: 1.8rem !important;
  letter-spacing: 0.2em !important;
  padding: 0.6rem !important;
  border-radius: 2px !important;
  transition: all 0.15s !important;
  text-shadow: 0 0 8px #00ff8888 !important;
}
div.stButton > button:hover {
  background: var(--green) !important;
  color: #000 !important;
  text-shadow: none !important;
  box-shadow: 0 0 20px #00ff8855 !important;
}
div.stButton > button:disabled {
  border-color: var(--dim) !important;
  color: var(--dim) !important;
  text-shadow: none !important;
}

/* ── DOWNLOAD BUTTON ── */
div[data-testid="stDownloadButton"] > button {
  width: 100%;
  background: var(--green) !important;
  border: none !important;
  color: #000 !important;
  font-family: 'VT323', monospace !important;
  font-size: 1.8rem !important;
  letter-spacing: 0.2em !important;
  padding: 0.6rem !important;
  border-radius: 2px !important;
  font-weight: bold !important;
}

/* ── PROGRESS ── */
.progress-wrap {
  background: #0a0a0a;
  border: 1px solid var(--border);
  height: 6px;
  border-radius: 1px;
  margin: 1rem 0;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  transition: width 0.3s ease;
}
.status-line {
  font-size: 0.65rem;
  color: var(--dim);
  letter-spacing: 0.15em;
  margin-top: 0.3rem;
}
.status-ok { color: var(--green); }
.status-warn { color: var(--amber); }
.status-err { color: var(--red); }

/* ── PREVIEW ── */
.preview-wrap {
  border: 1px solid var(--border);
  border-radius: 2px;
  overflow: hidden;
  background: #000;
}
.preview-wrap img {
  width: 100%;
  display: block;
}

/* ── SPECS TABLE ── */
.specs {
  font-size: 0.62rem;
  color: var(--dim);
  letter-spacing: 0.1em;
  line-height: 2;
}
.specs span { color: var(--text); }

/* ── SCANLINES EFFECT ── */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.04) 2px,
    rgba(0,0,0,0.04) 4px
  );
  pointer-events: none;
  z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
  <p class="header-title">⌗ WATERMARK_GEN</p>
  <p class="header-sub">VIDEO BRANDING SYSTEM · V1.0 · READY TO PUBLISH</p>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_video_info(path: str) -> dict:
    """Extract width, height, duration via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=0",
        path
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
    """Grab first frame, composite logo, return PIL Image."""
    W, H = info["width"], info["height"]
    # extract frame
    frame_cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ]
    result = subprocess.run(frame_cmd, capture_output=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGBA")

    # compute logo placement
    logo_w = int(W * 0.15)
    logo = Image.open(logo_path).convert("RGBA")
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    margin_x = int(W * 0.05)
    margin_y = int(H * 0.07)
    x = W - logo_w - margin_x
    y = margin_y

    frame.paste(logo, (x, y), logo)
    return frame.convert("RGB")


def render_video(video_path: str, logo_path: str, output_path: str, info: dict, progress_cb=None):
    """Overlay logo on every frame using ffmpeg filter_complex."""
    W, H = info["width"], info["height"]
    logo_w = int(W * 0.15)
    margin_x = int(W * 0.05)
    margin_y = int(H * 0.07)
    x = W - logo_w - margin_x
    y = margin_y

    # Scale logo to target width, preserve aspect ratio
    scale_filter = f"scale={logo_w}:-1"

    filter_complex = (
        f"[1:v]{scale_filter}[logo];"
        f"[0:v][logo]overlay={x}:{y}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", logo_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264",
        "-crf", "18",          # near-lossless quality
        "-preset", "fast",
        "-c:a", "copy",        # audio passthrough (no quality loss)
        "-movflags", "+faststart",
        "-progress", "pipe:1",
        output_path
    ]

    total_dur = info["duration"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith("out_time_ms="):
            try:
                ms = int(line.split("=")[1])
                elapsed_s = ms / 1_000_000
                if total_dur > 0 and progress_cb:
                    pct = min(elapsed_s / total_dur, 1.0)
                    progress_cb(pct)
            except Exception:
                pass

    process.wait()
    if process.returncode != 0:
        err = process.stderr.read()
        raise RuntimeError(f"FFmpeg error:\n{err}")


# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "thumbnail" not in st.session_state:
    st.session_state.thumbnail = None
if "rendered_bytes" not in st.session_state:
    st.session_state.rendered_bytes = None

# ─── UPLOAD PANEL ──────────────────────────────────────────────────────────────
st.markdown('<div class="panel"><div class="panel-label">01 · SOURCE</div>', unsafe_allow_html=True)
video_file = st.file_uploader(
    "Vidéo source",
    type=["mp4", "mov", "avi", "mkv", "webm"],
    label_visibility="collapsed",
    help="MP4 · MOV · AVI · MKV · WEBM"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="panel"><div class="panel-label">02 · LOGO</div>', unsafe_allow_html=True)
logo_file = st.file_uploader(
    "Logo PNG transparent",
    type=["png"],
    label_visibility="collapsed",
    help="PNG avec transparence (canal alpha)"
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── PREVIEW PANEL ─────────────────────────────────────────────────────────────
if video_file and logo_file:
    # Write to temp files
    tmp_dir = tempfile.mkdtemp()
    vid_path = os.path.join(tmp_dir, "source" + os.path.splitext(video_file.name)[1])
    logo_path = os.path.join(tmp_dir, "logo.png")

    with open(vid_path, "wb") as f:
        f.write(video_file.read())
    with open(logo_path, "wb") as f:
        f.write(logo_file.read())

    info = get_video_info(vid_path)

    # Specs
    dur_str = f"{int(info['duration']//60)}:{int(info['duration']%60):02d}"
    st.markdown(f"""
    <div class="panel">
      <div class="panel-label">03 · SPECS</div>
      <div class="specs">
        RÉSOLUTION&nbsp;&nbsp;<span>{info['width']} × {info['height']} px</span><br>
        DURÉE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span>{dur_str}</span><br>
        FPS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span>{info['fps']}</span><br>
        LOGO&nbsp;W&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span>{int(info['width']*0.15)} px (15% de la largeur)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Thumbnail preview
    st.markdown('<div class="panel"><div class="panel-label">04 · PRÉVISUALISATION (THUMBNAIL)</div>', unsafe_allow_html=True)
    if st.session_state.thumbnail is None:
        with st.spinner("Génération du thumbnail…"):
            thumb = make_thumbnail(vid_path, logo_path, info)
            st.session_state.thumbnail = thumb

    thumb_buf = io.BytesIO()
    st.session_state.thumbnail.save(thumb_buf, format="JPEG", quality=90)
    st.image(st.session_state.thumbnail, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── RENDER BUTTON ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⌗ GÉNÉRER LE RENDU FINAL", key="render_btn", disabled=(st.session_state.rendered_bytes is not None)):
        out_path = os.path.join(tmp_dir, "video_ready_to_post.mp4")

        prog_ph = st.empty()
        status_ph = st.empty()

        progress_bar = prog_ph.progress(0.0, text="")

        def update_progress(pct: float):
            label = f"Rendu… {int(pct*100)}%"
            progress_bar.progress(pct, text=label)

        try:
            status_ph.markdown('<p class="status-line status-warn">⬡ TRAITEMENT EN COURS…</p>', unsafe_allow_html=True)
            render_video(vid_path, logo_path, out_path, info, progress_cb=update_progress)
            progress_bar.progress(1.0, text="100%")
            status_ph.markdown('<p class="status-line status-ok">✔ RENDU TERMINÉ — PRÊT À PUBLIER</p>', unsafe_allow_html=True)
            with open(out_path, "rb") as f:
                st.session_state.rendered_bytes = f.read()
        except Exception as e:
            status_ph.markdown(f'<p class="status-line status-err">✖ ERREUR : {e}</p>', unsafe_allow_html=True)
            st.stop()

    # ── DOWNLOAD BUTTON ──────────────────────────────────────────────────────
    if st.session_state.rendered_bytes:
        st.download_button(
            label="⬇ TÉLÉCHARGER video_ready_to_post.mp4",
            data=st.session_state.rendered_bytes,
            file_name="video_ready_to_post.mp4",
            mime="video/mp4",
        )

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0; color: #333; font-size: 0.65rem; letter-spacing: 0.3em;">
      ↑ UPLOAD VIDÉO + LOGO POUR COMMENCER
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #1a1a1a; margin-top:3rem; padding-top:1rem;
            text-align:center; font-size:0.55rem; color:#333; letter-spacing:0.3em;">
  NO DATA STORED · PROCESSING IS LOCAL · RGPD COMPLIANT
</div>
""", unsafe_allow_html=True)
