import streamlit as st
import requests
import os
from PIL import Image
import time

# Get backend URL from environment variable, fallback to localhost for development
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# Page configuration
st.set_page_config(
    page_title="AI-NutriCare - Smart Diet Planning",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        text-align: center;
        margin: 2rem 0;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .warning-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .success-card {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .info-card {
        background: linear-gradient(135deg, #74c0fc 0%, #339af0 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar-content {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Get backend URL from environment variable, fallback to localhost for development
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("🏥 AI-NutriCare")
    st.markdown("**Smart Diet Planning System**")
    st.markdown("---")

    st.markdown("### 📋 How it works:")
    st.markdown("1. 📤 Upload medical report")
    st.markdown("2. 🤖 AI analyzes biomarkers")
    st.markdown("3. 🍎 Get personalized diet plan")
    st.markdown("4. 📊 Track health improvements")

    st.markdown("---")
    st.markdown("### 🔧 System Status")
    if BACKEND_URL.startswith("http://127.0.0.1"):
        st.info("🖥️ Running locally")
    else:
        st.success("☁️ Running on cloud")

    st.markdown("### 📞 Support")
    st.markdown("For medical advice, consult healthcare professionals.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏥 AI-NutriCare</h1>
    <h3>Revolutionary AI-Powered Diet Planning</h3>
    <p>Upload your medical report and get a personalized, biomarker-aware diet plan in seconds</p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Medical Report")
    st.markdown("Supported formats: PDF, JPG, PNG")
    uploaded_file = st.file_uploader("Upload Medical Report", type=["pdf", "jpg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        # Analyze button with loading state
        if st.button("🔍 Analyze & Generate Diet Plan", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your medical report..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                try:
                    response = requests.post(
                        f"{BACKEND_URL}/upload/",
                        files=files,
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Success animation
                        st.balloons()
                        st.success("🎉 Analysis Complete!")

                        # Results in tabs
                        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🧬 Biomarkers", "👤 Patient Info", "🍎 Diet Plan"])

                        with tab1:
                            st.markdown('<div class="result-card">', unsafe_allow_html=True)
                            st.subheader("📊 Analysis Overview")

                            # Risk level with color coding
                            risk_level = data.get("risk_level", "unknown")
                            risk_colors = {
                                "low": "success-card",
                                "medium": "warning-card",
                                "high": "info-card"
                            }

                            risk_class = risk_colors.get(risk_level.lower(), "info-card")
                            st.markdown(f'<div class="{risk_class}">', unsafe_allow_html=True)
                            st.markdown(f"### Risk Level: {risk_level.upper()}")
                            st.markdown("Based on biomarker analysis")
                            st.markdown('</div>', unsafe_allow_html=True)

                            # Detected conditions
                            conditions = data.get("detected_conditions", [])
                            if conditions:
                                st.subheader("🔍 Detected Conditions")
                                cols = st.columns(min(len(conditions), 3))
                                for i, condition in enumerate(conditions):
                                    with cols[i % 3]:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <h4>{condition.replace('_', ' ').title()}</h4>
                                        </div>
                                        """, unsafe_allow_html=True)
                            else:
                                st.info("No specific conditions detected")

                            st.markdown('</div>', unsafe_allow_html=True)

                        with tab2:
                            st.markdown('<div class="result-card">', unsafe_allow_html=True)
                            st.subheader("🧬 Biomarker Analysis")

                            biomarkers = data.get("biomarkers", {})
                            if biomarkers:
                                cols = st.columns(2)
                                for i, (biomarker, info) in enumerate(biomarkers.items()):
                                    with cols[i % 2]:
                                        status_icon = "⚠️" if info.get("abnormal") else "✅"
                                        status_color = "red" if info.get("abnormal") else "green"

                                        st.markdown(f"""
                                        <div style="background: {'#ffe6e6' if info.get('abnormal') else '#e6ffe6'};
                                                  padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                                                  border-left: 4px solid {status_color};">
                                            <h4>{status_icon} {biomarker.replace('_', ' ').title()}</h4>
                                            <p style="font-size: 1.2em; font-weight: bold;">
                                                {info.get('value', 'N/A')} {info.get('unit', '')}
                                            </p>
                                            <small style="color: {status_color};">
                                                {'Abnormal' if info.get('abnormal') else 'Normal'}
                                            </small>
                                        </div>
                                        """, unsafe_allow_html=True)
                            else:
                                st.info("No biomarkers detected")

                            st.markdown('</div>', unsafe_allow_html=True)

                        with tab3:
                            st.markdown('<div class="result-card">', unsafe_allow_html=True)
                            st.subheader("👤 Patient Information")

                            patient_info = data.get("patient_info", {})
                            if patient_info:
                                col1, col2 = st.columns(2)

                                with col1:
                                    if patient_info.get("name"):
                                        st.metric("👤 Name", patient_info["name"])
                                    if patient_info.get("age"):
                                        st.metric("🎂 Age", f"{patient_info['age']} years")

                                with col2:
                                    if patient_info.get("gender"):
                                        st.metric("⚧️ Gender", patient_info["gender"].title())
                            else:
                                st.info("Patient information not extracted from report")

                            st.markdown('</div>', unsafe_allow_html=True)

                        with tab4:
                            st.markdown('<div class="result-card">', unsafe_allow_html=True)
                            st.subheader("🍎 Personalized Diet Plan")

                            diet = data.get("diet_plan", {})

                            # Diet rules
                            rules = diet.get("diet_rules", [])
                            if rules:
                                st.markdown("### 📋 Diet Rules")
                                rule_cols = st.columns(min(len(rules), 2))
                                for i, rule in enumerate(rules):
                                    with rule_cols[i % 2]:
                                        st.markdown(f"✅ {rule}")

                            # Medical conditions
                            conditions = diet.get("medical_condition", [])
                            if conditions:
                                st.markdown("### 🏥 Medical Conditions Considered")
                                st.write(", ".join(conditions))

                            # AI-generated diet plan
                            diet_plan_text = diet.get("diet_plan", "")
                            if diet_plan_text:
                                st.markdown("### 📝 AI-Generated Meal Plan")
                                st.markdown(diet_plan_text)
                            else:
                                st.warning("No detailed diet plan generated")

                            # Footer info
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**🤖 Generated by:** {diet.get('generated_by', 'AI System')}")
                            with col2:
                                st.markdown(f"**📅 Generated:** {time.strftime('%Y-%m-%d %H:%M')}")

                            st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error(f"❌ Backend Error: {response.status_code}")
                        st.error(f"Details: {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection Error: {str(e)}")
                    st.info("💡 Make sure the backend server is running")

    else:
        st.info("👆 Please upload a medical report to get started")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚠️ <strong>Medical Disclaimer:</strong> This AI tool provides general dietary suggestions based on medical reports.
    Always consult with healthcare professionals for medical advice and dietary planning.</p>
    <p>Built By Yashasvi Bhati ❤️ </p>
</div>
""", unsafe_allow_html=True)
