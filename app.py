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

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {{
  --blue:      #0068B1;
  --blue-mid:  #005a99;
  --blue-dark: #004880;
  --blue-pale: #e8f2fa;
  --blue-xpal: #f0f7fd;
  --white:     #ffffff;
  --bg:        #f7f8fa;
  --ink:       #111827;
  --muted:     #6b7280;
  --border:    #e5e7eb;
  --border-b:  #d0dce8;
  --green:     #16a34a;
  --green-bg:  #f0fdf4;
  --warn:      #d97706;
  --warn-bg:   #fffbeb;
  --red:       #dc2626;
  --red-bg:    #fef2f2;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
}}

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: 'Barlow', sans-serif !important;
  font-weight: 400 !important;
}}

.block-container {{
  background: transparent !important;
  padding: 0 1.5rem 4rem !important;
  max-width: 720px !important;
}}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{ display: none !important; }}

/* ─── HEADER ─── */
.site-header {{
  background: var(--white);
  border-bottom: 1px solid var(--border);
  padding: 0 1.5rem;
  margin: 0 -1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  box-shadow: var(--shadow-sm);
}}
.header-logo img {{
  height: 36px;
  width: auto;
  display: block;
}}
.header-badge {{
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--blue);
  background: var(--blue-pale);
  border: 1px solid var(--border-b);
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}}

/* ─── TABS ─── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  background: transparent !important;
  border-bottom: 2px solid var(--border) !important;
  gap: 0 !important;
  margin-bottom: 1.5rem !important;
  padding: 0 !important;
}}
div[data-testid="stTabs"] [data-baseweb="tab"] {{
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
  color: var(--muted) !important;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 0.6rem 1.4rem 0.6rem 0 !important;
  transition: color 0.15s !important;
}}
div[data-testid="stTabs"] [aria-selected="true"] {{
  color: var(--blue) !important;
  border-bottom: 2px solid var(--blue) !important;
}}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
  color: var(--ink) !important;
}}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {{
  display: none !important;
  background: transparent !important;
}}

/* ─── CARDS ─── */
.card {{
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
}}
.card-label {{
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}}
.card-label::before {{
  content: '';
  display: inline-block;
  width: 3px;
  height: 12px;
  background: var(--blue);
  border-radius: 2px;
}}

/* ─── UPLOADER ─── */
[data-testid="stFileUploader"] {{
  background: transparent !important;
}}
[data-testid="stFileUploader"] section {{
  background: var(--blue-xpal) !important;
  border: 1.5px dashed var(--border-b) !important;
  border-radius: 8px !important;
  padding: 1.4rem 1.2rem !important;
  transition: border-color 0.2s, background 0.2s !important;
}}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {{
  border-color: var(--blue) !important;
  background: var(--blue-pale) !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] * {{
  color: var(--muted) !important;
  font-family: 'Barlow', sans-serif !important;
  font-size: 0.85rem !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] span {{
  color: var(--ink) !important;
  font-weight: 500 !important;
}}
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {{
  background: var(--white) !important;
  border: 1.5px solid var(--blue) !important;
  color: var(--blue) !important;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  padding: 0.35rem 1rem !important;
  border-radius: 6px !important;
  transition: all 0.15s !important;
}}
[data-testid="stFileUploader"] button:hover {{
  background: var(--blue) !important;
  color: var(--white) !important;
}}
[data-testid="stFileUploaderFileName"] {{
  color: var(--blue-dark) !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
}}

/* ─── SPECS ─── */
.specs-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin: 0 0 1.2rem;
}}
.spec-item {{
  background: var(--white);
  padding: 0.85rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}}
.spec-key {{
  font-family: 'Barlow', sans-serif;
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}}
.spec-val {{
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}}

