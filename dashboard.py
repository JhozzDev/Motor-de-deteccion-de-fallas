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

# Header
st.set_page_config(page_title="Dashboard", layout="wide")

#  Auto refresh 
st_autorefresh(interval=1000, key="refresh")

#  Sesiones 
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
st.divider()
chart_placeholder = st.empty()

events_placeholder = st.empty()

# Generador de datos
def generar_datos():
    return {
        "temperature": random.randint(60, 100),
        "pressure": random.randint(50, 100),
        "humidity": random.randint(40, 100),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

# Loop principal 
if st.session_state.running:

    data = generar_datos()

    # Guardar datos
    st.session_state.buffer.append(data)
 
    # Ventana deslizante
    st.session_state.buffer = st.session_state.buffer[-MAX_POINTS:]

    # Gráfico
    df = pd.DataFrame(st.session_state.buffer)
    df.set_index("timestamp", inplace=True)

    # Plantilla del grafico
    with chart_placeholder.container():
         st.line_chart(df, color=["#FF000080", "#0000FF80", "#C9CC0480"], height=700)
         
    # LLamada Api - La api hace que se recargue la pagina
    try:
        response = requests.post(API_URL, json=data, timeout=3)

        # Pasa error si peticion falla
        response.raise_for_status() 

        # Traspasar json 
        result = response.json()
        new_events = result.get("events", [])

        with events_placeholder:
            if new_events:
                for event in new_events:
                    st.session_state.events.append(event)
                    st.warning(f"{event["rule"].upper()} | {event["severity"].upper()} | {event["timestamp"].upper()}")

    # Excepcion
    except Exception as e:
        st.session_state.events.append({
            "severity": "error",
            "rule": "API",
            "timestamp": str(e)
        })
        

else:
    with chart_placeholder:
        st.bar_chart()
