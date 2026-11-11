# EnvíaYa — Calidad y mantenimiento del calculador de envíos

Repositorio del parcial 3 de Ingeniería de Software I (Grupo B1, VI semestre).
El sistema calcula el costo de cada envío de EnvíaYa (empresa de envíos de
Riohacha). El código heredado (`envios.py`, versión 1.0.0) fue escrito por un
desarrollador que ya no trabaja en la empresa y llegó con defectos, malas
prácticas y deuda técnica. Este repositorio documenta el proceso completo para
ponerlo en orden: requisitos, plan de pruebas, pruebas de caja negra y caja
blanca, automatización, corrección de defectos, refactorización, gestión de
configuración y una solicitud de cambio.

## Especificación propia (código 0182410133)

Últimos 6 dígitos del código: **A=4, B=1, C=0, D=1, E=3, F=3**

| Parámetro | Fórmula | Valor |
|-----------|---------|-------|
| PMAX | 30 + 5·A | 50 kg |
| L1 | 2 + (B mod 3) | 3 kg (D impar: el tramo 1 **no** incluye el límite) |
| L2 | 10 + C | 10 kg (incluido) |
| RR | 10 + 5·(E mod 4) | 25 % |
| RN | 40 + 5·(F mod 3) | 40 % |
| V | 10 + 5·(A mod 3) | 15 % |
| S | 2000 + 500·(C mod 4) | $2.000 |

Reglas según paridad:

- **D (impar):** tramo 1 es `peso < 3` (el límite no está incluido).
- **E (impar):** el recargo de fin de semana (+$2.000) se suma **después** de los descuentos.
- **B (impar):** se aplican ambos descuentos: primero el del cliente y luego el del cupón.
- **F (impar):** un cupón que no existe es un **error**.

Solicitud de cambio asignada (parte 8): `(A + F) mod 3 = 1` → **cliente
empresarial** (12 % de descuento; si el peso es mayor que L2, no se cobra el
recargo de zona).

## Estructura

```
envios.py            Código fuente (v1.0.0 heredado, v2.0.0 corregido y refactorizado)
tests/               Suite de pruebas automatizadas con pytest
docs/                Evidencias: capturas, grafo de flujo, UML
informe/             Informe del parcial (PDF)
CHANGELOG.md         Historial de cambios (Keep a Changelog)
```

## Cómo ejecutar las pruebas

```bash
python -m pytest tests/ -v
python -m pytest tests/ --cov=envios --cov-branch --cov-report=term-missing
```
