# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [2.1.0] - 2026-11-11

### Añadido

- Nuevo tipo de cliente **empresarial** (`cliente="empresarial"`) con un
  descuento del 12 %.
- Si el peso es **mayor que L2** (10 kg), el recargo de zona
  **no se cobra** para clientes empresariales. La exención no aplica con peso
  igual a L2.
- Suite de pruebas `tests/test_empresarial.py` con 8 casos (escritos antes de
  implementar el cambio).

### Notas de la versión

Cambio **minor** (2.0.0 → 2.1.0): funcionalidad nueva y compatible hacia atrás;
los clientes existentes conservan exactamente el comportamiento de 2.0.0.

## [2.0.0] - 2026-11-11

### Cambiado

- **BREAKING:** se elimina el parámetro `flag` de la función de cálculo y se
  separa el cálculo de la presentación (ya no imprime "costo: ..."). El orden
  de los argumentos restantes se mantiene: `calc(peso, zona, cliente, día, cupón)`.
  `calc` queda como alias de `calcular_costo`.
- El recargo de fin de semana (+$2.000) ahora se suma **después** de los
  descuentos, como exige E (impar).
- El recargo de fin de semana aplica al **sábado** (día 6) y al domingo (día 7);
  antes solo aplicaba al domingo.
- El tramo 1 ya no incluye el límite L1: `peso < 3` (D impar).
- El redondeo del resultado pasa a ser al múltiplo de $100 **más cercano**, con
  los $50 redondeando hacia arriba (antes se truncaba).
- `envios.py` se refactoriza: funciones con una sola responsabilidad,
  constantes con nombre (`TARIFA_TRAMO_1`, `COSTO_MINIMO`, …), PMAX
  centralizado en `CONFIG` y patrón **Estrategia** para los recargos por zona
  (`ZonaUrbana`, `ZonaRural`, `ZonaNacional`).

### Corregido

- **DEF-01** (R3): el tramo 1 incluía el límite L1; con D impar el peso 3 kg
  debe cotizarse en el tramo 2.
- **DEF-02** (R5): el recargo de fin de semana solo aplicaba al domingo
  (`d > 6`); ahora incluye el sábado (`d >= 6`).
- **DEF-03** (R5): el recargo de fin de semana se aplicaba **antes** de los
  descuentos; E impar exige aplicarlo **después**.
- **DEF-04** (R7): un cupón que no existe se ignoraba silenciosamente; F
  impar exige lanzar `ValueError`.
- **DEF-05** (R2): no se validaba zona ni día; ahora una zona fuera de
  `{urbana, rural, nacional}` o un día fuera de 1–7 lanzan `ValueError`.
- **DEF-06** (R8): el resultado se redondeaba truncando (`int(t/100)*100`);
  ahora redondea al múltiplo de $100 más cercano, $50 hacia arriba.

### Añadido

- Patrón Estrategia para las zonas y validación de entradas centralizada.
- PMAX = 50 en `CONFIG` (antes el 50 estaba quemado en la condición del peso).

### Eliminado

- Parámetro `flag` y el `print` dentro de la función de cálculo.

### Notas de la versión

Cambio **major** (1.0.0 → 2.0.0): quitar el parámetro `flag` rompe el contrato
de la función (cualquier llamada `calc(p, z, c, d, cup, True)` deja de ser
válida), por lo que corresponde un incremento de versión mayor según
versionado semántico. Los cambios de comportamiento restantes son correcciones
a bugs, pero viajan en la misma major porque la interfaz cambió.

## [1.0.0] - 2026-11-11

### Añadido

- Versión heredada importada tal como la dejó el desarrollador anterior:
  función `calc(p, z, c, d, cup=None, flag=False)` con el `CONFIG` propio del
  estudiante (A=4, B=1, C=0, D=1, E=3, F=3).
