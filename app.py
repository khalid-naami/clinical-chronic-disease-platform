"""Clinical Chronic Disease Intelligence, Precision Nutrition & Medical Research Platform.

Standardized clean English UI with 10s Live Auto-Refresh, comprehensive clinical pathology,
therapeutic nutrition blueprints, FITT exercise prescriptions, risk calculators,
and live peer-reviewed medical journal breakthroughs feed.
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.diseases_database import ChronicDiseasesManager, CHRONIC_DISEASES_DB
from src.nutrition_engine import NutritionEngine
from src.exercise_prescription import ExerciseEngine
from src.biomarker_calculator import BiomarkerCalculator
from src.medical_journal_client import MedicalJournalClient
from src.visualizer import (
    create_macronutrient_donut,
    create_risk_score_gauge,
    create_global_epidemiology_bar,
    create_exercise_volume_gauge
)

# Streamlit Page Setup
st.set_page_config(
    page_title="Clinical Chronic Disease & Medical Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional Clinical Dark CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #34d399;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #38bdf8;
    }
    .clinical-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .journal-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-left: 5px solid #818cf8;
        border-radius: 10px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
    }
    .evidence-badge {
        background: #0284c7;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Journal Client
@st.cache_resource
def get_journal_client() -> MedicalJournalClient:
    return MedicalJournalClient()

journal_client = get_journal_client()

# Sidebar: Disease Selection & Auto-Refresh
st.sidebar.markdown("## 🧬 Chronic Disease Selection")
all_diseases = ChronicDiseasesManager.get_all_disease_names()
selected_disease = st.sidebar.selectbox("Select Target Chronic Pathology:", all_diseases, index=0)
disease_data = ChronicDiseasesManager.get_disease(selected_disease)
nutrition_data = NutritionEngine.get_protocol(selected_disease)
exercise_data = ExerciseEngine.get_protocol(selected_disease)

# 10s Live Auto-Refresh
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Live Telemetry & Auto-Refresh")
auto_refresh_enabled = st.sidebar.toggle("10s Auto-Refresh (Live Sync)", value=True)
refresh_counter = 0
if auto_refresh_enabled:
    refresh_counter = st_autorefresh(interval=10000, limit=None, key="clinical_auto_refresh_10s")

if st.sidebar.button("🔄 Force Refresh Clinical Feed", key="btn_refresh_now"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### 📋 Disease Metadata:
- **Category:** `{disease_data['category']}`
- **ICD-10 Code:** `{disease_data['icd10']}`
- **Clinical Consensus:** `{disease_data['guidelines']}`
- **Annual Global Deaths:** `{disease_data['annual_mortality']}`
""")

# Main Header
st.markdown('<div class="main-title">🧬 Clinical Chronic Disease & Medical Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Evidence-Based Pathophysiology | Therapeutic Nutrition Blueprints | FITT Exercise Prescriptions | Risk Calculators | Breakthrough Medical Journal Feed</div>', unsafe_allow_html=True)

# Live Status Badge
now_utc_str = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
if auto_refresh_enabled:
    st.markdown(f'<div class="live-badge">🟢 LIVE CLINICAL TELEMETRY ACTIVE &bull; Auto-Refreshing every 10s &bull; Last Synced: {now_utc_str} &bull; Cycle #{refresh_counter}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="live-badge" style="background:rgba(148,163,184,0.1); border-color:rgba(148,163,184,0.3); color:#94a3b8;">⏸️ LIVE SYNC PAUSED &bull; Last Synced: {now_utc_str}</div>', unsafe_allow_html=True)

