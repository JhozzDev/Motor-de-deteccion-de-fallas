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

        #Graba cuando una condicion comienza
        self.rule_start_times = {}
        self.rule_fired = {}

    def process(self, data_window:pd.DataFrame) ->List[Event]:
        events = []
        
        for rule in self.rules:

            now = datetime.now()
            condition_met = rule.evaluate(data_window)

            if condition_met:
                
                if rule.name not in self.rule_start_times:
                    self.rule_start_times[rule.name] = now
                    self.rule_fired[rule.name] = False
                elapsed = (now - self.rule_start_times[rule.name]).total_seconds()

                if elapsed>=rule.duration and not self.rule_fired[rule.name]:
                    event = Event(
                        timestamp=now.strftime("%H:%M:%S"),
                        rule_name=rule.name,
                        severity=rule.severity,
                        message=f"{rule.name}"
                    )
                    self.rule_fired[rule.name] = True
                    events.append(event)

            else:
                    if rule.name in self.rule_start_times:
                        del self.rule_start_times[rule.name]    
                    if rule.name in self.rule_fired:
                        del self.rule_fired[rule.name]
        return events            