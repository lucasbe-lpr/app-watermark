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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,300&display=swap');

:root {
  --ink:       #111111;
  --ink-light: #444444;
  --rule:      #111111;
  --cream:     #faf9f7;
  --warm-bg:   #f3f1ee;
  --border:    #d8d5d0;
  --accent:    #111111;
  --green:     #1a6b3a;
  --red:       #b81c1c;
  --amber:     #7a5c00;
  --muted:     #888880;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container {
  background: var(--cream) !important;
  color: var(--ink) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }

.block-container {
  padding: 0 1.5rem 4rem !important;
  max-width: 700px !important;
}

/* ─── MASTHEAD ─── */
.masthead {
  text-align: center;
  padding: 3.5rem 0 0;
  border-bottom: 3px solid var(--rule);
}
.masthead-eyebrow {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.62rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.6rem;
}
.masthead-title {
  font-family: 'Playfair Display', 'Times New Roman', serif;
  font-weight: 700;
  font-style: italic;
  font-size: clamp(4rem, 14vw, 7.5rem);
  line-height: 0.92;
  letter-spacing: -0.01em;
  color: var(--ink);
  margin: 0 0 0.5rem;
}
.masthead-rule-wrap {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0.8rem 0 0;
}
.masthead-rule-wrap hr {
  flex: 1;
  border: none;
  border-top: 1px solid var(--border);
  margin: 0;
}
.masthead-date {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.58rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  white-space: nowrap;
}

/* ─── SECTION LABELS (remplacement des panel-label) ─── */
.section-head {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.6rem;
  font-weight: 400;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 1.4rem 0 0.5rem;
  border-top: 1px solid var(--border);
  margin-top: 1.2rem;
  margin-bottom: 0.4rem;
}
.section-head:first-of-type { border-top: none; margin-top: 0; }

/* ─── UPLOADER — visible, contrasté ─── */
[data-testid="stFileUploader"] {
  background: #ffffff !important;
}
[data-testid="stFileUploader"] section {
  background: #ffffff !important;
  border: 1.5px dashed #999 !important;
  border-radius: 0 !important;
  padding: 1.4rem !important;
  transition: border-color 0.2s, background 0.2s !important;
  cursor: pointer !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  border-color: var(--ink) !important;
  background: var(--warm-bg) !important;
}
/* Texte interne de l'uploader */
[data-testid="stFileUploader"] section * {
  color: var(--ink-light) !important;
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: var(--ink) !important;
  font-size: 0.85rem !important;
}
/* Bouton "Browse files" */
[data-testid="stFileUploader"] section button,
[data-testid="stBaseButton-secondary"] {
  background: var(--ink) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 0 !important;
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.08em !important;
  padding: 0.4rem 0.9rem !important;
  margin-top: 0.5rem !important;
  cursor: pointer !important;
}
[data-testid="stFileUploader"] section button:hover {
  background: #333 !important;
}
/* Nom du fichier chargé */
[data-testid="stFileUploaderFileName"] {
  color: var(--ink) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
}

/* ─── TABS ─── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 2px solid var(--rule) !important;
  gap: 0 !important;
  margin-top: 2rem !important;
  margin-bottom: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  color: var(--muted) !important;
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  padding: 0.55rem 1.6rem 0.55rem 0 !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--ink) !important;
  border-bottom: 2px solid var(--ink) !important;
}

/* ─── SPECS BAND ─── */
.specs-band {
  display: flex;
  gap: 2.5rem;
  padding: 0.9rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin: 1.2rem 0 1.4rem;
}
.spec-item { display: flex; flex-direction: column; gap: 0.18rem; }
.spec-key {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.52rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
}
.spec-val {
  font-family: 'Playfair Display', 'Times New Roman', serif;
  font-size: 0.95rem;
  color: var(--ink);
}

/* ─── PREVIEW ─── */
.preview-wrap {
  border: 1px solid var(--border);
  overflow: hidden;
  margin-bottom: 1.4rem;
  background: #eee;
}
.preview-cap {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
  text-align: center;
}