# Top KPI Metric Cards (5 Highlights)
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Target Pathology</div>
        <div class="metric-value">{disease_data['icon']} {disease_data['id']}</div>
        <div class="metric-sub">{disease_data['category'][:18]}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Global Prevalence</div>
        <div class="metric-value">👥 {disease_data['prevalence_global'].split()[0]}M</div>
        <div class="metric-sub">{disease_data['prevalence_global'].split('(')[-1].replace(')', '') if '(' in disease_data['prevalence_global'] else 'Global Cases'}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Annual Mortality</div>
        <div class="metric-value">⚠️ {disease_data['annual_mortality'].split()[0]}M</div>
        <div class="metric-sub">Deaths / Year Worldwide</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Therapeutic Diet</div>
        <div class="metric-value">🥗 {nutrition_data['diet_name'].split()[0]}</div>
        <div class="metric-sub">{nutrition_data['diet_name'][:20]}</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Exercise Target</div>
        <div class="metric-value">🏃 {exercise_data['target_weekly_volume'].split()[0]}m</div>
        <div class="metric-sub">Weekly FITT Volume</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs (6 Clinical Modules)
tabs = st.tabs([
    "🫀 Pathophysiology & Biomarkers",
    "🥗 Medical Nutrition & Diets",
    "🏃 Therapeutic Exercise (FITT)",
    "📊 Patient Risk Calculator",
    "🔬 Medical Journal & Breakthroughs",
    "🌍 Global Epidemiology & Burden"
])

