# core/engine.py
from datetime import datetime, timedelta
from typing import List
import pandas as pd
from core.rule import Rule
from core.event import Event

class RuleEngine:
    """
    Evalua las reglas sobre los datos y genera eventos
    """
    def __init__(self, rules: List[Rule]):
        self.rules = rules

        #Graba cuando una condicion se vuelve verdadera
        self.rule_start_times = {}

    def process(self, data_window:pd.DataFrame) ->List[Event]:
        events = []
        
        for rule in self.rules:

            now =datetime.now()
            condition_met = rule.evaluar(data_window)

            if condition_met:
                
                if rule.name not in self.rule_start_times:
                    self.rule_start_times[rule.name] = now
                elapsed = (now - self.rule_start_times[rule.name]).total_seconds()

                if elapsed>=rule.duration:
                    event = Event(
                        timestamp=now,
                        rule_name=rule.name,
                        severity=rule.severidad,
                        message=f"{rule.name}"
                    )
                    events.append(event)

            else:
                    if rule.name in self.rule_start_times:
                        del self.rule_start_times[rule.name]    
        return events            