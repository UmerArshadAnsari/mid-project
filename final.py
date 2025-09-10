# material_selector.py
import pandas as pd
import streamlit as st
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# ====== Load dataset ======
data = pd.DataFrame({
    "Material": ["Steel", "Aluminum", "Titanium", "Carbon Fiber", "Plastic"],
    "Strength": [500, 300, 900, 700, 50],      # MPa
    "Density": [7.8, 2.7, 4.5, 1.6, 1.2],      # g/cm^3
    "Cost": [2, 3, 10, 15, 1],                 # $/kg
    "CorrosionResistance": [3, 6, 7, 9, 5]     # 1-10 scale
})

features = ["Strength", "Density", "Cost", "CorrosionResistance"]

X = data[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = NearestNeighbors(n_neighbors=2)
model.fit(X_scaled)

# ====== Streamlit UI ======
st.title(" AI-Powered Material Selector")
st.write("Input your design requirements and get the best material suggestion.")

# User inputs
strength = st.slider("Required Strength (MPa)", 50, 1000, 300)
density = st.slider("Desired Density (g/cm³)", 1, 8, 3)
cost = st.slider("Max Cost ($/kg)", 1, 20, 5)
corrosion = st.slider("Corrosion Resistance (1=Low, 10=High)", 1, 10, 5)

# Convert input to vector
user_input = scaler.transform([[strength, density, cost, corrosion]])

# Predict nearest materials
distances, indices = model.kneighbors(user_input)

st.subheader("🔎 Recommended Materials:")
for idx in indices[0]:
    row = data.iloc[idx]
    st.write(f"**{row['Material']}** → Strength: {row['Strength']} MPa, Density: {row['Density']} g/cm³, Cost: {row['Cost']} $/kg, Corrosion Resistance: {row['CorrosionResistance']}")

