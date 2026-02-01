import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from core.rule import Rule
from core.engine import RuleEngine



df = pd.read_csv("data/temperaturas.csv")

sensors = ["temperature", "pressure", "humidity"]

def generar_dato_sensor():
    return {
        "temperature": random.randint(50, 120),  
        "pressure": random.randint(90, 120),     
        "humidity": random.randint(30, 90),      
        "Timestamp": datetime.now()
    }

def high_temp_overheat(df):
    return df["temperature"].iloc[-1] > 100  

def high_temp_prom(df):
    return df["temperature"].mean() > 80     

def high_temp_max(df):
    return df["temperature"].iloc[-1] > 150  

def high_pressure(df):
    return df["pressure"].iloc[-1] > 100  

def low_temp(df):
    return df["temperature"].mean() < 40     

def low_pressure(df):
    return df["pressure"].iloc[-1] < 60  

def low_humidity(df):
    return df["humidity"].iloc[-1] < 40  


rules = [
    Rule(name="Over Heat", sensors=["temperature"], condition=high_temp_overheat, duration=1, severity="High"),
    Rule(name="High Prom Temp", sensors=["temperature"], condition=high_temp_prom, duration=1, severity="High"),
    Rule(name="High Pressure", sensors=["pressure"], condition=high_pressure, duration=1, severity="Critic"),
    Rule(name="High Humidity", sensors=["humidity"], condition=high_temp_max, duration=1, severity="Medium"),
    Rule(name="Low Temp", sensors=["temperature"], condition=low_temp, duration=1, severity="High"),
    Rule(name="Low Pressure", sensors=["pressure"], condition=low_pressure, duration=1, severity="Critic"),
    Rule(name="Low Humidity", sensors=["humidity"], condition=low_humidity, duration=1, severity="Medium"),
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

while True:
    data = generar_dato_sensor()
    buffer.append(data)
    

    now = datetime.now()
    buffer = [d for d in buffer if (now - d["Timestamp"]).total_seconds() <= windows]
    df_windows = pd.DataFrame(buffer)
    df_windows["Timestamp_str"] = df_windows["Timestamp"].dt.strftime("%H:%M:%S")
    df_windows.set_index("Timestamp_str", inplace=True)

    promedio = df_windows["temperature"].mean()
    max = df_windows["temperature"].max()
    min = df_windows["temperature"].min()


  
    
    chart.line_chart(df_windows[["temperature", "pressure", 'humidity']])


    events = engine.process(df_windows)
    
    
    for event in events:
        # Mostrar en pantalla
        if event.severity == "Critic" or event.severity == "High":
            st.error(f"{event.rule_name} -> {event.timestamp}")
            print(event)
        else:
            st.warning(f"{event.rule_name} -> {event.timestamp}")
            print(event)
        # Guardar en log
        event_log.append({
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Regla": event.rule_name,
            "Severidad": event.severity,
            "Mensaje": event.message
        })
       
    
  

    time.sleep(1)