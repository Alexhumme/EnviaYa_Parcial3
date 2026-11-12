# -*- coding: utf-8 -*-
"""
envios.py — Cálculo del costo de envíos de EnvíaYa.

Especificación propia (código 0182410133):
    A=4, B=1, C=0, D=1, E=3, F=3

    PMAX = 50 kg
    L1 = 3 kg  (D impar: el tramo 1 NO incluye el límite; peso < 3)
    L2 = 10 kg (incluido)
    RR = 25 % (zona rural) · RN = 40 % (zona nacional)
    V  = 15 % (descuento VIP)
    S  = $2.000 (recargo de fin de semana, E impar: se suma DESPUÉS de los descuentos)
    B impar: se aplican AMBOS descuentos (primero el del cliente y luego el cupón)
    F impar: un cupón que no existe es un error (ValueError)

Versión 2.0.0: defectos corregidos y código refactorizado.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from math import isfinite

CONFIG = {
    "PMAX": 50,               # peso máximo permitido (kg)
    "L1": 3,                  # límite del tramo 1 (kg), no incluido (D impar)
    "L2": 10,                 # límite del tramo 2 (kg), incluido
    "RECARGO_RURAL": 0.25,    # RR
    "RECARGO_NACIONAL": 0.40, # RN
    "DESC_VIP": 0.15,         # V
    "RECARGO_FINDE": 2000,    # S, en pesos
}

TARIFA_TRAMO_1 = 6000        # peso < L1
TARIFA_TRAMO_2 = 9000        # L1 <= peso <= L2
RECARGO_KG_EXTRA = 800       # por cada kg sobre L2, proporcional
COSTO_MINIMO = 5000          # R8
DESC_FRECUENTE = 0.05
DESC_CUPON = 0.10
CUPON_VALIDO = "ENVIO10"
REDONDEO_BASIS = Decimal("100")


# ---------------------------------------------------------------- zonas
class EstrategiaZona(ABC):
    """Estrategia de recargo por zona. Cada zona decide cuánto recargar."""

    @abstractmethod
    def aplicar(self, subtotal):
        """Devuelve el subtotal con el recargo de la zona aplicado."""


class ZonaUrbana(EstrategiaZona):
    def aplicar(self, subtotal):
        return subtotal


class ZonaRural(EstrategiaZona):
    def aplicar(self, subtotal):
        return subtotal + subtotal * CONFIG["RECARGO_RURAL"]


class ZonaNacional(EstrategiaZona):
    def aplicar(self, subtotal):
        return subtotal + subtotal * CONFIG["RECARGO_NACIONAL"]


ESTRATEGIAS_ZONA = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# ------------------------------------------------------------ validación
def validar_peso(peso):
    if (not isinstance(peso, (int, float)) or isinstance(peso, bool)
            or not isfinite(peso) or peso <= 0 or peso > CONFIG["PMAX"]):
        raise ValueError("peso invalido")


def validar_zona(zona):
    if zona not in ESTRATEGIAS_ZONA:
        raise ValueError("zona invalida")


def validar_dia(dia):
    if not (isinstance(dia, (int, float)) and not isinstance(dia, bool)
            and float(dia).is_integer() and 1 <= dia <= 7):
        raise ValueError("dia invalido")


def validar_cupon(cupon):
    if cupon is not None and cupon != CUPON_VALIDO:
        raise ValueError("cupon no existe")  # F impar


# -------------------------------------------------------------- cálculo
def tarifa_por_peso(peso):
    if peso < CONFIG["L1"]:
        return TARIFA_TRAMO_1
    if peso <= CONFIG["L2"]:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * RECARGO_KG_EXTRA


def aplicar_recargo_zona(subtotal, zona):
    return ESTRATEGIAS_ZONA[zona].aplicar(subtotal)


def aplicar_descuentos(subtotal, cliente, cupon):
    # B impar: se aplican ambos (cliente primero y luego cupon)
    if cliente == "frecuente":
        subtotal -= subtotal * DESC_FRECUENTE
    elif cliente == "vip":
        subtotal -= subtotal * CONFIG["DESC_VIP"]
    if cupon == CUPON_VALIDO:
        subtotal -= subtotal * DESC_CUPON
    return subtotal


def aplicar_fin_de_semana(subtotal, dia):
    # E impar: se suma DESPUÉS de los descuentos
    if dia in (6, 7):
        subtotal += CONFIG["RECARGO_FINDE"]
    return subtotal


def redondear_100(valor):
    # R8: al múltiplo de $100 más cercano; los $50 redondean hacia arriba
    return int((Decimal(str(valor)) / REDONDEO_BASIS)
               .quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * 100


def calcular_costo(peso, zona, cliente, dia, cupon=None):
    """Calcula el costo de un envío según las reglas R1-R8. Devuelve pesos."""
    validar_peso(peso)
    validar_zona(zona)
    validar_dia(dia)
    validar_cupon(cupon)

    tarifa = tarifa_por_peso(peso)
    con_zona = aplicar_recargo_zona(tarifa, zona)
    con_descuentos = aplicar_descuentos(con_zona, cliente, cupon)
    con_finde = aplicar_fin_de_semana(con_descuentos, dia)

    costo = max(con_finde, COSTO_MINIMO)
    return redondear_100(costo)


# Alias de compatibilidad con la API heredada (calc). El parámetro flag
# se eliminó en v2.0.0; calc mantiene el orden (peso, zona, cliente, día, cupón).
calc = calcular_costo
