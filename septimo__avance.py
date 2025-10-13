from typing import Dict
from dataclasses import dataclass, asdict

base_datos_empresas = []


# 1. RECEPCIÓN DE DATOS
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

    registro_matriz = [
        ["empresa", empresa],
        ["indicador_energia", indicador_energia],
        ["indicador_renovable", indicador_renovable],
        ["indicador_combustibles", indicador_combustibles],
        ["indicador_residuos", indicador_residuos],
        ["indicador_agua", indicador_agua],
        ["indicador_empleados", indicador_empleados],
        ["indicador_accidentes", indicador_accidentes],
        ["indicador_dias_sin_incidentes", indicador_dias_sin_incidentes],
        ["indicador_capacitaciones", indicador_capacitaciones],
    ]

    base_datos_empresas.append(registro_matriz)

    print(f"\n Empresa '{empresa}' registrada correctamente.")
    return registro_matriz


# 2. FUNCIONES DE CÁLCULO DE INDICADORES
def construir_indicadores(datos):
    return {
        "empresa": datos[0][1],
        "energia_kwh": datos[1][1],
        "%renovable": datos[2][1],
        "combustibles_kg": datos[3][1],
        "residuos_kg": datos[4][1],
        "agua_m3": datos[5][1],
        "empleados": datos[6][1],
        "incidentes": datos[7][1],
        "dias_sin_incidentes": datos[8][1],
        "capacitaciones": datos[9][1],
    }


def kwh_por_empleado(ind):
    if ind[6][1] <= 0:
        return float("inf")
    return ind[1][1] / ind[6][1]


def tasa_incidentes(ind):
    if ind[6][1] <= 0:
        return 0.0
    return (ind[7][1] / ind[6][1]) * 100.0


def residuos_por_empleado(ind):
    if ind[6][1] <= 0:
        return float("inf")
    return ind[4][1] / ind[6][1]


# 3. SOLUCIONES BASE
def generar_soluciones_base():
    return [
        {"codigo": "paneles_solares", "nombre": "Paneles solares", "tipo": "energia",
         "%energia": 0.30, "capex_mxn": 300000, "meses": 6, "dificultad": 4, "seguridad": 4},
        {"codigo": "iluminacion_led", "nombre": "Iluminación LED", "tipo": "energia",
         "%energia": 0.10, "capex_mxn": 80000, "meses": 2, "dificultad": 2, "seguridad": 5},
        {"codigo": "optimizacion_procesos", "nombre": "Optimización procesos", "tipo": "energia",
         "%energia": 0.05, "capex_mxn": 30000, "meses": 3, "dificultad": 3, "seguridad": 5},
        {"codigo": "electrificacion_flot", "nombre": "Electrificación flotilla", "tipo": "combustible",
         "%combustibles": 0.40, "capex_mxn": 600000, "meses": 12, "dificultad": 5, "seguridad": 5},
        {"codigo": "reciclaje_compostaje", "nombre": "Reciclaje/compostaje", "tipo": "residuos",
         "%residuos": 0.25, "capex_mxn": 20000, "meses": 2, "dificultad": 2, "seguridad": 4},
        {"codigo": "capacitaciones_seg", "nombre": "Capacitaciones seguridad", "tipo": "seguridad",
         "%incidentes": 0.40, "capex_mxn": 15000, "meses": 1, "dificultad": 1, "seguridad": 5},
    ]


# 4. ESTIMACIÓN ECONÓMICA
def estimar_impacto_y_economia(sol, ind, precio_kwh, factores):
    energia_ahorrada = 0.0
    co2_ev_kg = 0.0
    ahorro_operativo = 0.0

    fraccion_no_renovable = 1.0 - (ind[2][1] / 100.0)

    if sol["tipo"] == "energia":
        energia_ahorrada = sol.get("%energia", 0.0) * ind[1][1]
        co2_ev_kg += energia_ahorrada * \
            factores["factor_emision_energia_no_renovable"] * \
            fraccion_no_renovable

    elif sol["tipo"] == "combustible":
        combustibles_ahorrados = sol.get(
            "%combustibles", 0.0) * ind[3][1]
        co2_ev_kg += combustibles_ahorrados * \
            factores["factor_emision_combustibles"]

    elif sol["tipo"] == "residuos":
        residuos_ev = sol.get("%residuos", 0.0) * ind[4][1]
        co2_ev_kg += residuos_ev * factores["factor_emision_residuos"]

    ahorro_anual = energia_ahorrada * precio_kwh + ahorro_operativo
    capex = sol["capex_mxn"]
    payback = None if ahorro_anual <= 0 else (capex / ahorro_anual)
    costo_por_ton = capex / \
        (co2_ev_kg / 1000.0) if co2_ev_kg > 0 else float("inf")

    res = dict(sol)
    res.update({
        "energia_ahorrada_kwh": energia_ahorrada,
        "co2_ev_kg": co2_ev_kg,
        "ahorro_anual_mxn": ahorro_anual,
        "payback_anios": payback,
        "costo_por_ton_mxn": costo_por_ton,
    })
    return res


