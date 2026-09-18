
import io, os, zipfile, urllib.request
from pathlib import Path
import streamlit as st
from PIL import Image, ImageFilter


st.set_page_config(page_title="UPSCALE BANG JEFF AI", page_icon="👑", layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 90% 4%,rgba(120,65,255,.28),transparent 25%),radial-gradient(circle at 3% 75%,rgba(0,190,255,.12),transparent 24%),linear-gradient(135deg,#030910,#071423 52%,#11103a);color:#fff}
.block-container{max-width:1540px;padding:28px 24px 35px}
header[data-testid="stHeader"]{background:transparent!important;border:0!important;box-shadow:none!important;color:inherit!important}
header[data-testid="stHeader"] button{color:#ffffff!important;background:transparent!important;opacity:1!important}
[data-testid="stSidebarCollapsedControl"],[data-testid="stSidebarCollapseButton"]{display:flex!important;visibility:visible!important;opacity:1!important}
[data-testid="stToolbar"]{display:none!important}
[data-testid="stDecoration"]{display:none!important}
footer{display:none!important}
#MainMenu{display:none!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#030914,#071322);border-right:1px solid #294867}
[data-testid="stSidebar"] *{color:#edf5ff}
.brand{font-size:34px;font-weight:1000;background:linear-gradient(90deg,#22ddff,#6870ff,#e44fff);-webkit-background-clip:text;color:transparent}
.bang{font-size:30px;font-weight:1000;font-style:italic;color:#fff;text-shadow:0 0 18px rgba(255,194,48,.35)}
.muted{font-size:10px;color:#8da1bb}
.hero{position:relative;z-index:5;font-size:44px;font-weight:1000;letter-spacing:-2px;line-height:1;background:linear-gradient(90deg,#fff,#59d2ff,#d568ff);-webkit-background-clip:text;color:transparent}
.top-status{display:flex;justify-content:flex-end;align-items:center;gap:9px;margin-bottom:2px;font-size:11px;font-weight:900;color:#b9c9df;letter-spacing:.3px}.status-pill{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border:1px solid rgba(71,213,255,.35);border-radius:999px;background:rgba(5,20,38,.72);box-shadow:0 0 18px rgba(46,184,255,.10)}.status-dot{width:9px;height:9px;border-radius:50%;background:#45f2ae;box-shadow:0 0 0 0 rgba(69,242,174,.7);animation:pulse 1.6s infinite}.status-dot.busy{background:#ff3d70;box-shadow:0 0 0 0 rgba(255,61,112,.7);animation:pulseBusy 1s infinite}.status-text{color:#eaf4ff}@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(69,242,174,.65)}70%{box-shadow:0 0 0 8px rgba(69,242,174,0)}100%{box-shadow:0 0 0 0 rgba(69,242,174,0)}}@keyframes pulseBusy{0%{box-shadow:0 0 0 0 rgba(255,61,112,.7)}70%{box-shadow:0 0 0 9px rgba(255,61,112,0)}100%{box-shadow:0 0 0 0 rgba(255,61,112,0)}}
.hero-quote{margin:10px 0 7px;font-size:18px;font-weight:800;font-style:italic;line-height:1.25;color:#ff66b3;text-shadow:0 0 14px rgba(255,55,150,.32)}.subtitle{font-size:17px;font-weight:700;color:#d8e5f4}
.ai-badge{display:inline-block;padding:5px 10px;border-radius:999px;background:linear-gradient(90deg,#ff1265,#7d4dff);color:#fff;font-size:11px;font-weight:1000;box-shadow:0 0 18px rgba(255,30,120,.22)}
.feature{font-size:13px;font-weight:950;color:#fff;text-align:center}
.quote{min-height:82px;padding:14px 17px;border-radius:15px;background:linear-gradient(135deg,#102945,#091727);border:1px solid #2c4d72}
.quote b{font-size:14px;color:#fff}.quote span{display:block;font-size:11px;color:#c7d5e5;margin-top:5px}
.panel{border:1px solid #2c4d72;border-radius:19px;background:linear-gradient(145deg,rgba(8,25,43,.98),rgba(5,15,27,.98));padding:18px}
.panel-title{font-size:19px;font-weight:1000;color:#fff}
[data-testid="stFileUploader"]{background:#071727!important;border:2px dashed #6687ae!important;border-radius:15px!important}
[data-testid="stFileUploader"] *{color:#fff!important}
.stRadio label,.stSelectbox label,.stSlider label{color:#fff!important;font-weight:900!important}
.stButton>button,.stDownloadButton>button{min-height:46px;border-radius:12px!important;font-weight:1000!important}
div.stButton>button[kind="primary"]{background:linear-gradient(90deg,#ff1265,#a536ff,#315cff)!important;color:#fff!important;border:0!important}
.stDownloadButton>button{background:linear-gradient(90deg,#06d58a,#08aaf4)!important;color:#fff!important;border:0!important}
.stat{border:1px solid #2b4c70;border-radius:15px;background:linear-gradient(145deg,#0b2037,#081523);padding:13px;text-align:center}
.stat .n{font-size:27px;font-weight:1000;color:#fff}.stat .l{font-size:10px;font-weight:800;color:#a9bdd4}
.imgcard{border:1px solid #2c4c6e;border-radius:15px;background:#081827;padding:9px}
.name{font-size:11px;font-weight:950;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.meta{font-size:10px;color:#b7c8dc}
.dim-in{background:linear-gradient(90deg,#0e487d,#1767a8);border-radius:9px;padding:8px;text-align:center;color:#fff;font-weight:950}
.dim-out{background:linear-gradient(90deg,#71118d,#c21cb8);border-radius:9px;padding:8px;text-align:center;color:#fff;font-weight:950}
.output-box{border:1px solid #14c79f;border-radius:17px;background:linear-gradient(135deg,#062d2c,#09263e);padding:18px}
.green{color:#45f2ae}
</style>
""", unsafe_allow_html=True)

# IMPORTANT: use clean internal page keys; emoji labels are only display text.
pages = {
    "Home":"🏠 Home",
    "Upscale":"✨ Upscale Image",
    "Output":"📦 Output & Download",
    "History":"🕘 History",
    "Settings":"⚙️ Settings",
    "About":"ℹ️ About"
}
labels=list(pages.values())
label_to_key={v:k for k,v in pages.items()}

for k,v in {"page":"Home","files":[],"results":[],"scale":2.5,"sharp":40,"fmt":"JPG","engine":"Smart Enhance"}.items():
    if k not in st.session_state: st.session_state[k]=v

FAST_MODEL_URL="https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x4.pb"
FAST_MODEL_PATH=Path(".cache")/"FSRCNN_x4.pb"

def up(im,scale,sharp):
    out=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    if sharp:
        out=out.filter(ImageFilter.UnsharpMask(radius=1.2,percent=70+int(sharp*1.4),threshold=2))
    return out

@st.cache_resource(show_spinner=False)
def load_fast_ai_model():
    """Download and cache the lightweight FSRCNN x4 model."""
    try:
        import cv2
        if not hasattr(cv2, "dnn_superres"):
            raise RuntimeError("OpenCV contrib is not installed")
        FAST_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not FAST_MODEL_PATH.exists() or FAST_MODEL_PATH.stat().st_size < 10_000:
            urllib.request.urlretrieve(FAST_MODEL_URL, FAST_MODEL_PATH)
        sr=cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(str(FAST_MODEL_PATH))
        sr.setModel("fsrcnn",4)
        return sr, None
    except Exception as e:
        return None, str(e)

def ai_fast_upscale(im, target_scale, sharp):
    """FSRCNN x4 AI super-resolution, resized down for 2x/2.5x targets."""
    import cv2, numpy as np
    sr, err = load_fast_ai_model()
    if sr is None:
        raise RuntimeError(f"AI Fast belum siap: {err}")
    rgb=np.array(im.convert("RGB"))
    bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
    tile=256
    h,w=bgr.shape[:2]
    out=np.zeros((h*4,w*4,3),dtype=np.uint8)
    for y in range(0,h,tile):
        for x in range(0,w,tile):
            patch=bgr[y:min(y+tile,h),x:min(x+tile,w)]
            ph,pw=patch.shape[:2]
            up_patch=sr.upsample(patch)
            out[y*4:y*4+ph*4,x*4:x*4+pw*4]=up_patch
    result=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB))
    if target_scale != 4:
        result=result.resize((round(im.width*target_scale),round(im.height*target_scale)),Image.Resampling.LANCZOS)
    if sharp:
        result=result.filter(ImageFilter.UnsharpMask(radius=1.05,percent=55+int(sharp*.9),threshold=2))
    return result

def encode(im,fmt):
    b=io.BytesIO()
    if fmt=="JPG":
        im.save(b,"JPEG",quality=95,optimize=True); return b.getvalue(),"jpg","image/jpeg"
    if fmt=="PNG":
        im.save(b,"PNG",optimize=True); return b.getvalue(),"png","image/png"
    im.save(b,"WEBP",quality=95); return b.getvalue(),"webp","image/webp"


def compare_html(orig, upscaled, height=390):
    import base64
    def b64(im):
        buf=io.BytesIO()
        im.save(buf, "JPEG", quality=94)
        return base64.b64encode(buf.getvalue()).decode("ascii")

    a = b64(orig)
    b = b64(upscaled)

    html = r"""
<html>
<head>
<style>
html,body{margin:0;padding:0;background:transparent;overflow:hidden;font-family:Arial,sans-serif}
.cmp{position:relative;width:100%;height:__HEIGHT__px;overflow:hidden;border-radius:14px;background:#050b13;user-select:none}
.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#050b13}
.after{clip-path:inset(0 50% 0 0)}
.tag{position:absolute;top:12px;padding:7px 10px;border-radius:8px;background:rgba(3,10,20,.88);color:#fff;font-size:12px;font-weight:900;z-index:4;border:1px solid rgba(255,255,255,.18)}
.beforetag{left:12px}.aftertag{right:12px}
.line{position:absolute;top:0;bottom:0;left:50%;width:3px;background:#fff;box-shadow:0 0 16px rgba(255,255,255,.8);z-index:6;transform:translateX(-50%);pointer-events:none}
.knob{position:absolute;top:50%;left:50%;width:46px;height:46px;border-radius:50%;background:#fff;color:#111;z-index:7;transform:translate(-50%,-50%);display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:1000;box-shadow:0 3px 18px rgba(0,0,0,.45);pointer-events:none}
input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;z-index:8;margin:0}
.hint{position:absolute;bottom:11px;left:50%;transform:translateX(-50%);z-index:7;color:#fff;background:rgba(0,0,0,.68);padding:6px 10px;border-radius:999px;font-size:11px;font-weight:800;white-space:nowrap}
</style>
</head>
<body>
<div class="cmp">
<img src="data:image/jpeg;base64,__ORIGINAL__">
<img class="after" id="after" src="data:image/jpeg;base64,__UPscaled__">
<div class="tag beforetag">ORIGINAL</div>
<div class="tag aftertag">UPSCALED</div>
<div class="line" id="line"></div>
<div class="knob" id="knob">↔</div>
<input id="range" type="range" min="0" max="100" value="50">
<div class="hint">GESER GARIS ← → UNTUK MEMBANDINGKAN DETAIL</div>
</div>
<script>
var r=document.getElementById("range");
var a=document.getElementById("after");
var l=document.getElementById("line");
var k=document.getElementById("knob");
function move(){
  var v=r.value;
  a.style.clipPath="inset(0 "+(100-v)+"% 0 0)";
  l.style.left=v+"%";
  k.style.left=v+"%";
}
r.addEventListener("input",move);
move();
</script>
</body>
</html>
"""
    return (html.replace("__HEIGHT__", str(height))
                .replace("__ORIGINAL__", a)
                .replace("__UPscaled__", b))

def make_zip():
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as z:
        for name,orig,out in st.session_state.results:
            data,ext,_=encode(out,st.session_state.fmt)
            z.writestr(f"{Path(name).stem}_{st.session_state.scale:g}x.{ext}",data)
    b.seek(0); return b.getvalue()

with st.sidebar:
    st.markdown('<div class="brand">👑 UPSCALE</div><div class="bang">BANG JEFF</div><div class="muted">AI IMAGE ENHANCER • LOCAL WORKFLOW</div>',unsafe_allow_html=True)
    st.divider()
    current_label=pages[st.session_state.page]
    selected_label=st.radio("Navigation",labels,index=labels.index(current_label),label_visibility="collapsed")
    st.session_state.page=label_to_key[selected_label]
    st.divider()
    st.markdown("🔥 **SIDE HUSTLE, BIG FREEDOM**")
    st.markdown("**Jadikan hobi kamu sumber rezeki.**")
    st.markdown("**Bukan sekadar memperbesar gambar, tapi memperbesar peluang.**")
    st.caption("— Bang Jeff 👑")
    st.divider()
    st.caption("V15 AI FAST • Made with Passion ❤️")
    st.caption("Online & Local • Batch image processing")

status_slot=st.empty()
status_slot.markdown('<div class="top-status"><div class="status-pill"><span class="status-dot"></span><span class="status-text">● READY • AI ENGINE ONLINE</span></div></div>',unsafe_allow_html=True)
st.markdown('<div class="hero">👑 UPSCALE BANG JEFF — SMALL IMAGE, BIGGER DREAMS.</div>',unsafe_allow_html=True)
st.markdown('<div class="hero-quote">“Dari gambar sekecil debu, kita besarkan menjadi peluang sebesar langit—karena mimpi besar pantas punya resolusi tanpa batas.”</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upscale Today. Create More. Earn More. Keep Growing. 🚀 &nbsp; <span class="ai-badge">SMART IMAGE ENHANCER</span></div>',unsafe_allow_html=True)
st.write("")
for c,t in zip(st.columns(5),["🔍 Higher Resolution","✨ Sharper Details","📚 Batch Processing","⬇️ One Click Download","🌍 Online & Local"]):
    c.markdown(f'<div class="feature">{t}</div>',unsafe_allow_html=True)
st.write("")
q=st.columns(3)
q[0].markdown('<div class="quote"><b>🔥 SIDE HUSTLE, BIG FREEDOM</b><span>Kerja kecil hari ini bisa menjadi peluang besar besok.</span></div>',unsafe_allow_html=True)
q[1].markdown('<div class="quote"><b>💎 CREATE MORE. EARN MORE.</b><span>Jangan biarkan resolusi membatasi kreativitasmu.</span></div>',unsafe_allow_html=True)
q[2].markdown('<div class="quote"><b>👑 BANG JEFF MODE: ON</b><span>Satu gambar lebih tajam. Satu peluang lebih besar.</span></div>',unsafe_allow_html=True)
st.write("")

page=st.session_state.page

if page in ("Home","Upscale"):
    L,R=st.columns([1.62,1])
    with L:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📤 Upload Your Images</div>',unsafe_allow_html=True)
        nf=st.file_uploader("Drag & Drop Your Images Here",type=["jpg","jpeg","png","webp"],accept_multiple_files=True)
        st.markdown('<div class="muted" style="text-align:center">Pilih banyak gambar sekaligus • JPG / PNG / WEBP • Proses semua dalam satu batch</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with R:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙️ Pengaturan Upscale</div>',unsafe_allow_html=True)
        engines=["Smart Enhance","AI Fast"]
        engine=st.radio("Engine",engines,index=engines.index(st.session_state.engine) if st.session_state.engine in engines else 0,horizontal=True)
        st.session_state.engine=engine
        if engine=="Smart Enhance":
            st.caption("⚡ Smart Enhance = Lanczos upscaling + intelligent sharpening • ringan & cepat")
        else:
            st.caption("🤖 AI Fast = FSRCNN super-resolution • lebih detail dengan model AI ringan")
        scale=st.radio("Faktor Upscale",[2,2.5,4],index=[2,2.5,4].index(st.session_state.scale),horizontal=True,format_func=lambda x:f"{x:g}×")
        sharp=st.slider("Detail / Sharpen",0,100,st.session_state.sharp)
        fmt=st.selectbox("Format Output",["JPG","PNG","WEBP"],index=["JPG","PNG","WEBP"].index(st.session_state.fmt))
        st.session_state.scale,st.session_state.sharp,st.session_state.fmt=scale,sharp,fmt
        st.markdown('<div class="muted">MODE: <b style="color:#45f2ae">ONLINE / LOCAL</b></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    if nf:
        if [x.name for x in nf] != [x.name for x in st.session_state.files]:
            st.session_state.results=[]
        st.session_state.files=nf

    files=st.session_state.files
    if files:
        st.write("")
        stats=[(len(files),"TOTAL GAMBAR","DIPILIH"),(len(st.session_state.results),"TELAH DIPROSES","SELESAI"),(f"{sum(x.size for x in files)/1024/1024:.1f} MB","TOTAL FILE SIZE","ORIGINAL"),("LOCAL","MODE","ONLINE / LOCAL")]
        for c,(n,l,s) in zip(st.columns(4),stats):
            c.markdown(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}<br>{s}</div></div>',unsafe_allow_html=True)

        if not st.session_state.results:
            st.write("")
            st.markdown(f"### 🖼️ Gambar Terpilih ({len(files)})")
            cols=st.columns(min(4,len(files)))
            for i,f in enumerate(files):
                with cols[i%len(cols)]:
                    im=Image.open(f).convert("RGB")
                    st.markdown('<div class="imgcard">',unsafe_allow_html=True)
                    st.image(im,use_container_width=True)
                    st.markdown(f'<div class="name">{f.name}</div><div class="meta">{im.width:,} × {im.height:,} px • {im.width*im.height/1e6:.2f} MP</div>',unsafe_allow_html=True)
                    st.markdown('</div>',unsafe_allow_html=True)
            st.write("")
            a,b=st.columns(2)
            if a.button("⚡ UPSCALE ALL",type="primary",use_container_width=True):
                res=[]; bar=st.progress(0,text="Memproses...")
                status_slot.markdown('<div class="top-status"><div class="status-pill"><span class="status-dot busy"></span><span class="status-text">⚡ PROCESSING • AI UPSCALE RUNNING</span></div></div>',unsafe_allow_html=True)
                try:
                    for i,f in enumerate(files):
                        im=Image.open(f).convert("RGB")
                        if engine=="AI Fast":
                            enhanced=ai_fast_upscale(im,scale,sharp)
                        else:
                            enhanced=up(im,scale,sharp)
                        res.append((f.name,im,enhanced))
                        bar.progress((i+1)/len(files),text=f"Upscale {i+1}/{len(files)} • {f.name}")
                except Exception as e:
                    st.error(f"AI Fast gagal diproses: {e}")
                    st.stop()
                st.session_state.results=res
                st.session_state.page="Output"
                st.rerun()
            if b.button("🗑️ CLEAR ALL",use_container_width=True):
                st.session_state.files=[];st.session_state.results=[];st.rerun()

if page=="Output":
    st.markdown("## 📦 Output & Download")
    if not st.session_state.results:
        st.info("Belum ada hasil. Masuk ke Upscale Image lalu tekan UPSCALE ALL.")
    else:
        results=st.session_state.results
        st.markdown(f'### <span class="green">✓ HASIL UPSCALE ({len(results)})</span>',unsafe_allow_html=True)
        st.success(f"{len(results)} gambar selesai • {st.session_state.engine} • {st.session_state.scale:g}× • {st.session_state.fmt} • Geser garis pada foto untuk melihat perbedaan detail.")
        st.markdown("### 🎚️ BEFORE / AFTER — DETAIL COMPARISON")
        st.caption("Geser garis putih pada foto. Kiri = original • Kanan = hasil upscale.")
        cols=st.columns(min(4,len(results)))
        for i,(name,orig,out) in enumerate(results):
            with cols[i%len(cols)]:
                st.markdown('<div class="imgcard">',unsafe_allow_html=True)
                st.markdown(f'<div class="name" style="font-size:13px;margin-bottom:7px">🔍 {name}</div>',unsafe_allow_html=True)
                st.components.v1.html(compare_html(orig,out,390),height=410,scrolling=False)
                x,y=st.columns(2)
                x.markdown(f'<div class="dim-in">ORIGINAL<br>{orig.width:,} × {orig.height:,}<br>{orig.width*orig.height/1e6:.2f} MP</div>',unsafe_allow_html=True)
                y.markdown(f'<div class="dim-out">UPSCALED {st.session_state.scale:g}×<br>{out.width:,} × {out.height:,}<br>{out.width*out.height/1e6:.2f} MP</div>',unsafe_allow_html=True)
                data,ext,mime=encode(out,st.session_state.fmt)
                st.download_button("⬇️ DOWNLOAD",data,file_name=f"{Path(name).stem}_{st.session_state.scale:g}x.{ext}",mime=mime,key=f"single_{i}",use_container_width=True)
                st.markdown('</div>',unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="output-box">',unsafe_allow_html=True)
        st.markdown("### 📦 DOWNLOAD HASIL")
        d1,d2,d3=st.columns([1.5,1.25,.8])
        d1.download_button("⬇️ DOWNLOAD ALL HASIL (ZIP)",make_zip(),file_name=f"Upscale_Bang_Jeff_{st.session_state.scale:g}x.zip",mime="application/zip",use_container_width=True)
        if d2.button("💾 SAVE OUTPUT LOCALLY",use_container_width=True):
            outdir=Path.home()/"Pictures"/"Upscale_By_BangJeff";outdir.mkdir(parents=True,exist_ok=True)
            for name,orig,out in results:
                data,ext,_=encode(out,st.session_state.fmt)
                (outdir/(Path(name).stem+f"_{st.session_state.scale:g}x.{ext}")).write_bytes(data)
            st.success(f"Tersimpan di {outdir}")
        if d3.button("🗑️ CLEAR HASIL",use_container_width=True):
            st.session_state.results=[];st.session_state.page="Upscale";st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

if page=="History":
    st.markdown("## 🕘 History")
    st.info(f"Batch terakhir: {len(st.session_state.results)} gambar." if st.session_state.results else "Belum ada hasil.")

if page=="Settings":
    st.markdown("## ⚙️ Settings")
    st.info("Pengaturan utama ada di panel Pengaturan Upscale. Aplikasi dapat berjalan lokal atau melalui cloud.")

if page=="About":
    st.markdown("## ℹ️ About")
    st.markdown("### 👑 UPSCALE BANG JEFF V15 AI FAST")
    st.write("Upload → Smart Enhance → Compare → Download. Batch workflow untuk gambar, tersedia lokal maupun online.")

st.markdown('<div style="text-align:center;color:#71859f;font-size:10px;padding:20px">UPSCALE BANG JEFF 👑 • CREATE MORE • EARN MORE • KEEP GROWING</div>',unsafe_allow_html=True)
