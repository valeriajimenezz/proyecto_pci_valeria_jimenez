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

hallazgos: list[Finding] = []


def Limites():
    porcentaje_renovable_min: float
    kwh_por_empleado_max: float
    tasa_de_incidentes_max: float
    residuos_por_empleado_max: float


def Indicadores():
    empresa: str
    consumo_energia_kwh_anual: float
    porcentaje_energia_renovable: float
    consumo_combustibles_kg_anual: float
    residuos_kg_anual: float
    consumo_agua_m3_anual: float
    empleados: int
    incidentes_anual: int
    dias_sin_incidentes: int
    capacitaciones_anuales: int

    def kwh_renovable(self):
        return self.consumo_energia_kwh_anual * (self.porcentaje_energia_renovable / 100)

    def kwh_no_renovable(self):
        return self.consumo_energia_kwh_anual - self.kwh_renovable()

    def tasa_de_incidentes(self):
        if self.empleados == 0:
            return 0
        return (self.incidentes_anual / max(self.empleados, 1)) * 100.0


Finding = Tuple[str, str, Dict[str, float]]


def diagnostico(ind):
    if ind.porcentaje_renovable < ind.Limites.porcentaje_renovable_min:
        hallazgos.append(("dependencia_focil", f"% renovable({ind.porcentaje_renovable:.1f}%) < ({ind.Limites.porcentaje_renovable_min:.1f}%)",
                          {
                              "%_renovable": ind.porcentaje_renovable,
                              "limite_%_renovable": ind.Limites.porcentaje_renovable_min
        }
        ))
# CREAR lista de soluciones por área:
#        - Paneles solares
#        - Iluminación LED
#        - Optimización procesos
#        - Electrificación flotilla
#        - Reciclaje/compostaje
#        - Capacitaciones seguridad
#    PARA cada solución:
#        Estimar impacto, coste, tiempo y dificultad