/* ─── PREVIEW ─── */
.preview-shell {{
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.2rem;
  background: #111;
  box-shadow: var(--shadow-sm);
}}
.preview-topbar {{
  background: var(--white);
  border-bottom: 1px solid var(--border);
  padding: 0.45rem 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.ptag {{
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--white);
  background: var(--blue);
  padding: 0.1rem 0.5rem;
  border-radius: 3px;
}}
.preview-name {{
  font-size: 0.7rem;
  color: var(--muted);
  font-family: 'Barlow', sans-serif;
}}

/* ─── BUTTONS ─── */
div.stButton > button {{
  width: 100% !important;
  background: var(--blue) !important;
  border: none !important;
  color: var(--white) !important;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 8px !important;
  transition: background 0.15s, transform 0.1s !important;
  box-shadow: 0 2px 8px rgba(0,104,177,0.3) !important;
}}
div.stButton > button:hover {{
  background: var(--blue-mid) !important;
  box-shadow: 0 4px 12px rgba(0,104,177,0.4) !important;
}}
div.stButton > button:active {{
  transform: translateY(1px) !important;
}}
div.stButton > button:disabled {{
  background: var(--border) !important;
  color: var(--muted) !important;
  box-shadow: none !important;
}}

div[data-testid="stDownloadButton"] > button {{
  width: 100% !important;
  background: var(--green) !important;
  border: none !important;
  color: var(--white) !important;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(22,163,74,0.25) !important;
  transition: background 0.15s !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{
  background: #15803d !important;
}}

/* ─── PROGRESS ─── */
div[data-testid="stProgress"] > div {{
  background: var(--border) !important;
  border-radius: 99px !important;
  height: 6px !important;
}}
div[data-testid="stProgress"] > div > div {{
  background: var(--blue) !important;
  border-radius: 99px !important;
}}
div[data-testid="stProgress"] p {{
  font-size: 0.72rem !important;
  color: var(--muted) !important;
  font-family: 'Barlow', sans-serif !important;
  font-weight: 500 !important;
}}

/* ─── STATUS ─── */
.status {{
  font-family: 'Barlow', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  border: 1px solid;
  margin: 0.8rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.status-ok   {{ border-color: #bbf7d0; color: var(--green); background: var(--green-bg); }}
.status-warn {{ border-color: #fde68a; color: var(--warn);  background: var(--warn-bg); }}
.status-err  {{ border-color: #fecaca; color: var(--red);   background: var(--red-bg); }}
.status-idle {{ border-color: var(--border); color: var(--muted); background: var(--white); }}

/* ─── FOOTER ─── */
.site-footer {{
  margin-top: 3.5rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.footer-name {{
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: 0.03em;
}}
.footer-legal {{
  font-family: 'Barlow', sans-serif;
  font-size: 0.65rem;
  color: var(--muted);
  letter-spacing: 0.02em;
}}

/* Spinner */
div[data-testid="stSpinner"] p {{
  font-family: 'Barlow', sans-serif !important;
  font-size: 0.8rem !important;
  color: var(--muted) !important;
}}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="site-header">
  <div class="header-logo">
    <img src="{LOGO_URL}" alt="Luluflix" />
  </div>
  <span class="header-badge">Watermark Tool</span>
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

def get_default_logo() -> str:
    """Télécharge le watermark par défaut et retourne son chemin local."""
    if "default_logo_path" not in st.session_state:
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "default_wm.png")
        urllib.request.urlretrieve(DEFAULT_WM_URL, path)
        st.session_state.default_logo_path = path
    return st.session_state.default_logo_path

# ── SESSION STATE ───────────────────────────────────────────────────────────────
for k in ["thumbnail", "rendered_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ── TABS ────────────────────────────────────────────────────────────────────────
tab_v, tab_p = st.tabs(["📹 Vidéo", "🖼 Photo"])

# ═══════════════════════════════ VIDÉO ════════════════════════════════════════
with tab_v:

    st.markdown('<div class="card"><div class="card-label">Fichier source</div>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposer la vidéo ici ou cliquer sur Parcourir",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">Logo PNG transparent <span style="font-weight:400;color:var(--muted);font-size:0.65rem;letter-spacing:0;text-transform:none;">(optionnel — logo Luluflix par défaut)</span></div>', unsafe_allow_html=True)
    logo_v = st.file_uploader(
        "Déposer un logo personnalisé ou laisser vide",
        type=["png"],
        key="vl"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if video_file:
        tmp = tempfile.mkdtemp()
        vp = os.path.join(tmp, "src" + os.path.splitext(video_file.name)[1])
        with open(vp, "wb") as f: f.write(video_file.read())

        # Logo : custom ou défaut
        if logo_v:
            lp = os.path.join(tmp, "logo.png")
            with open(lp, "wb") as f: f.write(logo_v.read())
        else:
            lp = get_default_logo()

        nfo = get_video_info(vp)
        dur_s = f"{int(nfo['duration']//60)}:{int(nfo['duration']%60):02d}"

        st.markdown(f"""
        <div class="specs-grid">
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
            <span class="ptag">Aperçu</span>
            <span class="preview-name">Première image avec logo incrusté</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶  Générer le rendu", key="vbtn",
                     disabled=bool(st.session_state.rendered_bytes)):
            out = os.path.join(tmp, "video_ready_to_post.mp4")
            ph_p, ph_s = st.empty(), st.empty()
            bar = ph_p.progress(0.0, text="")
            ph_s.markdown('<div class="status status-warn">⏳ Encodage en cours, veuillez patienter…</div>', unsafe_allow_html=True)
            try:
                render_video(vp, lp, out, nfo,
                             lambda p: bar.progress(p, text=f"Encodage : {int(p*100)} %"))
                bar.progress(1.0, text="Terminé : 100 %")
                ph_s.markdown('<div class="status status-ok">✓ Encodage terminé — fichier prêt.</div>', unsafe_allow_html=True)
                with open(out, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                ph_s.markdown(f'<div class="status status-err">✗ Erreur : {e}</div>', unsafe_allow_html=True)

        if st.session_state.rendered_bytes:
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

    st.markdown('<div class="card"><div class="card-label">Image source</div>', unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Déposer l'image ici ou cliquer sur Parcourir",
        type=["png", "jpg", "jpeg"],
        key="pu"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">Logo PNG transparent <span style="font-weight:400;color:var(--muted);font-size:0.65rem;letter-spacing:0;text-transform:none;">(optionnel — logo Luluflix par défaut)</span></div>', unsafe_allow_html=True)
    logo_p = st.file_uploader(
        "Déposer un logo personnalisé ou laisser vide",
        type=["png"],
        key="pl"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if photo_file:
        base = Image.open(photo_file)
        W, H = base.size
        tmp2 = tempfile.mkdtemp()

        # Logo : custom ou défaut
        if logo_p:
            lp2 = os.path.join(tmp2, "logo.png")
            with open(lp2, "wb") as f: f.write(logo_p.read())
        else:
            lp2 = get_default_logo()

        fmt = (base.format or photo_file.name.rsplit(".", 1)[-1]).upper()
        st.markdown(f"""
        <div class="specs-grid">
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
            <span class="ptag">Aperçu</span>
            <span class="preview-name">Image avec logo incrusté</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result_img.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result_img.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"

        st.markdown('<div class="status status-ok">✓ Traitement terminé — prêt à télécharger.</div>', unsafe_allow_html=True)
        st.download_button(
            "↓  Télécharger la photo",
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
  <span class="footer-legal">Aucune donnée n'est conservée sur un serveur</span>
</div>
""", unsafe_allow_html=True)