# ----------------- TAB 1: Clinical Pathophysiology -----------------
with tabs[0]:
    st.markdown(f"### {disease_data['icon']} {selected_disease} — Clinical Profile & Pathophysiology")
    
    col_p1, col_p2 = st.columns([1.2, 1])
    with col_p1:
        st.markdown(f"""
        <div class="clinical-card">
            <h4>📖 Clinical Definition</h4>
            <p>{disease_data['summary']}</p>
            <hr style="border-color: rgba(56, 189, 248, 0.2);">
            <h4>🔬 Molecular & Cellular Pathophysiology</h4>
            <p>{disease_data['pathophysiology']}</p>
            <hr style="border-color: rgba(56, 189, 248, 0.2);">
            <h4>📚 Gold-Standard Guideline Consensus</h4>
            <code>{disease_data['guidelines']}</code>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("#### ⚠️ Major Clinical Complications & End-Organ Risks")
        for comp in disease_data["key_complications"]:
            st.markdown(f"- 🔴 **{comp}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🧬 Modifiable vs Non-Modifiable Risk Factors")
        st.markdown("**Modifiable:** " + ", ".join(disease_data["risk_factors"]["modifiable"]))
        st.markdown("**Non-Modifiable:** " + ", ".join(disease_data["risk_factors"]["non_modifiable"]))

    st.markdown("---")
    st.markdown("#### 🎯 Primary Target Biomarkers & Clinical Thresholds")
    df_bio = pd.DataFrame(disease_data["primary_biomarkers"])
    st.dataframe(df_bio.rename(columns={
        "name": "Biomarker Name",
        "unit": "Measurement Unit",
        "optimal": "Optimal Health Range",
        "pre_disease": "Borderline / Pre-Disease",
        "target_managed": "Clinical Management Target",
        "critical": "Critical Danger Level"
    }), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 💊 Standard Pharmacological Pillars & Drug Classes")
    df_drugs = pd.DataFrame(disease_data["pharmacological_pillars"])
    st.dataframe(df_drugs.rename(columns={
        "class": "Pharmacological Drug Class",
        "mechanism": "Primary Mechanism of Action"
    }), use_container_width=True, hide_index=True)

# ----------------- TAB 2: Medical Nutrition & Diets -----------------
with tabs[1]:
    st.markdown(f"### 🥗 Therapeutic Clinical Nutrition Protocol — {selected_disease}")
    st.markdown(f"**Prescribed Protocol:** `{nutrition_data['diet_name']}`")
    st.info(f"💡 **Scientific Rationale:** {nutrition_data['scientific_rationale']}")

    n_col1, n_col2 = st.columns([1, 1.2])
    with n_col1:
        fig_donut = create_macronutrient_donut(nutrition_data["macros"], nutrition_data["diet_name"])
        st.plotly_chart(fig_donut, use_container_width=True)

    with n_col2:
        st.markdown("#### 🧪 Daily Micronutrient & Electrolyte Guardrails")
        for k, v in nutrition_data["micronutrient_targets"].items():
            st.markdown(f"- **{k}:** ` {v} `")
        
        if "Daily Fiber" in nutrition_data["macros"]:
            st.markdown(f"- **Daily Therapeutic Fiber:** ` {nutrition_data['macros']['Daily Fiber']} `")

    st.markdown("---")
    sn1, sn2 = st.columns(2)
    with sn1:
        st.markdown("#### 🥑 Recommended Therapeutic Superfoods")
        for sf in nutrition_data["therapeutic_superfoods"]:
            st.markdown(f"""
            <div style="background:rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:10px; border-radius:6px; margin-bottom:8px;">
                <b>🟢 {sf['food']}</b><br>
                <span style="font-size:0.85rem; color:#cbd5e1;">{sf['mechanism']}</span>
            </div>
            """, unsafe_allow_html=True)

    with sn2:
        st.markdown("#### 🚫 Strictly Prohibited & Harmful Foods")
        for pf in nutrition_data["strictly_prohibited_foods"]:
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.1); border-left:4px solid #ef4444; padding:10px; border-radius:6px; margin-bottom:8px;">
                <b>🔴 {pf['food']}</b><br>
                <span style="font-size:0.85rem; color:#fca5a5;"><b>Clinical Hazard:</b> {pf['hazard']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🍽️ 1-Day Clinical Meal Blueprint Example")
    mp = nutrition_data["sample_meal_plan"]
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"**🍳 Breakfast:**<br>{mp.get('breakfast', 'N/A')}", unsafe_allow_html=True)
    m2.markdown(f"**🥗 Lunch:**<br>{mp.get('lunch', 'N/A')}", unsafe_allow_html=True)
    m3.markdown(f"**🍲 Dinner:**<br>{mp.get('dinner', 'N/A')}", unsafe_allow_html=True)
    m4.markdown(f"**🌰 Snacks:**<br>{mp.get('snacks', 'N/A')}", unsafe_allow_html=True)

# ----------------- TAB 3: Therapeutic Exercise (FITT) -----------------
with tabs[2]:
    st.markdown(f"### 🏃 FITT Medical Exercise Prescription — {selected_disease}")
    st.markdown(f"**Protocol Designation:** `{exercise_data['prescription_title']}`")

    e_col1, e_col2 = st.columns([1.2, 1])
    with e_col1:
        st.markdown("#### 🏃 Aerobic Conditioning Protocol")
        a_fitt = exercise_data["aerobic_fitt"]
        st.markdown(f"- **Frequency:** `{a_fitt['frequency']}`")
        st.markdown(f"- **Intensity:** `{a_fitt['intensity']}`")
        st.markdown(f"- **Time / Duration:** `{a_fitt['time']}`")
        st.markdown(f"- **Modality / Type:** `{a_fitt['type']}`")

        st.markdown("#### 🏋️ Progressive Resistance Training Protocol")
        r_fitt = exercise_data["resistance_fitt"]
        st.markdown(f"- **Frequency:** `{r_fitt['frequency']}`")
        st.markdown(f"- **Intensity:** `{r_fitt['intensity']}`")
        st.markdown(f"- **Time / Duration:** `{r_fitt['time']}`")
        st.markdown(f"- **Modality / Type:** `{r_fitt['type']}`")

    with e_col2:
        fig_ex_gauge = create_exercise_volume_gauge(target_min=150, current_min=135)
        st.plotly_chart(fig_ex_gauge, use_container_width=True)

    st.markdown("---")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("#### 🔬 Molecular & Physiological Mechanisms of Exercise")
        for mech in exercise_data["physiological_mechanisms"]:
            st.markdown(f"- ⚡ **{mech}**")

    with m_col2:
        st.markdown("#### 🛑 Clinical Contraindications & Safety Precautions")
        for sc in exercise_data["safety_contraindications"]:
            st.markdown(f"""
            <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:10px; border-radius:6px; margin-bottom:8px;">
                <span style="font-size:0.85rem; color:#fde68a;">⚠️ {sc}</span>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 4: Patient Risk Calculator -----------------
with tabs[3]:
    st.markdown("### 📊 Interactive Patient Biomarker & Multi-System Risk Staging")
    st.markdown("Enter patient clinical parameters to calculate ADA Diabetes Risk, 10-Year ASCVD Cardiovascular Risk, KDIGO CKD Staging, and Comprehensive Longevity Index.")

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        input_age = st.number_input("Age (Years):", min_value=18, max_value=100, value=52)
        input_gender = st.selectbox("Biological Sex:", ["Male", "Female"], index=0)
        input_bmi = st.number_input("Body Mass Index (BMI):", min_value=15.0, max_value=50.0, value=27.4, step=0.1)
        input_weekly_ex = st.slider("Weekly Moderate Exercise (Minutes):", min_value=0, max_value=400, value=90, step=15)

    with rc2:
        input_sbp = st.number_input("Systolic Blood Pressure (mmHg):", min_value=80, max_value=240, value=138)
        input_dbp = st.number_input("Diastolic Blood Pressure (mmHg):", min_value=50, max_value=140, value=88)
        input_hba1c = st.number_input("Hemoglobin A1c (%):", min_value=4.0, max_value=15.0, value=6.1, step=0.1)
        input_fpg = st.number_input("Fasting Glucose (mg/dL):", min_value=60, max_value=350, value=112)

    with rc3:
        input_ldl = st.number_input("LDL-Cholesterol (mg/dL):", min_value=30, max_value=300, value=135)
        input_hdl = st.number_input("HDL-Cholesterol (mg/dL):", min_value=15, max_value=100, value=44)
        input_egfr = st.number_input("eGFR (mL/min/1.73m²):", min_value=5, max_value=130, value=78)
        
        c_smk, c_cad, c_t2d = st.columns(3)
        input_smoker = c_smk.checkbox("Active Smoker", value=False)
        input_fam_cad = c_cad.checkbox("Family CAD", value=True)
        input_fam_t2d = c_t2d.checkbox("Family Diabetes", value=True)

    risk_result = BiomarkerCalculator.calculate_patient_risk(
        age=input_age,
        gender=input_gender,
        systolic_bp=input_sbp,
        diastolic_bp=input_dbp,
        hba1c=input_hba1c,
        fasting_glucose=input_fpg,
        ldl_c=input_ldl,
        hdl_c=input_hdl,
        egfr=input_egfr,
        bmi=input_bmi,
        weekly_exercise_min=input_weekly_ex,
        is_smoker=input_smoker,
        family_history_cad=input_fam_cad,
        family_history_diabetes=input_fam_t2d
    )

    st.markdown("---")
    st.markdown("#### 🎯 Clinical Risk Stratification Readout")

    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(create_risk_score_gauge(risk_result["health_index"], "Longevity & Health Index", "Overall Preventive Staging"), use_container_width=True)
    with g2:
        st.plotly_chart(create_risk_score_gauge(risk_result["t2d_risk_pct"], "Diabetes Risk Score", risk_result["t2d_stage"]), use_container_width=True)
    with g3:
        st.plotly_chart(create_risk_score_gauge(risk_result["ascvd_risk_pct"], "10-Yr ASCVD Risk", risk_result["cv_category"]), use_container_width=True)

    st.markdown(f"""
    <div style="background:rgba(30,41,59,0.7); border:1px solid rgba(56,189,248,0.3); border-radius:10px; padding:1.2rem; margin-top:1rem;">
        <h4>📋 Multi-System Staging Summary:</h4>
        - <b>Blood Pressure Classification:</b> <span style="color:{risk_result['bp_status_color']}; font-weight:bold;">{risk_result['bp_stage']}</span> ({input_sbp}/{input_dbp} mmHg)<br>
        - <b>Metabolic & Glycemic Category:</b> <b>{risk_result['t2d_stage']}</b> (HbA1c: {input_hba1c}%, FPG: {input_fpg} mg/dL)<br>
        - <b>Cardiovascular Atherosclerotic Category:</b> <b>{risk_result['cv_category']}</b> (LDL-C: {input_ldl} mg/dL, HDL-C: {input_hdl} mg/dL)<br>
        - <b>Renal KDIGO Category:</b> <b>{risk_result['kdigo_stage']}</b> ({risk_result['renal_risk_level']})
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💡 Tailored Clinical Action Steps:")
    for rec in risk_result["recommendations"]:
        st.markdown(f"- 🩺 {rec}")

# ----------------- TAB 5: Medical Journal & Breakthroughs -----------------
with tabs[4]:
    st.markdown(f"### 🔬 Medical Research Journal & Breakthrough Discoveries — {selected_disease}")
    st.markdown("Curated landmark Phase III/IV clinical trials and live peer-reviewed research indexed from **Europe PMC & PubMed**.")

    st.markdown("#### 🏆 Landmark Gold-Standard Clinical Trials & Breakthroughs")
    curated_papers = journal_client.get_curated_breakthroughs(selected_disease)
    for p in curated_papers:
        st.markdown(f"""
        <div class="journal-card">
            <span class="evidence-badge">{p['evidence_grade']}</span> &bull; <span style="color:#94a3b8; font-size:0.85rem;">{p['journal']} &bull; {p['date']}</span>
            <h4 style="margin: 0.4rem 0; color:#f8fafc;">{p['title']}</h4>
            <p style="font-size:0.85rem; color:#94a3b8;"><b>Lead Authors:</b> {p['lead_authors']} | <b>DOI:</b> <code>{p['doi']}</code></p>
            <p style="margin: 0.5rem 0; color:#cbd5e1;"><b>Breakthrough Summary:</b> {p['breakthrough_summary']}</p>
            <div style="background:rgba(56,189,248,0.1); border-left:3px solid #38bdf8; padding:8px; border-radius:4px; font-size:0.85rem; color:#e0f2fe;">
                <b>Clinical Takeaway:</b> {p['clinical_takeaway']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🌐 Live Europe PMC & PubMed Research Index")
    custom_search = st.text_input("Search open-access literature database:", value=selected_disease, placeholder="e.g. Semaglutide kidney outcomes, CRISPR PCSK9...")
    
    with st.spinner("Querying live medical research database..."):
        live_trials = journal_client.fetch_live_recent_trials(custom_search, max_results=4)

    for lt in live_trials:
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.25); border-radius:8px; padding:1.1rem; margin-bottom:1rem;">
            <span style="background:#334155; color:#38bdf8; font-size:0.75rem; font-weight:bold; padding:2px 8px; border-radius:4px;">{lt['source']}</span> &bull; <span style="color:#94a3b8; font-size:0.85rem;">{lt['journal']} ({lt['date']})</span>
            <h4 style="margin:0.4rem 0; color:#f1f5f9;">{lt['title']}</h4>
            <p style="font-size:0.8rem; color:#94a3b8;"><b>Authors:</b> {lt['lead_authors']} | <b>DOI:</b> <code>{lt['doi']}</code></p>
            <p style="font-size:0.85rem; color:#cbd5e1;">{lt['abstract']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 6: Global Epidemiology & Burden -----------------
with tabs[5]:
    st.markdown("### 🌍 Global Chronic Disease Burden & Epidemiological Comparison")
    st.markdown("Comparative epidemiological analysis across the 7 major chronic disease categories.")

    st.plotly_chart(create_global_epidemiology_bar(), use_container_width=True)

    st.markdown("""
    #### 💡 Preventive Medicine & Economic Health Impact:
    - **Cardiovascular & Metabolic Dominance:** Ischemic Heart Disease, Stroke, and Type 2 Diabetes account for over **55%** of all preventable chronic disease mortality worldwide.
    - **Lifestyle Reversibility:** Rigorous randomized controlled trials demonstrate that adherence to the **DASH / Mediterranean Dietary Protocols** alongside **150+ minutes/week of exercise** reduces primary cardiovascular and diabetic events by **40% to 58%**, surpassing single-agent pharmacotherapy in early stages.
    - **Economic Burden:** Chronic diseases consume **>75% of global healthcare expenditures**, underscoring the urgent priority for early biomarker screening and precision lifestyle intervention.
    """)
