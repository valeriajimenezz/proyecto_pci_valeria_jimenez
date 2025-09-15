# 1. RECEPCIÓN DE DATOS
from typing import Tuple, Dict
from dataclasses import dataclass, asdict


def entrada_de_datos():
    empresa = input("Ingrese el nombre de la empresa: ")
    indicador_energia = float(
        input("Ingrese el consumo de energía en kWh/año: "))
    indicador_renovable = float(
        input("Ingrese el porcentaje de energía renovable (%): "))

    if indicador_renovable < 0 or indicador_renovable > 100:
        print("Error: el porcentaje renovable debe estar entre 0 y 100.")
        return None

    indicador_combustibles = float(
        input("Ingrese el consumo de combustibles en kg/año: "))
    indicador_residuos = float(
        input("Ingrese la generación de residuos en kg/año: "))
    indicador_agua = float(input("Ingrese el consumo de agua en m³/año: "))
    indicador_empleados = int(input("Ingrese el número de empleados: "))
    indicador_accidentes = int(
        input("Ingrese el número de accidentes en el periodo: "))
    indicador_dias_sin_incidentes = int(
        input("Ingrese los días sin incidentes: "))
    indicador_capacitaciones = int(
        input("Ingrese el número de capacitaciones realizadas: "))

    return {
        "empresa": empresa,
        "indicador_energia": indicador_energia,
        "indicador_renovable": indicador_renovable,
        "indicador_combustibles": indicador_combustibles,
        "indicador_residuos": indicador_residuos,
        "indicador_agua": indicador_agua,
        "indicador_empleados": indicador_empleados,
        "indicador_accidentes": indicador_accidentes,
        "indicador_dias_sin_incidentes": indicador_dias_sin_incidentes,
        "indicador_capacitaciones": indicador_capacitaciones
    }


# 2. PROCESAMIENTO DE DATOS
datos = entrada_de_datos()

if datos is not None:
    kWh_renovable = datos["indicador_energia"] * \
        (datos["indicador_renovable"] / 100)
    kWh_no_renovable = datos["indicador_energia"] - kWh_renovable

    factor_emision_energia_no_renovable = float(
        input("Ingrese el factor de emisión de energía no renovable (kg CO2/kWh): "))
    factor_emision_combustibles = float(
        input("Ingrese el factor de emisión de combustibles (kg CO2/kg): "))
    factor_emision_residuos = float(
        input("Ingrese el factor de emisión de residuos (kg CO2/kg): "))

    emisiones_energia_no_renovable = kWh_no_renovable * \
        factor_emision_energia_no_renovable
    emisiones_combustibles = datos["indicador_combustibles"] * \
        factor_emision_combustibles
    emisiones_residuos = datos["indicador_residuos"] * factor_emision_residuos

    emisiones_totales_kg = (
        emisiones_energia_no_renovable +
        emisiones_combustibles +
        emisiones_residuos
    )

    emisiones_totales_ton = emisiones_totales_kg / 1000

    def desglose_emisiones():
        return {
            "energía_no_renovable (kg CO2)": emisiones_energia_no_renovable,
            "combustibles (kg CO2)": emisiones_combustibles,
            "residuos (kg CO2)": emisiones_residuos,
            "total (ton CO2)": emisiones_totales_ton
        }

    print("\n Desglose de emisiones por fuente")
    for fuente, valor in desglose_emisiones().items():
        print(f"{fuente}: {valor:.2f}"
              )
# DIAGNÓSTICO


def Limites():
    porcentaje_renovable_min: float
    kwh_por_empleado_max: float
    tasa_de_incidentes_max: float
    residuos_por_empleado_max: float


def construir_indicadores(datos):
    return {
        "empresa": datos["empresa"],
        "energia_kwh": datos["indicador_energia"],
        "%renovable": datos["indicador_renovable"],
        "combustibles_kg": datos["indicador_combustibles"],
        "residuos_kg": datos["indicador_residuos"],
        "agua_m3": datos["indicador_agua"],
        "empleados": datos["indicador_empleados"],
        "incidentes": datos["indicador_accidentes"],
        "dias_sin_incidentes": datos["indicador_dias_sin_incidentes"],
        "capacitaciones": datos["indicador_capacitaciones"],
    }


