# ==============================
# Imports
# ==============================
import streamlit as st
from fpdf import FPDF
from ai_diet_generator import generate_diet
import re

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f1e1c, #192924);
    color: #e0ffe0;
    font-family: 'Segoe UI', sans-serif;
}
.stApp h1 {
    color: #00ff7f;
    text-align: center;
    font-size: 42px;
}
div.stButton > button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 12px;
    border: none;
}
.stTextInput input {
    border-radius: 12px;
    padding: 10px;
    border: 2px solid #10b981;
    background-color: #0f1e1c;
    color: #e0ffe0;
}
.diet-card {
    background-color: #1f3d28;
    color: #e0ffe0;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    font-size: 16px;
    line-height: 1.6;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# Remove emojis for PDF
# ==============================
def remove_emojis(text):
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# ==============================
# PDF Generator
# ==============================
def create_pdf(patient_id, diet_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Diet Plan", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)

    clean_text = remove_emojis(diet_text)
    for line in clean_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_name = f"diet_plan_{patient_id}.pdf"
    pdf.output(file_name)
    return file_name

# ==============================
# Title
# ==============================
st.title("🥗 AI Diet Planner 🍎")
st.image(
    "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    use_container_width=True

)

# ==============================
# Layout
# ==============================
col1, col2 = st.columns([2, 1])

with col1:
    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. 101")

    if st.button("Generate Diet Plan"):
        if patient_id.isdigit():

            with st.spinner("Generating diet plan..."):
                diet_text = generate_diet(patient_id)

            if diet_text:
                st.success("✅ Diet Generated Successfully!")

                meals = {
                    "Breakfast 🥣": "",
                    "Lunch 🥗": "",
                    "Snacks 🍎": "",
                    "Dinner 🍛": ""
                }

                current_meal = None

                for raw_line in diet_text.split("\n"):
                    line = raw_line.strip()
                    lower = line.lower()

                    if lower.startswith("breakfast"):
                        current_meal = "Breakfast 🥣"
                        continue
                    if lower.startswith("lunch"):
                        current_meal = "Lunch 🥗"
                        continue
                    if lower.startswith("snack"):
                        current_meal = "Snacks 🍎"
                        continue
                    if lower.startswith("dinner"):
                        current_meal = "Dinner 🍛"
                        continue

                    if current_meal and line:
                        meals[current_meal] += f"- {line}<br>"

                st.subheader("Your Diet Plan 🥗")

                for meal, content in meals.items():
                    if content:
                        st.markdown(f"""
                            <div class="diet-card">
                                <b>{meal}</b><br><br>
                                {content}
                            </div>
                        """, unsafe_allow_html=True)

                pdf = create_pdf(patient_id, diet_text)
                with open(pdf, "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        f,
                        file_name=pdf,
                        mime="application/pdf"
                    )

            else:
                st.error("❌ Diet generation failed")

        else:
            st.warning("⚠️ Enter numeric ID only")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce",
        use_container_width=True

    )
    st.caption("Healthy Eating = Healthy Life 🥗")

# ==============================
# Footer
# ==============================
st.markdown("""
<div style="text-align:center; font-size:14px; margin-top:20px; color:#00ff7f;">
💡 Tip: Drink water & walk 30 minutes daily
</div>
""", unsafe_allow_html=True)




https://ai-diet-planner-vjmgltvwuegdxoudqq9kvx.streamlit.app/#your-diet-plan
https://share.streamlit.io/