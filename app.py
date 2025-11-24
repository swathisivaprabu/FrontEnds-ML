import streamlit as st
from PIL import Image
import base64
import os
import requests

# -------------------------------------------------------------------
# FETCH IMAGE FROM iNaturalist
# -------------------------------------------------------------------
def fetch_insect_image(insect_name):
    url = f"https://api.inaturalist.org/v1/taxa?q={insect_name}"

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None

        data = r.json()
        if len(data.get("results", [])) == 0:
            return None

        taxon = data["results"][0]

        if "default_photo" not in taxon:
            return None

        return taxon["default_photo"].get("medium_url") or \
               taxon["default_photo"].get("square_url") or \
               taxon["default_photo"].get("url")

    except:
        return None


# -------------------------------------------------------------------
# BACKGROUND CSS
# -------------------------------------------------------------------
st.markdown("""
<style>
/* ---------- Reset Streamlit's default width constraints ---------- */
.main .block-container {
    max-width: 100% !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Force full width for all sections */
section.main > div {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Fix the app background and overlay */
.stApp {
    background: url("bf.jpg") center center / cover no-repeat fixed !important;
    min-height: 100vh;
}

/* Create the dark overlay */
.app-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.45);
    pointer-events: none;
    z-index: -1;
}

/* Ensure content stays above overlay */
.stApp > header, .stApp > div, .stApp > main {
    position: relative;
    z-index: 1;
}

/* ---------- Text colors ---------- */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] label,
.stMarkdown, .stMarkdown p {
    color: #fff !important;
}

/* ---------- Widget styling ---------- */
/* Select box */
div[data-baseweb="select"] > div {
    background-color: rgba(0,0,0,0.55) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    color: #fff !important;
}
[data-testid="stFileUploader"] .upload {
    background: rgba(255,255,255,0.05) !important;
    border: 1px dashed rgba(255,255,255,0.2) !important;
}

/* Input fields */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: rgba(0,0,0,0.45) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Radio and checkbox */
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
    color: #fff !important;
}

/* Make columns use full available width */
.stColumns {
    width: 100% !important;
}

/* Column children should expand */
.stColumns > div {
    flex: 1 !important;
    min-width: 0 !important; /* Prevent overflow */
}

/* Make images responsive */
.stImage img {
    max-width: 100% !important;
    height: auto !important;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Button styling */
.stButton button {
    background: rgba(0,0,0,0.6) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    width: 100%;
}

/* Success/error messages */
.stSuccess, .stError {
    background: rgba(0,0,0,0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ---------- Mobile responsiveness ---------- */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .stColumns {
        flex-direction: column !important;
    }
    
    .stColumns > div {
        margin-bottom: 1rem;
    }
}
</style>

<!-- Overlay element -->
<div class="app-overlay"></div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------
# MAIN CATEGORY → SUB CATEGORY LIST
# -------------------------------------------------------------------
INSECT_MAP = {
    "Mosquitoes": [
        "Aedes aegypti",
        "Culex pipiens",
        "Culex pipiens pallens",
        "Anopheles gambiae"
    ],

    "Sandflies": [
        "Phlebotomus",
        "Lutzomyia"
    ],

    "Black flies": [
        "Simulium damnosum complex",
        "Simulium posticatum"
    ],

    "Biting midges": [
        "Culicoides",
        "Leptoconops",
        "Forcipomyia taiwana"
    ],

    "Horse flies / Deer flies": [
        "Tabanus",
        "Chrysops",
        "Haematopota",
        "Rhagionidae"
    ],

    "Eye flies / Frit flies": ["Chloropidae"],

    "House flies / Stable flies / Testse flies": ["Glossina"],

    "Louse flies": ["Lipoptera cervi"],

    "Blow flies": ["Calliphoridae"],

    "Flesh flies": ["Sarcophagidae"],

    "Bot flies": ["Oestridae"],

    "Fleas": [
        "Pulex irritans",
        "Ctenocephalides canis",
        "Ctenocephalides felis",
        "Xenopsylla cheopis",
        "Ceratophyllidae"
    ],

    "Bees, Wasps, Ants": ["Hymenoptera"],

    "Lice": [
        "Pediculus humanus capitis",
        "Pediculus humanus humanus",
        "Pthirus pubis"
    ],

    "Bugs": [
        "Cimex lectularius",
        "Cimex pipistrelli",
        "Cimex hemipterus",
        "Leptocimex",
        "Oeciacus",
        "Haematosiphon",
        "Triatoma sanguisuga",
        "Reduviidae",
        "Palomena prasina"
    ],

    "Thrips": ["Thrips"],

    "Beetles": ["Beetle"],

    "Cockroaches": ["Indian Cockroach"],

    "Locusts": ["Locust"],

    "Butterflies and Moths": ["Lepidoptera"]
}

# -------------------------------------------------------------------
# UI TITLE
# -------------------------------------------------------------------
st.markdown("<h2>Insect Detection</h2><hr>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# LAYOUT: 3 COLUMNS
# -------------------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])

# -------------------------------------------------------------------
# COLUMN 1 → CATEGORY + SUBCATEGORY DROPDOWN
# -------------------------------------------------------------------
with col1:
    st.subheader("1) Select Insect Category")

    category = st.selectbox("Choose category", list(INSECT_MAP.keys()))

    st.subheader("Select Species")

    species = st.selectbox("Choose species", INSECT_MAP[category])


# -------------------------------------------------------------------
# COLUMN 2 → SHOW REFERENCE IMAGE
# -------------------------------------------------------------------
with col2:
    st.subheader("2) Reference Image")

    img_url = fetch_insect_image(species)

    if img_url:
        st.image(img_url, use_container_width=True)
    else:
        st.error("No image found")


# -------------------------------------------------------------------
# COLUMN 3 → USER UPLOAD
# -------------------------------------------------------------------
with col3:
    st.subheader("3) Upload Your Image")

    uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

    if uploaded:
        user_img = Image.open(uploaded)
        st.image(user_img, use_container_width=True)
        st.success("Uploaded successfully")