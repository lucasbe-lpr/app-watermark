import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io

st.set_page_config(
    page_title="Luluflix",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&family=DM+Mono:wght@300;400&display=swap');

:root {
  --bg:      #0c0c0e;
  --surface: #131316;
  --border:  #222228;
  --gold:    #c9a96e;
  --gold2:   #e8c98a;
  --white:   #f0ede8;
  --muted:   #555560;
  --green:   #4caf7d;
  --red:     #e05252;
  --amber:   #d4a843;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container {
  background: var(--bg) !important;
  color: var(--white) !important;
  font-family: 'DM Mono', monospace !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }

.block-container { padding: 0 1rem 3rem !important; max-width: 680px !important; }

/* ── HERO ── */
.hero {
  padding: 5rem 0 3.5rem;
  text-align: center;
  position: relative;
}
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: clamp(5rem, 16vw, 9rem);
  line-height: 0.9;
  letter-spacing: -0.02em;
  color: var(--white);
  margin: 0;
  animation: fadeUp 0.9s cubic-bezier(0.16,1,0.3,1) both;
}
.hero-title em {
  font-style: italic;
  color: var(--gold);
}
.hero-rule {
  width: 40px;
  height: 1px;
  background: var(--gold);
  margin: 1.8rem auto 0;
  opacity: 0.6;
  animation: fadeUp 0.9s 0.15s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes fadeUp {
  from { opacity:0; transform:translateY(18px); }
  to   { opacity:1; transform:translateY(0); }
}

/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  margin-bottom: 2rem !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  color: var(--muted) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.65rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 0.6rem 1.6rem !important;
  border-bottom: 1px solid transparent !important;
  transition: color 0.2s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 1px solid var(--gold) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--white) !important;
}

/* ── UPLOAD ZONES ── */
.upload-wrap { margin-bottom: 1rem; }
.upload-label {
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.5rem;
}
[data-testid="stFileUploader"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 2px !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover {
  border-color: var(--gold) !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploaderDropzoneInstructions"] {
  color: var(--muted) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.72rem !important;
}
[data-testid="stFileUploaderFileName"] {
  color: var(--white) !important;
  font-size: 0.72rem !important;
}

/* ── SPECS BAND ── */
.specs-band {
  display: flex;
  gap: 2rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin: 1.5rem 0;
  animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
.spec-item { display: flex; flex-direction: column; gap: 0.2rem; }
.spec-key  { font-size: 0.52rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); }
.spec-val  { font-size: 0.8rem; color: var(--white); }

/* ── PREVIEW ── */
.preview-wrap {
  border: 1px solid var(--border);
  overflow: hidden;
  margin-bottom: 1.5rem;
  background: #000;
  position: relative;
}
.preview-label {
  position: absolute; top: 0.6rem; left: 0.8rem;
  font-size: 0.5rem; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--gold);
  opacity: 0.7; z-index: 2;
}

/* ── BUTTONS ── */
div.stButton > button {
  width: 100%;
  background: transparent !important;
  border: 1px solid var(--gold) !important;
  color: var(--gold) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.65rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  padding: 0.85rem 1rem !important;
  border-radius: 1px !important;
  transition: all 0.2s !important;
}
div.stButton > button:hover {
  background: var(--gold) !important;
  color: #0c0c0e !important;
}
div.stButton > button:disabled {
  border-color: var(--border) !important;
  color: var(--muted) !important;
}

div[data-testid="stDownloadButton"] > button {
  width: 100%;
  background: var(--gold) !important;
  border: none !important;
  color: #0c0c0e !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.65rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  padding: 0.85rem 1rem !important;
  border-radius: 1px !important;
  transition: background 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: var(--gold2) !important;
}

/* ── PROGRESS ── */
div[data-testid="stProgress"] > div {
  background: var(--border) !important;
  border-radius: 0 !important;
  height: 2px !important;
}
div[data-testid="stProgress"] > div > div {
  background: var(--gold) !important;
  border-radius: 0 !important;
}

