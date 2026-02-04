import time
import pandas as pd
import requests

from core.engine import RuleEngine
from core.rule import Rule

API_URL = "http://127.0.0.1:8000/process"

data = {
    "temperature": 100,
    "pressure": 100
}

response = requests.post(API_URL, json=data, timeout=3)
response.raise_for_status()
result = response.json()

def temperature_condition(df: pd.DataFrame):
    return df["temperature"].iloc[-1] > 80

rule = Rule(
        name="OverHeat",
        sensors=["temperature"],
        condition=temperature_condition,
        duration=2,
        severity="HIGH"
    )

regla = Rule(
        name="Overheat",
        sensors=["temperature"],
        condition=temperature_condition,
        duration=1,
        severity="HIGH"
    )

def test_dont_Throw():

    engine = RuleEngine([rule])

    buffer = []
    buffer.append({"temperature": 85})
    df = pd.DataFrame(buffer)

    events = engine.process(df)

    assert len(events) == 0

def test_Throw():
 
    engine = RuleEngine([regla])

    buffer = []

    buffer.append({"temperature": 85})
    df = pd.DataFrame(buffer)

    engine.process(df)
    time.sleep(1)

    eventos = engine.process(df)

    assert len(eventos) == 1
    assert eventos[0].rule_name == "Overheat"

