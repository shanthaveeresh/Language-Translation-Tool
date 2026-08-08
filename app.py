import html
import requests
import streamlit as st

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="wide")

MYMEMORY_URL = "https://api.mymemory.translated.net/get"
LANGUAGES = {
    "Detect language": "auto", "English": "en", "Hindi": "hi", "Kannada": "kn",
    "Telugu": "te", "Tamil": "ta", "Malayalam": "ml", "Marathi": "mr",
    "Bengali": "bn", "Gujarati": "gu", "Spanish": "es", "French": "fr",
    "German": "de", "Italian": "it", "Portuguese": "pt", "Japanese": "ja",
    "Korean": "ko", "Chinese": "zh", "Arabic": "ar", "Russian": "ru",
}

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg,#f4f7fb,#eef3ff); }
.block-container { max-width:1100px; padding-top:2.5rem; }
.hero { background:rgba(255,255,255,.96); border:1px solid #e5eaf2;
border-radius:22px; padding:28px; margin-bottom:20px;
box-shadow:0 15px 45px rgba(32,50,80,.08); }
.eyebrow { font-size:.75rem; font-weight:800; letter-spacing:1.5px; color:#53627b; }
.hero h1 { margin:0; color:#172033; }
.subtitle { color:#65738b; }
.result-box { background:white; border:1px solid #dfe5ef; border-radius:14px;
padding:18px; min-height:190px; color:#29364d; font-size:1rem;
line-height:1.65; white-space:pre-wrap; overflow-wrap:anywhere; }
.info { text-align:center; color:#6c7890; font-size:.85rem; margin-top:1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<div class="eyebrow">TASK 1</div>
<h1>🌐 Language Translation Tool</h1>
<div class="subtitle">Python + Streamlit + Translation API</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    source_name = st.selectbox("Source language", list(LANGUAGES.keys()))
with c2:
    targets = [x for x in LANGUAGES if x != "Detect language"]
    target_name = st.selectbox("Target language", targets, index=0)

source = LANGUAGES[source_name]
target = LANGUAGES[target_name]

text = st.text_area("Enter text", placeholder="Type or paste your text here...", height=220, max_chars=5000)
st.caption(f"{len(text)} / 5000 characters")

b1, b2 = st.columns([5, 1])
with b1:
    translate_clicked = st.button("🌐 Translate", type="primary", use_container_width=True)
with b2:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    for key in ("translation", "provider"):
        st.session_state.pop(key, None)
    st.rerun()

if translate_clicked:
    if not text.strip():
        st.warning("Please enter some text first.")
    elif source == target:
        st.session_state["translation"] = text.strip()
        st.session_state["provider"] = "Same language"
    else:
        api_source = "en" if source == "auto" else source
        try:
            with st.spinner("Translating..."):
                r = requests.get(
                    MYMEMORY_URL,
                    params={"q": text.strip(), "langpair": f"{api_source}|{target}"},
                    timeout=20,
                )
                r.raise_for_status()
                data = r.json()
            translated = data.get("responseData", {}).get("translatedText", "").strip()
            if not translated:
                st.error("The translation API did not return a translation.")
            else:
                st.session_state["translation"] = translated
                st.session_state["provider"] = "MyMemory"
        except requests.RequestException:
            st.error("Could not connect to the translation API. Please try again.")
        except Exception:
            st.error("Something went wrong while translating.")

translation = st.session_state.get("translation", "Your translation will appear here.")
provider = st.session_state.get("provider", "Ready")

st.subheader("Translated text")
st.markdown(f'<div class="result-box">{html.escape(translation)}</div>', unsafe_allow_html=True)
st.caption(f"Provider: {provider}")

st.subheader("Copy")
st.code(translation, language=None)

st.markdown('<div class="info">Built with Python • Streamlit • MyMemory Translation API</div>', unsafe_allow_html=True)