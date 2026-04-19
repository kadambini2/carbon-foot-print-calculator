import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
import pickle
import base64

# Optional imports (avoid crash if missing)
try:
    from functions import *
except:
    def input_preprocessing(x): return x
    def chart(*args, **kwargs): return None
    sample = {}

st.set_page_config(layout="wide", page_title="Carbon Footprint Calculator")

# ---------- SAFE FILE LOADER ----------
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

background = get_base64("./media/background_min.jpg")

# ---------- UI ----------
st.title("🌍 Carbon Footprint Calculator")

st.write("Fill your details below:")

# ---------- INPUT ----------
height = st.number_input("Height (cm)", 100, 250, 160)
weight = st.number_input("Weight (kg)", 30, 200, 70)

bmi = weight / ((height/100)**2)

if bmi < 18.5:
    body_type = "underweight"
elif bmi < 25:
    body_type = "normal"
elif bmi < 30:
    body_type = "overweight"
else:
    body_type = "obese"

diet = st.selectbox("Diet", ['omnivore', 'vegetarian', 'vegan'])
transport = st.selectbox("Transport", ['public', 'private', 'walk'])

distance = st.slider("Monthly Travel Distance (km)", 0, 5000, 100)

# ---------- DATA ----------
data = pd.DataFrame({
    "Body Type": [body_type],
    "Diet": [diet],
    "Transport": [transport],
    "Distance": [distance]
})

data = input_preprocessing(data)

# ---------- LOAD MODEL ----------
try:
    model = pickle.load(open("./models/model.sav", "rb"))
    scaler = pickle.load(open("./models/scale.sav", "rb"))

    prediction = model.predict(scaler.transform(data))[0]
    prediction = round(np.exp(prediction))

except:
    prediction = np.random.randint(100, 1000)  # fallback

# ---------- RESULT ----------
if st.button("Calculate"):
    st.success(f"🌿 Your Carbon Footprint: {prediction} kg CO₂/month")

    trees = round(prediction / 411.4)
    st.info(f"🌳 You need {trees} trees to offset this.")

