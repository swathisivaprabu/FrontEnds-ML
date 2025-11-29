import streamlit as st
from PIL import Image
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
# INSECT DATA
# -------------------------------------------------------------------
INSECT_MAP = {
    "Mosquitoes": [
        "Aedes aegypti",
        "Culex pipiens",
        "Culex pipiens pallens",
        "Anopheles gambiae"
    ],
    "Sandflies": ["Phlebotomus", "Lutzomyia"],
    "Black flies": ["Simulium damnosum complex", "Simulium posticatum"],
    "Biting midges": ["Culicoides", "Leptoconops", "Forcipomyia taiwana"],
    "Horse flies / Deer flies": ["Tabanus", "Chrysops", "Haematopota", "Rhagionidae"],
    "Eye flies / Frit flies": ["Chloropidae"],
    "House flies / Stable flies / Testse flies": ["Glossina"],
    "Louse flies": ["Lipoptera cervi"],
    "Blow flies": ["Calliphoridae"],
    "Flesh flies": ["Sarcophagidae"],
    "Bot flies": ["Oestridae"],
    "Fleas": ["Pulex irritans", "Ctenocephalides canis", "Ctenocephalides felis", "Xenopsylla cheopis", "Ceratophyllidae"],
    "Bees, Wasps, Ants": ["Hymenoptera"],
    "Lice": ["Pediculus humanus capitis", "Pediculus humanus humanus", "Pthirus pubis"],
    "Bugs": ["Cimex lectularius", "Cimex pipistrelli", "Cimex hemipterus", "Leptocimex", "Oeciacus", "Haematosiphon", "Triatoma sanguisuga", "Reduviidae", "Palomena prasina"],
    "Thrips": ["Thrips"],
    "Beetles": ["Beetle"],
    "Cockroaches": ["Indian Cockroach"],
    "Locusts": ["Locust"],
    "Butterflies and Moths": ["Lepidoptera"]
}

# -------------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------------
st.set_page_config(page_title="FARM SAFE BITE CLASSIFIER", layout="wide")

# -------------------------------------------------------------------
# TITLE
# -------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; border: 2px solid black; padding: 10px; border-radius: 10px;'>FARM SAFE BITE CLASSIFIER</h1>", unsafe_allow_html=True)
st.write("") # Spacer

# -------------------------------------------------------------------
# LAYOUT: 3 COLUMNS
# -------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1])

# -------------------------------------------------------------------
# LEFT COLUMN
# -------------------------------------------------------------------
with col1:
    st.markdown("### farmer friendly GUI")
    
    # Upload Image Section
    st.markdown("<div style='border: 1px solid black; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("upload image", type=['jpg', 'png', 'jpeg'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Audio/Video Input Section
    st.markdown("#### Audio/Video input from Farmer")
    with st.container(border=True):
        st.text_input("Text input")
        st.button("Audio button")

# -------------------------------------------------------------------
# MIDDLE COLUMN
# -------------------------------------------------------------------
with col2:
    # Dropdowns
    insect_category = st.selectbox("Dropdown for Insect Category", list(INSECT_MAP.keys()))
    
    # Sub-category based on selection
    species = st.selectbox("Select Species", INSECT_MAP[insect_category])
    
    rash_category = st.selectbox("Dropdown for Rash Category", ["Rash Type 1", "Rash Type 2", "Rash Type 3"])
    
    st.write("") # Spacer
    
    # Result Area
    st.text_area("Result via AI Explanation", height=100)
    
    st.write("") # Spacer
    
    # Doctor Observation & Medication
    col2_a, col2_b = st.columns(2)
    with col2_a:
        st.text_area("Insect bite Doctor Observation", height=100)
    with col2_b:
        st.text_area("Doctor medication", height=100)

# -------------------------------------------------------------------
# RIGHT COLUMN
# -------------------------------------------------------------------
with col3:
    st.write("Insect Image")
    
    # Fetch image based on selected species
    img_url = fetch_insect_image(species)
    
    if img_url:
        st.image(img_url, use_container_width=True)
    else:
        st.markdown("<div style='border: 2px solid black; height: 150px; border-radius: 10px; display: flex; align-items: center; justify-content: center;'>Image Not Found</div>", unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    st.write("Rash image")
    st.markdown("<div style='border: 2px solid black; height: 150px; border-radius: 10px; display: flex; align-items: center; justify-content: center;'>Image Placeholder</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; border: 1px solid black; padding: 5px; border-radius: 10px;'>Design to identify insect byte</h3>", unsafe_allow_html=True)
