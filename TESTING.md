# Testing Fest

## Pruebas unitarias
- Validación de mensajes
- Gestión de clientes
- Retransmisión

## TDD
- RED
- GREEN
- REFACTOR

## Integración
- Múltiples conexiones
- Broadcast
- No duplicación
- Orden

## Desconexiones
- Un cliente
- Múltiples clientes
- Nueva conexión

## Resultados
20/20 pruebas exitosas

## Coverage
80%

# ------------  SEGUNDO INFORME    ---------------------

## Resultados de las pruebas

Se ejecutaron un total de 20 pruebas automatizadas.

Resultado:

- 20 pruebas exitosas.
- 0 pruebas fallidas.
- 0 errores.
- Tiempo de ejecución aproximado: 2.46 segundos.

### Cobertura

La cobertura obtenida fue del 80%.

| Archivo | Cobertura |
|---|---:|
| chat/validation.py | 100% |
| server.py | 89% |
| client.py | 0% |
| Total | 80% |

El archivo `client.py` no fue incluido en las pruebas de integración actuales debido a que contiene interacción directa con la consola mediante `input()` y un bucle de ejecución continuo.

El servidor obtuvo un 89% de cobertura y las funciones de validación alcanzaron un 100%.





##
comando para html: 
start htmlcov\index.html