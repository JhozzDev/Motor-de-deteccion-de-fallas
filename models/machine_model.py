import pandas as pd # Manejo de datos
import numpy as np # Soporte numerico

from sklearn.ensemble import IsolationForest # Deteccion de anomalias
from sklearn.preprocessing import StandardScaler # Normalizar sensores

import joblib # Guardar modelo entrenado

df = pd.read_csv("data/temperaturas.csv")

features = ["temperaturas"]
X = df[features] # Datos elegidos

X = X.dropna()
X = X[X["temperaturas"] > 0] # Limpiar datos

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # Normalizar Datos

# Modelo
model = IsolationForest(

    n_estimators=1000, # Numero de arboles
    contamination=0.05, # Anomalias esperadas
    random_state=42, # resultados 
    bootstrap=True


) 

# Entrenar modelo
model.fit(X_scaled)

df["ml_result"] = model.predict(X_scaled) # Modelo detecta fallas

# Mapear DF para asignar referencia
df["ml_result"] = df["ml_result"].map({
    1: "Normal",
    -1: "Anomalia Detectada por ML"
})

print(df)

# Guardar Modelo
joblib.dump(model, "models/model_fallas.pkl")
joblib.dump(scaler, "models/scaler.pkl")

def decision(d, ml):
    if d > 90 and d<70:
        return "Falla"
    elif ml == -1:
        return "Advertencia ML"
    else:
        return "Normal"