/* ── STATUS PILLS ── */
.status {
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  padding: 0.5rem 0.8rem;
  border-left: 2px solid;
  margin: 0.8rem 0;
}
.status-ok   { border-color: var(--green); color: var(--green); background: #4caf7d0d; }
.status-warn { border-color: var(--amber); color: var(--amber); background: #d4a8430d; }
.status-err  { border-color: var(--red);   color: var(--red);   background: #e052520d; }
.status-idle { border-color: var(--border); color: var(--muted); }

/* ── DIVIDER ── */
.thin-rule { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── FOOTER ── */
.footer {
  margin-top: 4rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.55rem;
  letter-spacing: 0.12em;
  color: var(--muted);
}
.footer-name { color: var(--gold); opacity: 0.7; }

/* ── SPINNER ── */
div[data-testid="stSpinner"] p { color: var(--muted) !important; font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1 class="hero-title">Lulu<em>flix</em></h1>
  <div class="hero-rule"></div>
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
    margin_x = int(W * 0.05)
    margin_y = int(H * 0.07)
    x = W - logo_w - margin_x
    y = margin_y
    out = base.convert("RGBA")
    out.paste(logo, (x, y), logo)
    return out

def get_video_info(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
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
    frame_cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ]
    result = subprocess.run(frame_cmd, capture_output=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGBA")
    return composite_logo(frame, logo_path).convert("RGB")

def render_video(video_path: str, logo_path: str, output_path: str, info: dict, progress_cb=None):
    W, H = info["width"], info["height"]
    logo_w = int(W * 0.15)
    x = W - logo_w - int(W * 0.05)
    y = int(H * 0.07)
    filter_complex = (
        f"[1:v]scale={logo_w}:-1[logo];"
        f"[0:v][logo]overlay={x}:{y}"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path, "-i", logo_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy", "-movflags", "+faststart",
        "-progress", "pipe:1",
        output_path
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    total = info["duration"]
    while True:
        line = process.stdout.readline()
        if not line:
            break
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

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k in ["thumbnail", "rendered_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_v, tab_p = st.tabs(["Vidéo", "Photo"])

# ════════════════════════════════ VIDÉO ══════════════════════════════════════
with tab_v:
    st.markdown('<div class="upload-wrap"><div class="upload-label">Source</div>', unsafe_allow_html=True)
    video_file = st.file_uploader(" ", type=["mp4","mov","avi","mkv","webm"], label_visibility="collapsed", key="vu")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="upload-wrap"><div class="upload-label">Logo — PNG</div>', unsafe_allow_html=True)
    logo_v = st.file_uploader(" ", type=["png"], label_visibility="collapsed", key="vl")
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
          <div class="spec-item"><span class="spec-key">Résolution</span><span class="spec-val">{nfo['width']}×{nfo['height']}</span></div>
          <div class="spec-item"><span class="spec-key">Durée</span><span class="spec-val">{dur_s}</span></div>
          <div class="spec-item"><span class="spec-key">FPS</span><span class="spec-val">{nfo['fps']}</span></div>
          <div class="spec-item"><span class="spec-key">Logo</span><span class="spec-val">{int(nfo['width']*0.15)} px</span></div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.thumbnail is None:
            with st.spinner(""):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown('<div class="preview-wrap"><span class="preview-label">Aperçu</span>', unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Générer", key="vbtn", disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_p, ph_s = st.empty(), st.empty()
            bar = ph_p.progress(0.0, text="")
            ph_s.markdown('<div class="status status-warn">Traitement en cours…</div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo, lambda p: bar.progress(p, text=f"{int(p*100)} %"))
                bar.progress(1.0, text="100 %")
                ph_s.markdown('<div class="status status-ok">Prêt.</div>', unsafe_allow_html=True)
                with open(out, "rb") as f: st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">{e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button("Télécharger", data=st.session_state.rendered_bytes,
                               file_name="video_ready_to_post.mp4", mime="video/mp4", key="vdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo et un logo.</div>', unsafe_allow_html=True)

# ════════════════════════════════ PHOTO ══════════════════════════════════════
with tab_p:
    st.markdown('<div class="upload-wrap"><div class="upload-label">Source</div>', unsafe_allow_html=True)
    photo_file = st.file_uploader(" ", type=["png","jpg","jpeg"], label_visibility="collapsed", key="pu")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="upload-wrap"><div class="upload-label">Logo — PNG</div>', unsafe_allow_html=True)
    logo_p = st.file_uploader(" ", type=["png"], label_visibility="collapsed", key="pl")
    st.markdown('</div>', unsafe_allow_html=True)

    if photo_file and logo_p:
        base = Image.open(photo_file)
        W, H = base.size
        tmp2 = tempfile.mkdtemp()
        lp2 = os.path.join(tmp2, "logo.png")
        with open(lp2, "wb") as f: f.write(logo_p.read())

        st.markdown(f"""
        <div class="specs-band">
          <div class="spec-item"><span class="spec-key">Résolution</span><span class="spec-val">{W}×{H}</span></div>
          <div class="spec-item"><span class="spec-key">Format</span><span class="spec-val">{(base.format or photo_file.name.rsplit('.',1)[-1]).upper()}</span></div>
          <div class="spec-item"><span class="spec-key">Logo</span><span class="spec-val">{int(W*0.15)} px</span></div>
        </div>
        """, unsafe_allow_html=True)

        result = composite_logo(base, lp2)

        st.markdown('<div class="preview-wrap"><span class="preview-label">Aperçu</span>', unsafe_allow_html=True)
        st.image(result.convert("RGB"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"

        st.markdown('<div class="status status-ok">Prêt.</div>', unsafe_allow_html=True)
        st.download_button("Télécharger", data=buf.getvalue(), file_name=fname, mime=mime, key="pdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une image et un logo.</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span class="footer-name">Lucas Bessonnat</span>
  <span>Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