def kwh_por_empleado(ind):
    if ind["empleados"] <= 0:
        return float("inf")
    return ind["energia_kwh"] / ind["empleados"]


def tasa_incidentes(ind):
    if ind["empleados"] <= 0:
        return 0.0
    return (ind["incidentes"] / ind["empleados"]) * 100.0


def residuos_por_empleado(ind):
    if ind["empleados"] <= 0:
        return float("inf")
    return ind["residuos_kg"] / ind["empleados"]


if datos is not None:
    ind = construir_indicadores(datos)
    print("\nMétricas clave:")
    print(f"- kWh por empleado: {kwh_por_empleado(ind):.2f}")
    print(f"- Tasa de incidentes (%): {tasa_incidentes(ind):.2f}")
    print(f"- Residuos por empleado (kg): {residuos_por_empleado(ind):.2f}")


#  7. SOLUCIONES PREDEFINIDAS
# Lista base
def generar_soluciones_base():
    return [
        {"codigo": "paneles_solares",        "nombre": "Paneles solares",        "tipo": "energia",
            "%energia": 0.30, "capex_mxn": 300000, "meses": 6,  "dificultad": 4, "seguridad": 4},
        {"codigo": "iluminacion_led",        "nombre": "Iluminación LED",        "tipo": "energia",
            "%energia": 0.10, "capex_mxn":  80000, "meses": 2,  "dificultad": 2, "seguridad": 5},
        {"codigo": "optimizacion_procesos",  "nombre": "Optimización procesos",  "tipo": "energia",
            "%energia": 0.05, "capex_mxn":  30000, "meses": 3,  "dificultad": 3, "seguridad": 5},
        {"codigo": "electrificacion_flot",   "nombre": "Electrificación flotilla", "tipo": "combustible",
            "%combustibles": 0.40, "capex_mxn": 600000, "meses": 12, "dificultad": 5, "seguridad": 5},
        {"codigo": "reciclaje_compostaje",   "nombre": "Reciclaje/compostaje",   "tipo": "residuos",
            "%residuos": 0.25, "capex_mxn": 20000, "meses": 2,  "dificultad": 2, "seguridad": 4},
        {"codigo": "capacitaciones_seg",     "nombre": "Capacitaciones seguridad", "tipo": "seguridad",
            "%incidentes": 0.40, "capex_mxn": 15000, "meses": 1,  "dificultad": 1, "seguridad": 5},
    ]

#   8. ESTIMACIÓN ECONÓMICA
# ahorro_anual = energía_ahorrada * precio_kWh + ahorro_operativo
# años_recuperación = costo_inicial / ahorro_anual (si ahorro > 0)


def estimar_impacto_y_economia(sol, ind, precio_kwh, factores):
    energia_ahorrada = 0.0  # kWh/año
    co2_ev_kg = 0.0
    ahorro_operativo = 0.0  # MXN/año

    fraccion_no_renovable = 1.0 - (ind["%renovable"] / 100.0)

    if sol["tipo"] == "energia":
        energia_ahorrada = sol.get("%energia", 0.0) * ind["energia_kwh"]
        co2_ev_kg += energia_ahorrada * \
            factores["factor_emision_energia_no_renovable"] * \
            fraccion_no_renovable

    elif sol["tipo"] == "combustible":
        combustibles_ahorrados = sol.get(
            "%combustibles", 0.0) * ind["combustibles_kg"]
        co2_ev_kg += combustibles_ahorrados * \
            factores["factor_emision_combustibles"]

    elif sol["tipo"] == "residuos":
        residuos_ev = sol.get("%residuos", 0.0) * ind["residuos_kg"]
        co2_ev_kg += residuos_ev * factores["factor_emision_residuos"]

    ahorro_anual = energia_ahorrada * precio_kwh + ahorro_operativo
    capex = sol["capex_mxn"]
    payback = None if ahorro_anual <= 0 else (capex / ahorro_anual)

    # Costo por tonelada evitada
    if co2_ev_kg > 0:
        costo_por_ton = capex / (co2_ev_kg / 1000.0)  # MXN por tonelada
    else:
        costo_por_ton = float("inf")

    res = dict(sol)
    res.update({
        "energia_ahorrada_kwh": energia_ahorrada,
        "co2_ev_kg": co2_ev_kg,
        "ahorro_anual_mxn": ahorro_anual,
        "payback_anios": payback,
        "costo_por_ton_mxn": costo_por_ton,
    })
    return res

