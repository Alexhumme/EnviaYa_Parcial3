# -*- coding: utf-8 -*-
"""
Pruebas de la solicitud de cambio #1 (Parte 8):

    Nuevo tipo de cliente empresarial con un 12 % de descuento.
    Si el peso es mayor que L2, el recargo de zona no se cobra.

(Cambio asignado: (A + F) mod 3 = (4 + 3) mod 3 = 1)
"""
import envios


def test_empresarial_urbana_descuenta_12_porciento():
    assert envios.calc(4, "urbana", "empresarial", 2) == 7900


def test_empresarial_nacional_cobra_zona():
    assert envios.calc(4, "nacional", "empresarial", 2) == 11100


def test_empresarial_rural_cobra_zona():
    assert envios.calc(4, "rural", "empresarial", 2) == 9900


def test_empresarial_peso_igual_a_L2_no_exime_zona():
    # la exención aplica solo si el peso es MAYOR que L2
    assert envios.calc(10, "nacional", "empresarial", 2) == 11100


def test_empresarial_peso_mayor_que_L2_no_cobra_recargo_zona():
    assert envios.calc(10.5, "nacional", "empresarial", 2) == 8300
    assert envios.calc(12, "rural", "empresarial", 2) == 9300


def test_empresarial_combina_cupon_envio10():
    assert envios.calc(12, "rural", "empresarial", 2, "ENVIO10") == 8400


def test_empresarial_fin_de_semana_se_suma_despues_de_descuentos():
    assert envios.calc(4, "urbana", "empresarial", 6) == 9900


def test_empresarial_con_envio10_en_sabado():
    # 9000*0.88 = 7920; *0.9 = 7128; +2000 = 9128 -> 9100
    assert envios.calc(4, "urbana", "empresarial", 6, "ENVIO10") == 9100
