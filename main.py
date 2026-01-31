# main.py
import time
import pandas as pd
from core.rule import Rule
from core.engine import RuleEngine

def generar_data(temperatura):
    return pd.DataFrame({
        "temperatura": [temperatura]
    })


def high_temperatura_condicion(df:pd.DataFrame) -> bool:
    return df["temperatura"].iloc[-1] > 80

overheat_rule = Rule(
    name="Overheat",
    sensores=["temperatura"],
    condicion=high_temperatura_condicion,
    duration=5,
    severidad="HIGH"
)

engine = RuleEngine(rules=[overheat_rule])

temperaturas = [70,75,82,85,90,92,88, 43, 56, 22, 44, 99, 99, 99, 100, 100,100,100]

for i in temperaturas:
    df = generar_data(i)
    events = engine.process(df)

    print(f"Temp: {i}")
    for event in events:
        print(f"EVENT ->{event}")

    time.sleep(1)    