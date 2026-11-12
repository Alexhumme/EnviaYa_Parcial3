# envios.py
'''
# DIGITOS
*código : 0182[410133]*
- 4 -> A 
- 1 -> B 
- 0 -> C 
- 1 -> D 
- 3 -> E 
- 3 -> F

# PARAMETROS
- *PMAX:* 30 + 5 * 4 = 50
- *L1:* 2 + ( 1 mod 3 ) = 3
- *L2:* 10 + 0 = 10
- *RR:* 10 + 5 * ( 3 mod 4 ) = 25
- *RN:* 40 + 5 * ( 3 mod 3 ) = 40
- *V:* 10 + 5 ( 4 mod 3 ) = 15
- *S:* 2000 + 500 * ( 0 mod 4 ) = 2000

# REGLAS
- D = 1 -> peso < 3
- E = 3 -> Se suma después de los descuentos
- B = 1 -> Se aplican ambos: primero el del cliente y luego el cupón 
- F = 3 -> Es error
'''
CONFIG = {
"L1": 3, # <- pon tus valores
"L2": 10,
"RECARGO_RURAL": 0.25, # como fracción, ej. 0.15
"RECARGO_NACIONAL": 0.4,
"DESC_VIP": 0.15,
"RECARGO_FINDE": 2000, # en pesos
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 50:
        raise ValueError("peso invalido")
    if z not in ("urbana", "rural", "nacional"):
        raise ValueError("zona invalida")  # R2
    if not (isinstance(d, (int, float)) and not isinstance(d, bool)
            and float(d).is_integer() and 1 <= d <= 7):
        raise ValueError("dia invalido")  # R2
    if p < CONFIG["L1"]:  # D impar: el tramo 1 no incluye el limite
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup is not None:
        if cup == "ENVIO10":
            t = t - t * 0.10
        else:
            raise ValueError("cupon no existe")  # F impar: error
    # fin de semana (E impar: el recargo se suma despues de los descuentos)
    if d >= 6:  # sabado y domingo son fin de semana
        t = t + CONFIG["RECARGO_FINDE"]
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(t / 100) * 100