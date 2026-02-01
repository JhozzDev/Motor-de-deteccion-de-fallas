import time
import pandas as pd

from core.engine import RuleEngine
from core.rule import Rule

def temperature_condition(df: pd.DataFrame):
    return df["temperature"].iloc[-1] > 80

def test_dont_Throw():
    rule = Rule(
        name="OverHeat",
        sensors=["temperature"],
        condition=temperature_condition,
        duration=2,
        severity="HIGH"
    )

    engine = RuleEngine([rule])

    buffer = []
    buffer.append({"temperature": 85})
    df = pd.DataFrame(buffer)

    events = engine.process(df)

    assert len(events) == 0

def test_dispara_cuando_cumple_duracion():
    regla = Rule(
        name="Sobrecalentamiento",
        sensors=["temperature"],
        condition=temperature_condition,
        duration=1,
        severity="ALTA"
    )

    engine = RuleEngine([regla])

    buffer = []

    buffer.append({"temperature": 85})
    df = pd.DataFrame(buffer)

    engine.process(df)
    time.sleep(1)

    eventos = engine.process(df)

    assert len(eventos) == 1
    assert eventos[0].rule_name == "Sobrecalentamiento"

