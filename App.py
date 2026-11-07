python
import streamlit as st

def generate_fertilizer_prescription(crop, current_pH, current_N, current_P, current_K):
    crop_database = {
        "cabbages": {"min_pH": 6.0, "max_pH": 6.8, "target_N": 50, "target_P": 30, "target_K": 200, "notes": "Monitor closely for Clubroot if pH drops below 6.0."},
        "tomatoes": {"min_pH": 6.0, "max_pH": 6.8, "target_N": 45, "target_P": 25, "target_K": 180, "notes": "Ensure steady moisture to prevent Blossom End Rot."},
        "maize": {"min_pH": 5.5, "max_pH": 6.5, "target_N": 40, "target_P": 20, "target_K": 150, "notes": "Ensure zinc availability during early growth stages."}, 
        "coffee": {"min_pH": 5.0, "max_pH": 5.6, "target_N": 60, "target_P": 15, "target_K": 250, "notes": "Apply boron post-harvest to support cherry development."}
    }
    crop_key = crop.lower().strip()
    if crop_key not in crop_database:
        return "Crop data not available."
    targets = crop_database[crop_key]
    prescription = {"Crop": crop.capitalize(), "Soil_Amendments": [], "Eco_Fertilizer_Blend": {}, "Advisory": targets["notes"], "targets": targets}
    if current_pH < targets["min_pH"]:
        prescription["Soil_Amendments"].append("Apply Agricultural Lime (CaCO3) to neutralize soil acidity and unlock nutrient availability.")
    elif current_pH > targets["max_pH"]:
        prescription["Soil_Amendments"].append("Apply Agricultural Sulfur to safely lower soil pH to optimal ranges.")
    else:
        prescription["Soil_Amendments"].append("Soil pH is optimal. No structural chemical amendments needed.")
    deficit_N = max(0, targets["target_N"] - current_N)
    deficit_P = max(0, targets["target_P"] - current_P)
    deficit_K = max(0, targets["target_K"] - current_K)
    if deficit_N > 0:
        prescription["Eco_Fertilizer_Blend"]["Nitrogen (N) Source"] = f"Apply Neem Cake or Neem-coated Slow-Release Urea to supply {deficit_N} ppm N without rapid leaching."
    if deficit_P > 0:
        prescription["Eco_Fertilizer_Blend"]["Phosphorus (P) Source"] = f"Apply Bio-fertilizer (Phosphorus Solubilizing Bacteria) paired with Rock Phosphate to supply {deficit_P} ppm P safely."
    if deficit_K > 0:
        prescription["Eco_Fertilizer_Blend"]["Potassium (K) Source"] = f"Apply Organic Compost enriched with Cocoa Pod Ash or Muriate of Potash to supply {deficit_K} ppm K."
    if not prescription["Eco_Fertilizer_Blend"]:
        prescription["Eco_Fertilizer_Blend"]["Status"] = "Nutrient reserves are fully satisfied. Apply organic mulch only to maintain soil structure."
    return prescription

st.set_page_config(page_title="Eco-Gro AI", page_icon="🌱", layout="centered")
st.title("🌱 Eco-Gro: Precision Fertilizer Platform")
st.markdown("### *MUT Innovation Week 2026 Project Showcase*")
st.write("This digital system converts lab-tested chemical soil metrics into green, localized fertilizer applications.")

st.sidebar.header("📍 Farm Soil Inputs")
selected_crop = st.sidebar.selectbox("Select Target Crop", ["Cabbages", "Tomatoes", "Maize", "Coffee"])
input_pH = st.sidebar.slider("Measured Soil pH", 4.0, 9.0, 6.0, step=0.1)
input_N = st.sidebar.slider("Measured Nitrogen (N in ppm)", 0, 100, 30)
input_P = st.sidebar.slider("Measured Phosphorus (P in ppm)", 0, 100, 20)
input_K = st.sidebar.slider("Measured Potassium (K in ppm)", 0, 300, 150)

if st.sidebar.button("Run Diagnostic Engine"):
    result = generate_fertilizer_prescription(selected_crop, input_pH, input_N, input_P, input_K)
    st.success(f"### 📋 Diagnostic Results for {result['Crop']}")
    st.warning(f"💡 **Agronomic Advisory:** {result['Advisory']}")
    st.write("#### 📊 Nutrient Analysis: Current vs. Target (ppm)")
    chart_data = {
        "Nutrient": ["Nitrogen (N)", "Nitrogen (N)", "Phosphorus (P)", "Phosphorus (P)", "Potassium (K)", "Potassium (K)"],
        "Status": ["Current Level", "Target Goal", "Current Level", "Target Goal", "Current Level", "Target Goal"],
        "Value (ppm)": [input_N, result["targets"]["target_N"], input_P, result["targets"]["target_P"], input_K, result["targets"]["target_K"]]
    }
    st.bar_chart(data=chart_data, x="Nutrient", y="Value (ppm)", color="Status", stack=False)
    st.write("#### 🏗️ Required Structural Amendments")
    for amendment in result['Soil_Amendments']:
        st.info(amendment)
    st.write("#### 🌿 Customized Eco-Friendly Nutrition Blend")
    for nutrient, recommendation in result['Eco_Fertilizer_Blend'].items():
        st.write(f"- **{nutrient}:** {recommendation}")