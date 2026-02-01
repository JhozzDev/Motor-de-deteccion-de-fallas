import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from core.rule import Rule
from core.engine import RuleEngine
from send_email import Gmail
import joblib

df = pd.read_csv("data/temperaturas.csv")

# Cargar modelo
model = joblib.load("models/model_fallas.pkl")
scaler = joblib.load("models/scaler.pkl")

# Transformar datos
X = df[["temperaturas"]]
X_scaled = scaler.transform(X)

# Predecir Datos
df["ml_result"] = model.predict(X_scaled)
df["estado_ml"] = df["ml_result"].map({
    1: "Normal",
    -1: "Anomalía detectada por ML"
})

# Sensores
sensors = ["temperature", "pressure", "humidity"]

# Deteccion de reglas
def generar_dato_sensor():
    return {
        "temperature": random.randint(50, 130),    
        "pressure": random.randint(40, 150),
        "humidity": random.randint(20, 60),
        "Timestamp": datetime.now()
    }

# El Df es recibido de events

def high_temp_overheat(df):
    return df["temperature"].iloc[-1] > 100  

def high_temp_prom(df):
    return df["temperature"].mean() > 90     

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

def ml_anomaly_rule(df):
    return df["ml_result"].iloc[-1] == -1

# Reglas
rules = [
    Rule(name="ML temp anomaly", sensors=["temperature"], condition=ml_anomaly_rule, duration=1, severity="Critic"),
    Rule(name="High Prom Temp", sensors=["temperature"], condition=high_temp_prom, duration=1, severity="High"),
    Rule(name="High Pressure", sensors=["pressure"], condition=high_pressure, duration=1, severity="Critic"),
    Rule(name="High Humidity", sensors=["humidity"], condition=high_temp_max, duration=1, severity="Medium"),
    Rule(name="Low Temp", sensors=["temperature"], condition=low_temp, duration=1, severity="High"),
    Rule(name="Low Pressure", sensors=["pressure"], condition=low_pressure, duration=1, severity="Critic"),
    Rule(name="Low Humidity", sensors=["humidity"], condition=low_humidity, duration=1, severity="Medium"),
]

# Motor
engine = RuleEngine(rules)

# Inicializar Dashboard
st.title("Dashboard")
st.subheader("Motor de deteccion de fallas")

chart = st.empty()

buffer = []
windows = 30
start_time = datetime.now()

event_table = st.empty()
event_log = []

while True:
    
    # Generar dato
    data = generar_dato_sensor()
    
    # Convertir 2D
    X = [[data["temperature"]]]
    X_scaled2 = scaler.transform(X)

    # Modelo Predice
    pred = model.predict(X_scaled2)[0]

    # Append a buffer
    buffer.append({

      "temperature": data["temperature"],
      "pressure": data["pressure"],
      "humidity": data["humidity"],
      "Timestamp": data["Timestamp"],
      "ml_result": pred

    })

    now = datetime.now()

    # Filtrar Buffer
    buffer = [d for d in buffer if (now - d["Timestamp"]).total_seconds() <= windows]

    # Convertir buffer a Df
    df_windows = pd.DataFrame(buffer)
    df_windows["Timestamp_str"] = df_windows["Timestamp"].dt.strftime("%H:%M:%S")

    # Seleccionar index X
    df_windows.set_index("Timestamp_str", inplace=True)

    chart.line_chart(df_windows[["temperature", "pressure", "humidity"]])

    # Enviar datos al motor
    events = engine.process(df_windows)
     
    for event in events:
        # Mostrar en pantalla
        if event.severity == "Critic":
            st.error(f"{event.rule_name} -> {event.timestamp}")
            print(event, pred)
            
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


