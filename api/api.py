from fastapi import FastAPI
import pandas as pd
from datetime import datetime, timedelta
from core.rule import Rule
from core.engine import RuleEngine
import joblib


app = FastAPI()

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

def ml_anomaly_rule(df):
    return df["ml_result"].iloc[-1] == -1


rules = [
    Rule(name="ML anomaly", sensors=["temperature"], condition=ml_anomaly_rule, duration=1, severity="Critic")]

# Motor
engine = RuleEngine(rules)

@app.get("/home")
def home():
    return {"Greeting": "Hi"}

# Definir ruta
@app.post("/process")
def process_data(data:dict):
    df = pd.DataFrame([data])

    # Escalar
    X = scaler.transform([[data["temperature"]]])
    pred = model.predict(X)[0]
    df["ml_result"] = pred

    events = engine.process(df)

    # Returnar JSON
    return {
        "prediction": int(pred),
        "events": [
            {
                "rule": e.rule_name,
                "severity": e.severity,
                "timestamp": str(e.timestamp)
            } for e in events
        ]
    }
