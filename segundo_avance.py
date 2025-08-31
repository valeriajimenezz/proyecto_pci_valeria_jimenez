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

    desglose = {
        "energía_no_renovable (kg CO2)": emisiones_energia_no_renovable,
        "combustibles (kg CO2)": emisiones_combustibles,
        "residuos (kg CO2)": emisiones_residuos,
        "total (ton CO2)": emisiones_totales_ton
    }

    print("\n Desglose de emisiones por fuente ")
    for fuente, valor in desglose.items():
        print(f"{fuente}: {valor:.2f}")