# 5. PRIORIZACIÓN DE SOLUCIONES
def normalizar_0a1(valor, vmin, vmax, invertido=False):
    if (vmax - vmin) == 0:
        return 1.0
    x = (valor - vmin) / (vmax - vmin)
    if invertido:
        x = 1.0 - x
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
    costos_validos = [s["costo_por_ton_mxn"]
                      for s in soluciones_estimadas if s["costo_por_ton_mxn"] != float("inf")]
    cmin, cmax = (min(costos_validos), max(costos_validos)
                  ) if costos_validos else (0.0, 1.0)

    priorizadas = []
    for s in soluciones_estimadas:
        costo_score = normalizar_0a1(
            s["costo_por_ton_mxn"], cmin, cmax, invertido=True)
        facilidad = (6 - s["dificultad"]) / 5.0
        seguridad_norm = s["seguridad"] / 5.0
        puntuacion = 0.6 * costo_score + 0.2 * facilidad + 0.2 * seguridad_norm
        item = dict(s)
        item["puntuacion"] = puntuacion
        item["bucket"] = clasificar_bucket(s)
        priorizadas.append(item)

    priorizadas.sort(key=lambda x: x["puntuacion"], reverse=True)
    return priorizadas


# 6. MENÚ PRINCIPAL
def menu():
    print("\n=== Menú Principal ===")
    print("1. Registrar nueva empresa")
    print("2. Ver métricas de una empresa")
    print("3. Ver soluciones base")
    print("4. Estimación económica")
    print("5. Priorizar soluciones")
    print("6. Ver base de datos completa")
    print("0. Salir")
    return int(input("Seleccione una opción: "))


# 7. BUCLE PRINCIPAL
soluciones_base = generar_soluciones_base()

while True:
    opcion = menu()

    if opcion == 1:
        entrada_de_datos()

    elif opcion == 2:
        if not base_datos_empresas:
            print("No hay empresas registradas.")
        else:
            for i, e in enumerate(base_datos_empresas, 1):
                print(f"{i}. {e[0][1]}")
            sel = int(input("Seleccione la empresa: ")) - 1
            datos = base_datos_empresas[sel]
            ind = construir_indicadores(datos)
            print(f"\n--- Métricas de {datos[0][1]} ---")
            print(f"- kWh por empleado: {kwh_por_empleado(datos):.3f}")
            print(f"- Tasa de incidentes: {tasa_incidentes(datos):.3f}%")
            print(f"- Residuos por empleado: {residuos_por_empleado(datos):.3f} kg")

    elif opcion == 3:
        print("\nSoluciones base:")
        for sol in soluciones_base:
            print(f"- {sol['nombre']} (Tipo: {sol['tipo']})")

    elif opcion == 4:
        if not base_datos_empresas:
            print("Registre una empresa primero.")
        else:
            datos = base_datos_empresas[-1]
            ind = construir_indicadores(datos)
            precio_kwh = float(input("Precio electricidad (MXN/kWh): "))
            factores = {
                "factor_emision_energia_no_renovable": float(input("Factor energía no renovable (kg CO2/kWh): ")),
                "factor_emision_combustibles": float(input("Factor combustibles (kg CO2/kg): ")),
                "factor_emision_residuos": float(input("Factor residuos (kg CO2/kg): "))
            }
            resultados = [
                estimar_impacto_y_economia(sol, ind, precio_kwh, factores)
                for sol in soluciones_base
            ]
            print("\nEstimaciones económicas generadas.")

    elif opcion == 5:
        print("\nPriorización de soluciones")
        ranking = priorizar(soluciones_base)
        for s in ranking:
            print(
                f"- {s['nombre']} | Punt: {s['puntuacion']:.2f} | Bucket: {s['bucket']}")

    elif opcion == 6:
        print("\nEmpresas registradas:")
        if not base_datos_empresas:
            print("No hay registros todavía.")
        else:
            for i, emp in enumerate(base_datos_empresas, 1):
                print(
                    f"{i}. {emp[1][1]} - Energía: {emp[2][1]} kWh/año, Renovable: {emp[3][1]}%")

    elif opcion == 0:
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida, intente de nuevo.")
