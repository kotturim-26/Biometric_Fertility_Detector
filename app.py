import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from openai import OpenAI

from sim_engine import generate_cycle_data
from logic_layer import detect_ovulation, get_fertility_window

# 1. SETUP & CREDENTIAL MANAGEMENT
load_dotenv()

# Check local .env first; fallback to Streamlit Cloud secrets if deployed
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY and "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

st.set_page_config(page_title="CyclicSense AI | Oura Integration Demo", layout="wide")

# 2. HEADER & SCIENTIFIC DISCLAIMER
st.title("🧬 CyclicSense: Multimodal Fertility Engine")
st.markdown("### *Prototype using simulated sensor data based on Oura Ring metrics*")
st.caption("Implementation of the physiology-first methodology validated in Thigpen et al. (JMIR 2025).")

# 3. SIDEBAR (Professionalized Labels)
st.sidebar.header("Algorithm Configuration")
c_length = st.sidebar.slider("Cycle Length (days)", 21, 45, 32)
st.sidebar.info("The sliding-window detector identifies shifts independent of cycle length, addressing the 7-day MAE error seen in calendar-based apps.")

# 4. DATA PROCESSING
df = generate_cycle_data(c_length)
ov_day = detect_ovulation(df)
win_start, win_end = get_fertility_window(ov_day)

# 5. VISUALIZATION (Plotly)
fig = go.Figure()

# Distal Skin Temp Trace
fig.add_trace(go.Scatter(
    x=df['CycleDay'], y=df['SkinTemp'], 
    name='Skin Temp (°F)', 
    line=dict(color='#FF4B4B', width=3)
))

# HRV Trace (Secondary Axis)
fig.add_trace(go.Scatter(
    x=df['CycleDay'], y=df['HRV'], 
    name='HRV (ms)', 
    line=dict(color='#0068C9', dash='dot'), 
    yaxis='y2'
))

# Fertile Window Overlay
if win_start and win_end:
    fig.add_vrect(
        x0=win_start, x1=win_end,
        fillcolor="LightGreen", opacity=0.2, layer="below", line_width=0,
        annotation_text="Estimated Fertile Window", annotation_position="top left"
    )
    fig.add_vline(x=ov_day, line_width=2, line_dash="dash", line_color="green")

fig.update_layout(
    xaxis_title="Day of Cycle",
    yaxis=dict(title="Skin Temp (°F)", tickformat=".1f"),
    yaxis2=dict(title="HRV (ms)", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 6. CLINICAL STATUS CARDS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Detected Shift Point", f"Day {ov_day}" if ov_day else "Analyzing...")
with col2:
    st.metric("Correlation Window", f"Day {win_start} - {win_end}" if win_start else "N/A")
with col3:
    status = "Post-Ovulatory" if ov_day else "Follicular"
    st.info(f"Physiological State: **{status}**")

# 7. METHODOLOGY & REASONING (Renamed & Professionally Prompted)
st.divider()
if st.button("View Methodology & Algorithm Reasoning"):
    try:
        with st.spinner("Analyzing cross-signal synchrony..."):
            prompt = f"""
            System: You are a HealthTech Data Scientist. 
            User: Analyze this {c_length}-day cycle data. 
            - Ovulation detected via skin temp shift on Day {ov_day}.
            - Window: {win_start} to {win_end}.
            Explain how this physiology-based detection compares to Oura Ring's benchmarks 
            (MAE 1.26 days) in the JMIR 2025 study. Focus on the correlation between 
            the HRV drop and the thermal shift.
            """
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown("### Algorithm Analysis")
            st.write(response.choices[0].message.content)
    except Exception as e:
        st.error("Model reasoning is currently unavailable. Review the code logic for deterministic calculations.")

st.caption("Built by Maanasvi Kotturi | UT Austin Biomedical Engineering | Prototype")
