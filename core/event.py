# core/events.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """
    Representa el evento generado por el motor
    """

    timestamp: datetime
    rule_name:str
    severity:str
    message:str
    