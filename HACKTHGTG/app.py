import streamlit as st
import pandas as pd
import random
import time
import requests
from datetime import datetime

# --- CONFIG & INITIALIZATION ---
st.set_page_config(page_title="SentinAI | Caregiver Dashboard", layout="wide")

# Ini rahsia Streamlit: Kita simpan memori (state) supaya semua kotak berubah serentak
if 'sys_status' not in st.session_state: st.session_state.sys_status = "Green"
if 'history' not in st.session_state: st.session_state.history = ["• System initialized and monitoring."]
if 'med_rec' not in st.session_state: st.session_state.med_rec = "Awaiting agent analysis..."
if 'vision_conf' not in st.session_state: st.session_state.vision_conf = "98%"

# --- LOAD CSS ---
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# --- TITLE ---
st.markdown("<h1 style='text-align: center; color: #ffffff; letter-spacing: 3px; font-weight: 900; font-size: 70px;'>SENTIN<span style='color: #6366f1;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-top: -15px;'>Autonomous Multi-Agent Elderly Care System</p>", unsafe_allow_html=True)

# Susun atur Kotak (Kita declare dulu supaya senang update)
sidebar_container = st.sidebar.container()
col_vid, col_status = st.columns([1.8, 1])

# --- BAHAGIAN TENGAH: OTAM AUTONOMI AI ---
with col_vid:
    st.markdown("#### 🤖 Autonomous Agent Patrol (Live)")
    st.caption("The AI Agent dynamically monitors various CCTV angles and analyzes behavior.")
    
    if st.button("🔄 INITIATE AGENT PATROL", use_container_width=True):
        # Senarai pangkalan data video rawak awak
        scenarios = [
            {"video": "HACKTHGTG/tidur.mp4", "event": "sleeping_peacefully", "danger": False, "conf": "96%", "rec": "Patient is resting. Maintain a quiet environment and dim the lights."},
            {"video": "HACKTHGTG/baca.mp4", "event": "reading_a_book", "danger": False, "conf": "94%", "rec": "Patient is engaging in cognitive activity. Ensure proper room lighting."},
            {"video": "HACKTHGTG/berborak.mp4", "event": "chatting_with_friends", "danger": False, "conf": "92%", "rec": "Social interaction detected. Excellent for mental well-being."},
            {"video": "HACKTHGTG/demo_jatuh.mp4", "event": "fall_detected", "danger": True, "conf": "99%", "rec": "CRITICAL ACTION TAKEN: Alerting family and dispatching emergency unit."}
        ]
        
        current = random.choice(scenarios)
        current_time = datetime.now().strftime("%I:%M %p")
        
        # 1. Mainkan Video Baru
        st.video(current["video"], autoplay=True, loop=True)
        
        with st.spinner("👁️ Vision Agent is analyzing behavior..."):
            time.sleep(2)
            st.info(f"**System Log:** Behavior `{current['event']}` detected.")
            st.write("Cross-referencing with Gemini Cloud for protocol...")
            
            # 2. Hantar ke Google Cloud Run awak
            url_cloud = "https://sentinai-backend-137181402202.asia-southeast1.run.app/api/emergency-alert"
            payload = {"event_type": current["event"], "confidence": float(current["conf"].strip('%'))/100, "timestamp": pd.Timestamp.now().isoformat() + "Z"}
            
            try:
                res = requests.post(url_cloud, json=payload, timeout=8)
                data = res.json() if res.status_code == 200 else {}
                gemini_action = data.get('gemini_action', 'Protocol executed based on local logic.')
                
                st.markdown("---")
                # 3. UPDATE SEMUA DATA DI DASHBOARD SECARA AUTOMATIK
                if current["danger"]:
                    st.error(f"🚨 **EMERGENCY AI ACTION:** {gemini_action}")
                    st.session_state.sys_status = "Red"
                    st.session_state.history.insert(0, f"• {current_time}: CRITICAL - Fall detected! Protocol initiated.")
                else:
                    st.success(f"✅ **DAILY LOG:** {gemini_action}")
                    st.session_state.sys_status = "Green"
                    st.session_state.history.insert(0, f"• {current_time}: Routine check - {current['event'].replace('_', ' ')}.")
                
                st.session_state.med_rec = current["rec"]
                st.session_state.vision_conf = current["conf"]
                
            except Exception as e:
                st.error("Failed to connect to Cloud Run Backend.")


# --- BAHAGIAN KIRI (SIDEBAR): KINI AUTO-UPDATE ---
with sidebar_container:
    st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/2382/2382461.png' width='80'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Caregiver Mode</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.subheader("📍 Action Center")
    if st.button("🚨 CALL AMBULANCE", use_container_width=True):
        st.toast("Emergency Protocol Initiated!", icon="🚨")
        st.error("Connecting to Emergency Services (999)...")
    
    st.write("---")
    st.subheader("🔔 Notification History")
    # Tunjuk 4 log terakhir sahaja supaya tak serabut
    for item in st.session_state.history[:4]: 
        st.caption(item)
        
    st.write("---")
    st.subheader("💡 Medical Recommendation")
    st.info(f"**Gemini Reasoning:** {st.session_state.med_rec}")


# --- BAHAGIAN KANAN (METRICS): KINI AUTO-UPDATE ---
with col_status:
    st.markdown("#### 🚦 Live Status Indicator")
    
    if st.session_state.sys_status == "Green":
        st.markdown('<div class="status-indicator status-green">● GREEN (SAFE)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-red">● RED (CRITICAL: FALL)</div>', unsafe_allow_html=True)

    st.markdown("#### 📊 System Metrics")
    m1, m2 = st.columns(2)
    m1.metric("Vision Confidence", st.session_state.vision_conf, "YOLOv8")
    m2.metric("Processing Time", "0.8s", "Fast")
    
    st.write("---")
    st.markdown("#### 🛠️ Ecosystem")
    st.caption("• Model: Gemini 2.5 Flash")
    st.caption("• Backend: Google Cloud Run")
