# core/rule.py

from dataclasses import dataclass
from typing import Callable, List
import pandas as pd

@dataclass
class Rule:
    """
    Representa las reglas de las fallas

    Regla define:
    - Sensor involucrado
    - Condicion
    - Cuanto tiempo duro
    - El Grado de la falla
    """
    name: str
    sensores: List[str]
    condicion: Callable[[pd.DataFrame], bool]
    duration: int
    severidad: str

    def evaluar(self, data_window: pd.DataFrame) -> bool:
        """
        Evalua las condiciones dadas por la ventana deslizante
        """
        return self.condicion(data_window)