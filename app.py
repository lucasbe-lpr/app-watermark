import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image
import io

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Luluflix",
    page_icon="🇫🇷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS : STYLE GOUVERNEMENT FRANÇAIS ────────────────────────────────────────
st.markdown("""
<style>
:root {
  --bleu:    #003189;
  --rouge:   #e1000f;
  --blanc:   #ffffff;
  --gris-bg: #f5f5f5;
  --gris-bd: #cccccc;
  --gris-txt:#6b6b6b;
  --noir:    #1a1a1a;
  --vert:    #008941;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--gris-bg) !important;
  color: var(--noir) !important;
  font-family: Arial, Helvetica, sans-serif !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── BANDEAU TRICOLORE EN HAUT ── */
.bandeau {
  height: 7px;
  background: linear-gradient(to right,
    var(--bleu) 33.3%,
    var(--blanc) 33.3%, var(--blanc) 66.6%,
    var(--rouge) 66.6%);
  margin-bottom: 0;
  border-bottom: 1px solid var(--gris-bd);
}

/* ── HEADER ── */
.header-block {
  background: var(--blanc);
  border-bottom: 2px solid var(--bleu);
  padding: 1rem 1.5rem 0.9rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.header-title {
  font-size: 1.55rem;
  font-weight: bold;
  color: var(--bleu);
  margin: 0;
  line-height: 1.1;
}
.header-sub {
  font-size: 0.68rem;
  color: var(--gris-txt);
  margin-top: 0.15rem;
  font-style: italic;
}

/* ── ONGLETS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--gris-bg) !important;
  border-bottom: 2px solid var(--bleu) !important;
  gap: 0 !important;
  padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: #e8e8e8 !important;
  border: 1px solid var(--gris-bd) !important;
  border-bottom: none !important;
  border-radius: 0 !important;
  color: var(--gris-txt) !important;
  font-size: 0.78rem !important;
  font-weight: bold !important;
  padding: 0.5rem 1.5rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  margin-right: 3px !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--blanc) !important;
  color: var(--bleu) !important;
  border-top: 3px solid var(--bleu) !important;
}

/* ── ENCADRÉS ── */
.encadre {
  background: var(--blanc);
  border: 1px solid var(--gris-bd);
  border-left: 4px solid var(--bleu);
  padding: 1rem 1.2rem;
  margin-bottom: 1rem;
}
.encadre-label {
  font-size: 0.65rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--bleu);
  margin-bottom: 0.6rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #e8e8e8;
}
.encadre-info {
  font-size: 0.78rem;
  color: var(--gris-txt);
  line-height: 2;
}
.encadre-info b { color: var(--noir); }

/* ── UPLOADER ── */
[data-testid="stFileUploader"] {
  background: var(--blanc) !important;
  border: 1px dashed var(--gris-bd) !important;
  border-radius: 0 !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--bleu) !important; }

/* ── BOUTON PRINCIPAL ── */
div.stButton > button {
  width: 100%;
  background: var(--bleu) !important;
  border: none !important;
  color: var(--blanc) !important;
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: bold !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  padding: 0.65rem 1rem !important;
  border-radius: 0 !important;
}
div.stButton > button:hover { background: #001f6b !important; }
div.stButton > button:disabled {
  background: var(--gris-bd) !important;
  color: var(--gris-txt) !important;
}

/* ── BOUTON TÉLÉCHARGER ── */
div[data-testid="stDownloadButton"] > button {
  width: 100%;
  background: var(--vert) !important;
  border: none !important;
  color: var(--blanc) !important;
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: bold !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  padding: 0.65rem 1rem !important;
  border-radius: 0 !important;
}
div[data-testid="stDownloadButton"] > button:hover { background: #006130 !important; }

/* ── MESSAGES ── */
.msg-ok   { background:#e8f5e9; border-left:4px solid var(--vert); padding:0.6rem 1rem; font-size:0.8rem; color:#1b5e20; margin:0.5rem 0; }
.msg-warn { background:#fff8e1; border-left:4px solid #f9a825;     padding:0.6rem 1rem; font-size:0.8rem; color:#5d4037; margin:0.5rem 0; }
.msg-err  { background:#ffebee; border-left:4px solid var(--rouge); padding:0.6rem 1rem; font-size:0.8rem; color:#b71c1c; margin:0.5rem 0; }

/* ── FOOTER ── */
.footer {
  border-top: 1px solid var(--gris-bd);
  margin-top: 2.5rem;
  padding-top: 0.8rem;
  font-size: 0.62rem;
  color: var(--gris-txt);
  text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bandeau"></div>
<div class="header-block">
  <div style="font-size:2.2rem;line-height:1">🇫🇷</div>
  <div>
    <p class="header-title">Luluflix</p>
    <p class="header-sub">Outil d'incrustation de logo — usage interne</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPER COMMUN : INCRUSTATION LOGO ────────────────────────────────────────

def composite_logo(base: Image.Image, logo_path: str) -> Image.Image:
    """Incruste le logo sur une image PIL selon les règles métier."""
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

# ─── HELPERS VIDÉO ────────────────────────────────────────────────────────────

def get_video_info(path: str) -> dict:
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
    frame_cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ]
    result = subprocess.run(frame_cmd, capture_output=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGBA")
    composited = composite_logo(frame, logo_path)
    return composited.convert("RGB")


def render_video(video_path: str, logo_path: str, output_path: str, info: dict, progress_cb=None):
    W, H = info["width"], info["height"]
    logo_w = int(W * 0.15)
    margin_x = int(W * 0.05)
    margin_y = int(H * 0.07)
    x = W - logo_w - margin_x
    y = margin_y
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
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "copy",
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
for key in ["thumbnail", "rendered_bytes"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─── ONGLETS ──────────────────────────────────────────────────────────────────
tab_video, tab_photo = st.tabs(["📹  Vidéo", "🖼️  Photo"])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET VIDÉO
# ══════════════════════════════════════════════════════════════════════════════
with tab_video:

    st.markdown('<div class="encadre"><div class="encadre-label">1 — Fichier source</div>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Vidéo source",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        label_visibility="collapsed",
        key="vid_upload"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="encadre"><div class="encadre-label">2 — Logo (PNG transparent)</div>', unsafe_allow_html=True)
    logo_file_v = st.file_uploader(
        "Logo PNG",
        type=["png"],
        label_visibility="collapsed",
        key="vid_logo"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if video_file and logo_file_v:
        tmp_dir = tempfile.mkdtemp()
        vid_path = os.path.join(tmp_dir, "source" + os.path.splitext(video_file.name)[1])
        logo_path_v = os.path.join(tmp_dir, "logo.png")

        with open(vid_path, "wb") as f:
            f.write(video_file.read())
        with open(logo_path_v, "wb") as f:
            f.write(logo_file_v.read())

        info = get_video_info(vid_path)
        dur_str = f"{int(info['duration']//60)}:{int(info['duration']%60):02d}"

        st.markdown(f"""
        <div class="encadre">
          <div class="encadre-label">Informations détectées</div>
          <div class="encadre-info">
            Résolution : <b>{info['width']} × {info['height']} px</b><br>
            Durée : <b>{dur_str}</b><br>
            Fréquence : <b>{info['fps']} fps</b><br>
            Largeur logo : <b>{int(info['width']*0.15)} px</b> (15 % de la largeur)
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Thumbnail
        st.markdown('<div class="encadre"><div class="encadre-label">Prévisualisation (1re image)</div>', unsafe_allow_html=True)
        if st.session_state.thumbnail is None:
            with st.spinner("Génération de la prévisualisation…"):
                st.session_state.thumbnail = make_thumbnail(vid_path, logo_path_v, info)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Générer le rendu final", key="render_btn",
                     disabled=(st.session_state.rendered_bytes is not None)):
            out_path = os.path.join(tmp_dir, "video_ready_to_post.mp4")
            prog_ph = st.empty()
            status_ph = st.empty()
            progress_bar = prog_ph.progress(0.0, text="")

            def update_progress(pct: float):
                progress_bar.progress(pct, text=f"Traitement… {int(pct*100)} %")

            try:
                status_ph.markdown('<div class="msg-warn">⏳ Traitement en cours, veuillez patienter…</div>', unsafe_allow_html=True)
                render_video(vid_path, logo_path_v, out_path, info, progress_cb=update_progress)
                progress_bar.progress(1.0, text="Terminé — 100 %")
                status_ph.markdown('<div class="msg-ok">✔ Rendu terminé. Vous pouvez télécharger votre fichier.</div>', unsafe_allow_html=True)
                with open(out_path, "rb") as f:
                    st.session_state.rendered_bytes = f.read()
            except Exception as e:
                status_ph.markdown(f'<div class="msg-err">✖ Erreur : {e}</div>', unsafe_allow_html=True)
                st.stop()

        if st.session_state.rendered_bytes:
            st.download_button(
                label="⬇ Télécharger video_ready_to_post.mp4",
                data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4",
                mime="video/mp4",
                key="dl_video"
            )
    else:
        st.markdown('<div class="msg-warn">Veuillez déposer une vidéo et un logo pour continuer.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET PHOTO
# ══════════════════════════════════════════════════════════════════════════════
with tab_photo:

    st.markdown('<div class="encadre"><div class="encadre-label">1 — Image source</div>', unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "Image source",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key="photo_upload"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="encadre"><div class="encadre-label">2 — Logo (PNG transparent)</div>', unsafe_allow_html=True)
    logo_file_p = st.file_uploader(
        "Logo PNG",
        type=["png"],
        label_visibility="collapsed",
        key="photo_logo"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if photo_file and logo_file_p:
        base_img = Image.open(photo_file)
        W, H = base_img.size

        tmp_dir_p = tempfile.mkdtemp()
        logo_path_p = os.path.join(tmp_dir_p, "logo.png")
        with open(logo_path_p, "wb") as f:
            f.write(logo_file_p.read())

        st.markdown(f"""
        <div class="encadre">
          <div class="encadre-label">Informations détectées</div>
          <div class="encadre-info">
            Résolution : <b>{W} × {H} px</b><br>
            Format : <b>{(base_img.format or photo_file.name.rsplit(".", 1)[-1]).upper()}</b><br>
            Largeur logo : <b>{int(W*0.15)} px</b> (15 % de la largeur)
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Prévisualisation instantanée
        result_img = composite_logo(base_img, logo_path_p)

        st.markdown('<div class="encadre"><div class="encadre-label">Prévisualisation</div>', unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Export
        out_buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        is_png = ext == "png"

        if is_png:
            result_img.save(out_buf, format="PNG", optimize=False)
            mime = "image/png"
            fname = "photo_ready_to_post.png"
        else:
            result_img.convert("RGB").save(out_buf, format="JPEG", quality=97, subsampling=0)
            mime = "image/jpeg"
            fname = "photo_ready_to_post.jpg"

        st.markdown('<div class="msg-ok">✔ Aperçu prêt. Cliquez sur Télécharger pour récupérer votre fichier.</div>', unsafe_allow_html=True)

        st.download_button(
            label=f"⬇ Télécharger {fname}",
            data=out_buf.getvalue(),
            file_name=fname,
            mime=mime,
            key="dl_photo"
        )
    else:
        st.markdown('<div class="msg-warn">Veuillez déposer une image et un logo pour continuer.</div>', unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Luluflix — Aucune donnée n'est conservée sur nos serveurs · Conforme RGPD
</div>
""", unsafe_allow_html=True)
