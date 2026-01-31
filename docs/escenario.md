## Escenario - Sobrecalentamiento con baja presion

El sistema procesa senales provenientes de sensores
La data es continuamente analizada utilizando reglas establecidas

## Senales procesadas

-Temperatura
-Presion

## Falla

A falla es considerada cuando

- La temperatura es mayor a 80C
- La presion es menor a 30
- Ambas permanecen por 5s

## Comportamiento

IF temperatura > 80 
AND presion < 30
FOR 5 segundos
THEN genera evento critico

## Secuencia de datos

| Tiempo  | Temperatura | Presion  |
|---------|-------------|----------|
| 0       | 70          | 40       |
| 1       | 85          | 28       |
| 2       | 88          | 26       |
| 3       | 90          | 25       |
| 4       | 92          | 24       |