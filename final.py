# ai_material_selector.py
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from reportlab.pdfgen import canvas

# ====== Dataset ======
data = pd.DataFrame({
    "Material": ["Steel", "Aluminum", "Titanium", "Carbon Fiber", "Plastic",
                 "Copper", "Brass", "Magnesium", "Glass Fiber", "Nylon"],
    "Strength": [500, 300, 900, 700, 50, 220, 300, 150, 600, 80],   # MPa
    "Density": [7.8, 2.7, 4.5, 1.6, 1.2, 8.9, 8.4, 1.7, 2.5, 1.1], # g/cm³
    "Cost": [2, 3, 10, 15, 1, 6, 5, 4, 7, 2],                      # $/kg
    "CorrosionResistance": [3, 6, 7, 9, 5, 4, 5, 6, 7, 6]           # 1–10 scale
})

features = ["Strength", "Density", "Cost", "CorrosionResistance"]

X = data[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = NearestNeighbors(n_neighbors=3)
model.fit(X_scaled)

# ====== Streamlit UI ======
st.set_page_config(page_title="AI Material Selector", layout="wide")
st.title("🤖 AI-Powered Material Selector")
st.write("Input your design requirements and get the best material suggestions.")

# User inputs
strength = st.slider("Required Strength (MPa)", 50, 1000, 300)
density = st.slider("Desired Density (g/cm³)", 1, 9, 3)
cost = st.slider("Max Cost ($/kg)", 1, 20, 5)
corrosion = st.slider("Corrosion Resistance (1=Low, 10=High)", 1, 10, 5)

# Predict materials
user_input = scaler.transform([[strength, density, cost, corrosion]])
distances, indices = model.kneighbors(user_input)

st.subheader("🔎 Recommended Materials")
recommended = []
for idx in indices[0]:
    row = data.iloc[idx]
    recommended.append(row)
    st.markdown(
        f"✅ **{row['Material']}** — "
        f"Strength: {row['Strength']} MPa, "
        f"Density: {row['Density']} g/cm³, "
        f"Cost: ${row['Cost']}/kg, "
        f"Corrosion Resistance: {row['CorrosionResistance']}"
    )

# ====== 3D Plot (Ashby Chart style) ======
fig = px.scatter_3d(
    data, x="Strength", y="Density", z="Cost",
    color="Material", size="CorrosionResistance",
    title="Ashby Chart: Strength vs Density vs Cost"
)
st.plotly_chart(fig, use_container_width=True)

# ====== PDF Export ======
def generate_pdf(recs):
    c = canvas.Canvas("material_report.pdf")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "AI Material Selector Report")
    c.setFont("Helvetica", 12)
    y = 760
    for _, r in enumerate(recs):
        c.drawString(
            50, y,
            f"Material: {r['Material']}, Strength: {r['Strength']} MPa, "
            f"Density: {r['Density']} g/cm³, Cost: ${r['Cost']}/kg, "
            f"Corrosion Resistance: {r['CorrosionResistance']}"
        )
        y -= 20
    c.save()

if st.button("📄 Download Report"):
    generate_pdf(recommended)
    st.success("Report generated as material_report.pdf (check your folder).")