# ===== 9. PRIORIZACIÓN =====


def normalizar_0a1(valor, vmin, vmax, invertido=False):
    if (vmax - vmin) == 0:
        return 1.0
    x = (valor - vmin) / (vmax - vmin)
    if invertido:  # si menor es mejor
        x = 1.0 - x
    # limitar por si hay inf o fuera de rango
    if x != x:  # NaN
        return 0.0
    if x == float("inf") or x == -float("inf"):
        return 0.0
    return max(0.0, min(1.0, x))


def clasificar_bucket(sol):
    pb = sol["payback_anios"]
    dif = sol["dificultad"]
    if pb is not None and pb <= 2 and dif <= 2:
        return "Quick win"
    elif pb is not None and pb <= 4:
        return "Inversión media"
    else:
        return "Estratégica"


def priorizar(soluciones_estimadas):
    # Tomamos costos por tonelada válidos para normalizar
    costos_validos = [s["costo_por_ton_mxn"]
                      for s in soluciones_estimadas if s["costo_por_ton_mxn"] != float("inf")]
    if len(costos_validos) == 0:
        cmin = 0.0
        cmax = 1.0
    else:
        cmin = min(costos_validos)
        cmax = max(costos_validos)

    priorizadas = []
    for s in soluciones_estimadas:
        # 0.6 costo-eficacia (menor costo/ton es mejor)
        costo_score = normalizar_0a1(s["costo_por_ton_mxn"], cmin, cmax,
                                     invertido=True) if s["costo_por_ton_mxn"] != float("inf") else 0.0
        # 0.2 facilidad (menor dificultad es mejor). dificultad 1..5 -> facilidad = (6 - d)/5
        facilidad = (6 - s["dificultad"]) / 5.0
        # 0.2 seguridad (1..5) -> 0..1
        seguridad_norm = s["seguridad"] / 5.0

        puntuacion = 0.6 * costo_score + 0.2 * facilidad + 0.2 * seguridad_norm
        item = dict(s)
        item["puntuacion"] = puntuacion
        item["bucket"] = clasificar_bucket(s)
        priorizadas.append(item)

    priorizadas.sort(key=lambda x: x["puntuacion"], reverse=True)
    return priorizadas


# ===== Integración de 7–9 =====
if datos is not None:
    # Ya tienes estos factores de arriba cuando pediste inputs:
    factores = {
        "factor_emision_energia_no_renovable": factor_emision_energia_no_renovable,
        "factor_emision_combustibles": factor_emision_combustibles,
        "factor_emision_residuos": factor_emision_residuos
    }

    # Precio de la electricidad para ahorrar (MXN/kWh)
    precio_kwh = float(
        input("Ingresa el precio de la electricidad (MXN/kWh): "))

    soluciones_base = generar_soluciones_base()

    soluciones_estimadas = []
    for sol in soluciones_base:
        est = estimar_impacto_y_economia(sol, ind, precio_kwh, factores)
        soluciones_estimadas.append(est)

    ranking = priorizar(soluciones_estimadas)

    print("\n=== Priorización de soluciones (top → bottom) ===")
    for s in ranking:
        payback_txt = "N/A" if s["payback_anios"] is None else f"{s['payback_anios']:.1f} años"
        co2_t = s["co2_ev_kg"] / 1000.0
        costo_t = "∞" if s["costo_por_ton_mxn"] == float(
            "inf") else f"${s['costo_por_ton_mxn']:,.0f}/t"
        print(f"- {s['nombre']} | Punt: {s['puntuacion']:.2f} | Bucket: {s['bucket']} | CAPEX: ${s['capex_mxn']:,.0f} | Ahorro/año: ${s['ahorro_anual_mxn']:,.0f} | Payback: {payback_txt} | CO2 evitado: {co2_t:.2f} t | Costo/ton: {costo_t}")
