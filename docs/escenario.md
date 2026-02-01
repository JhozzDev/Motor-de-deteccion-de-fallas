## Escenario - Sobrecalentamiento con baja presion

El sistema procesa senales provenientes de sensores
La data es continuamente analizada utilizando reglas establecidas

## Senales procesadas

-Temperatura

## Falla

A falla es considerada cuando

- La temperatura es mayor a 80C
- Permanece por 5s

## Comportamiento

IF temperatura > 80 
FOR 5 segundos
THEN genera evento critico

# Analisis

Dashboard con streamlit en una web local