/* ─── BUTTONS ─── */
div.stButton > button {
  width: 100% !important;
  background: var(--ink) !important;
  border: none !important;
  color: #fff !important;
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.72rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  padding: 0.8rem 1rem !important;
  border-radius: 0 !important;
  transition: background 0.15s !important;
  cursor: pointer !important;
}
div.stButton > button:hover { background: #333 !important; }
div.stButton > button:disabled { background: var(--border) !important; color: var(--muted) !important; }

div[data-testid="stDownloadButton"] > button {
  width: 100% !important;
  background: var(--green) !important;
  border: none !important;
  color: #fff !important;
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  padding: 0.8rem 1rem !important;
  border-radius: 0 !important;
  cursor: pointer !important;
}
div[data-testid="stDownloadButton"] > button:hover { background: #125029 !important; }

/* ─── PROGRESS ─── */
div[data-testid="stProgress"] > div {
  background: var(--border) !important;
  border-radius: 0 !important;
  height: 3px !important;
}
div[data-testid="stProgress"] > div > div {
  background: var(--ink) !important;
  border-radius: 0 !important;
}

/* ─── STATUS ─── */
.status {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  padding: 0.55rem 0.8rem;
  border-left: 2px solid;
  margin: 0.8rem 0;
}
.status-ok   { border-color: var(--green); color: var(--green); background: #f0faf4; }
.status-warn { border-color: var(--amber); color: var(--amber); background: #fdf8ec; }
.status-err  { border-color: var(--red);   color: var(--red);   background: #fdf0f0; }
.status-idle { border-color: var(--border); color: var(--muted); }

/* ─── FOOTER ─── */
.footer {
  margin-top: 4rem;
  padding-top: 1rem;
  border-top: 3px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  color: var(--muted);
}
.footer-name {
  font-family: 'Playfair Display', 'Times New Roman', serif;
  font-style: italic;
  font-size: 0.78rem;
  color: var(--ink);
}
</style>
""", unsafe_allow_html=True)

# ─── MASTHEAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <p class="masthead-eyebrow">Outil d'incrustation de logo</p>
  <h1 class="masthead-title">Luluflix</h1>
  <div class="masthead-rule-wrap">
    <hr/><span class="masthead-date">Usage interne</span><hr/>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

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

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for k in ["thumbnail", "rendered_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab_v, tab_p = st.tabs(["Vidéo", "Photo"])

# ══════════════════════════════════ VIDÉO ═════════════════════════════════════
with tab_v:

    st.markdown('<p class="section-head">Source</p>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposez votre vidéo ici",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu"
    )

    st.markdown('<p class="section-head">Logo — PNG transparent</p>', unsafe_allow_html=True)
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
            <span class="spec-key">Résolution</span>
            <span class="spec-val">{nfo['width']}×{nfo['height']}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Durée</span>
            <span class="spec-val">{dur_s}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">FPS</span>
            <span class="spec-val">{nfo['fps']}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Logo</span>
            <span class="spec-val">{int(nfo['width']*0.15)} px</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.thumbnail is None:
            with st.spinner("Génération de l'aperçu…"):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)

        st.markdown('<div class="preview-wrap"><p class="preview-cap">Aperçu — première image</p>', unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
                ph_s.markdown('<div class="status status-ok">Rendu terminé.</div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">{e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
            st.download_button(
                "Télécharger la vidéo",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="vdl"
            )
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo et un logo pour commencer.</div>', unsafe_allow_html=True)


# ══════════════════════════════════ PHOTO ═════════════════════════════════════
with tab_p:

    st.markdown('<p class="section-head">Source</p>', unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposez votre image ici",
        type=["png", "jpg", "jpeg"],
        key="pu"
    )

    st.markdown('<p class="section-head">Logo — PNG transparent</p>', unsafe_allow_html=True)
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

        st.markdown(f"""
        <div class="specs-band">
          <div class="spec-item">
            <span class="spec-key">Résolution</span>
            <span class="spec-val">{W}×{H}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Format</span>
            <span class="spec-val">{(base.format or photo_file.name.rsplit(".",1)[-1]).upper()}</span>
          </div>
          <div class="spec-item">
            <span class="spec-key">Logo</span>
            <span class="spec-val">{int(W*0.15)} px</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        result_img = composite_logo(base, lp2)

        st.markdown('<div class="preview-wrap"><p class="preview-cap">Aperçu</p>', unsafe_allow_html=True)
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

        st.markdown('<div class="status status-ok">Prêt.</div>', unsafe_allow_html=True)
        st.download_button(
            "Télécharger la photo",
            data=buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="pdl"
        )
    else:
        st.markdown('<div class="status status-idle">Déposez une image et un logo pour commencer.</div>', unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span class="footer-name">Lucas Bessonnat</span>
  <span>Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
