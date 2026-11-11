# -*- coding: utf-8 -*-
"""
Suite de pruebas de caja negra para el calculador de envíos de EnvíaYa.

Los casos están derivados de la especificación propia (código 0182410133),
NO del código heredado. Cada caso trae el resultado esperado calculado a mano
(o con calculadora) a partir de las reglas R1-R8.

Técnicas usadas:
  PE = particiones de equivalencia
  VL = valores límite
  TD = tabla de decisión (cliente x cupón x fin de semana)
"""
import pytest

import envios

# (id, requisito, peso, zona, cliente, dia, cupon, esperado, tecnica)
CASOS = [
    ("CA-01", "R3", 2,    "urbana",   "normal",    2, None,      6000,  "PE"),
    ("CA-02", "R3", 2.5,  "urbana",   "normal",    2, None,      6000,  "PE"),
    ("CA-03", "R3", 2.99, "urbana",   "normal",    2, None,      6000,  "VL"),
    ("CA-04", "R3", 3,    "urbana",   "normal",    2, None,      9000,  "VL"),
    ("CA-05", "R3", 10,   "urbana",   "normal",    2, None,      9000,  "VL"),
    ("CA-06", "R3", 10.5, "urbana",   "normal",    2, None,      9400,  "VL"),
    ("CA-07", "R3", 12,   "urbana",   "normal",    2, None,      10600, "PE"),
    ("CA-08", "R3", 50,   "urbana",   "normal",    2, None,      41000, "VL"),
    ("CA-09", "R4", 4,    "rural",    "normal",    2, None,      11300, "PE"),
    ("CA-10", "R4", 4,    "nacional", "normal",    2, None,      12600, "PE"),
    ("CA-11", "R4", 12,   "rural",    "normal",    2, None,      13300, "PE"),
    ("CA-12", "R5", 4,    "urbana",   "normal",    6, None,      11000, "TD"),
    ("CA-13", "R5", 4,    "urbana",   "normal",    7, None,      11000, "TD"),
    ("CA-14", "R6", 4,    "urbana",   "frecuente", 2, None,      8600,  "TD"),
    ("CA-15", "R6", 4,    "urbana",   "vip",       2, None,      7700,  "TD"),
    ("CA-16", "R6", 4,    "urbana",   "normal",    2, "ENVIO10",  8100,  "TD"),
    ("CA-17", "R6", 4,    "urbana",   "vip",       2, "ENVIO10",  6900,  "TD"),
    ("CA-18", "R6", 4,    "urbana",   "frecuente", 2, "ENVIO10",  7700,  "TD"),
    ("CA-19", "R5", 4,    "urbana",   "vip",       6, None,      9700,  "TD"),
    ("CA-20", "R5", 4,    "urbana",   "vip",       6, "ENVIO10",  8900,  "TD"),
    ("CA-21", "R4", 4,    "rural",    "vip",       6, "ENVIO10",  10600, "TD"),
    ("CA-22", "R5", 4,    "urbana",   "frecuente", 6, None,      10600, "TD"),
    ("CA-23", "R8", 2,    "urbana",   "vip",       2, "ENVIO10",  5000,  "PE"),
    ("CA-24", "R1", 0,    "urbana",   "normal",    2, None,      None,  "PE"),
    ("CA-25", "R1", -1,   "urbana",   "normal",    2, None,      None,  "PE"),
    ("CA-26", "R1", 51,   "urbana",   "normal",    2, None,      None,  "PE"),
    ("CA-27", "R2", 4,    "insular",  "normal",    2, None,      None,  "PE"),
    ("CA-28", "R2", 4,    "urbana",   "normal",    0, None,      None,  "VL"),
    ("CA-29", "R2", 4,    "urbana",   "normal",    8, None,      None,  "VL"),
    ("CA-30", "R7", 4,    "urbana",   "normal",    2, "VERANO20", None,  "PE"),
    ("CA-31", "R4", 12,   "nacional", "vip",       7, "ENVIO10",  13400, "TD"),
    ("CA-32", "R5", 4,    "urbana",   "frecuente", 7, None,      10600, "TD"),
]

CASOS_OK = [c for c in CASOS if c[7] is not None]
CASOS_ERROR = [c for c in CASOS if c[7] is None]


@pytest.mark.parametrize(
    "cid, req, peso, zona, cliente, dia, cupon, esperado, tecnica",
    CASOS_OK,
    ids=[c[0] for c in CASOS_OK],
)
def test_costo_calculado(cid, req, peso, zona, cliente, dia, cupon, esperado, tecnica):
    assert envios.calc(peso, zona, cliente, dia, cupon) == esperado


@pytest.mark.parametrize(
    "cid, req, peso, zona, cliente, dia, cupon, esperado, tecnica",
    CASOS_ERROR,
    ids=[c[0] for c in CASOS_ERROR],
)
def test_entradas_invalidas(cid, req, peso, zona, cliente, dia, cupon, esperado, tecnica):
    with pytest.raises(ValueError):
        envios.calc(peso, zona, cliente, dia, cupon)
