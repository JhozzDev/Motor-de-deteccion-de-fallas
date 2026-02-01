import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

from core.rule import Rule
from core.engine import RuleEngine
import smtplib
from email.message import EmailMessage


df = pd.read_csv("data/temperaturas.csv")

def high_temp_overheat(df):
    return df["temperature"].iloc[-1] > 100  

def high_temp_prom(df):
    return df["temperature"].mean() > 80     

def high_temp_max(df):
    return df["temperature"].iloc[-1] > 150  


rules = [
    Rule(name="Overheat", sensors=["temperature"], condition=high_temp_overheat, duration=1, severity="HIGH"),
    Rule(name="HIGH-PROM", sensors=["temperature"], condition=high_temp_prom, duration=3, severity="HIGH"),
    Rule(name="MAX", sensors=["temperature"], condition=high_temp_max, duration=0, severity="CRITIC"),
]

engine = RuleEngine(rules)

st.title("Dashboard")
st.subheader("Motor de deteccion de fallas")

chart = st.empty()

buffer = []
windows = 30
start_time = datetime.now()

event_table = st.empty()
event_log = []

for i, d in enumerate(df["temperaturas"]):
    buffer.append({
        "temperature": d,
        "Timestamp": datetime.now()
    })
    

    now = datetime.now()
    buffer = [d for d in buffer if (now - d["Timestamp"]).total_seconds() <= windows]
    df_windows = pd.DataFrame(buffer)
    df_windows["Timestamp_str"] = df_windows["Timestamp"].dt.strftime("%H:%M:%S")
    df_windows.set_index("Timestamp_str", inplace=True)
    promedio = df_windows["temperature"].mean()
    max = df_windows["temperature"].max()
    min = df_windows["temperature"].min()


  
    
    chart.line_chart(df_windows["temperature"])

    events = engine.process(df_windows)
    
    
    for event in events:
        # Mostrar en pantalla
        if event.severity == "CRITIC":
            st.error(f"{event.rule_name} -> {event.message} ({event.severity})")
            print(event)
        else:
            st.warning(f"{event.rule_name} -> {event.message} ({event.severity})")
            print(event)
        # Guardar en log
        event_log.append({
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Regla": event.rule_name,
            "Severidad": event.severity,
            "Mensaje": event.message
        })
       
    
    # Actualizar tabla de eventos
    if event_log:
        event_table.dataframe(pd.DataFrame(event_log))
    

    time.sleep(1)