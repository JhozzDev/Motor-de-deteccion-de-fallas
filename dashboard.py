import streamlit as st
import requests
import random
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import random

# Configuración 
API_URL = "http://127.0.0.1:8000/process"
MAX_POINTS = 30

st.set_page_config(page_title="Dashboard", layout="centered")

#  Auto refresh 
st_autorefresh(interval=1000, key="refresh")

#  Session State 
if "running" not in st.session_state:
    st.session_state.running = False

if "buffer" not in st.session_state:
    st.session_state.buffer = []

if "events" not in st.session_state:
    st.session_state.events = []

# UI
st.title("Dashboard")
st.subheader("Motor de detección de fallas")

# Botones
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Iniciar"):
        st.session_state.running = True

with col2:
    if st.button("⏹ Detener"):
        st.session_state.running = False

# Placeholders
chart_placeholder = st.empty()
events_placeholder = st.empty()



# Generador de datos
def generar_datos():
    return {
        "temperature": random.randint(60, 120),
        "pressure": random.randint(50,100)
    }

# Loop principal 
if st.session_state.running:

    data = generar_datos()
    now = datetime.now().strftime("%H:%M:%S")

    # Guardar datos
    st.session_state.buffer.append({
        "temperature": data["temperature"],
        "timestamp": now,
        "pressure": data["pressure"]
    })

    st.session_state.buffer = st.session_state.buffer[-MAX_POINTS:]

    # Gráfico
    df = pd.DataFrame(st.session_state.buffer)
    df.set_index("timestamp", inplace=True)
    with chart_placeholder:
         st.bar_chart(df, y=["temperature", "pressure"], color=["#FF000080", "#0000FF80"])
         
         

    data = generar_datos()

    # LLamada Api
    try:
        response = requests.post(API_URL, json=data, timeout=3)
        response.raise_for_status()
        result = response.json()

        new_events = result.get("events", [])
        with events_placeholder:
            st.empty()
            if new_events: 
                for event in new_events:
                   st.session_state.events.append(event)
                   st.error(f"ML Anomaly - {event["severity"].upper()} - {event["timestamp"]}")
              
        st.session_state.events = st.session_state.events[-20:]
             

    except Exception as e:
        st.session_state.events.append({
            "severity": "error",
            "rule": "API",
            "timestamp": str(e)
        })

else:
    with chart_placeholder:
        st.info("Presiona ▶ Iniciar para comenzar el monitoreo")
