# main.py
import time
import pandas as pd
from datetime import datetime
from core.rule import Rule
from core.engine import RuleEngine



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

temperaturas = [70,75,82,85,90,92,88, 43, 56, 22, 44, 99, 99, 99, 100, 100,100, 100, 100, 100, 50, 50, 50, 34, 100,100,100,100,100,100,100,100,100, 45, 64, 20, 20]
buffer=[]

window_seconds = 5
now = datetime.now()


for i in temperaturas:
    buffer.append({"temperatura": i, "timestamp": datetime.now()})
    buffer=[d for d in buffer
    if (now - d["timestamp"]).total_seconds() <= window_seconds]
    df = pd.DataFrame(buffer)
    events = engine.process(df)

    print(f"Temp: {i}")
    for event in events:
        print(f"{event}")

    time.sleep(1)    