import os
import pandas as pd
import numpy as np

# Carpeta donde están los Excel
CARPETA_DATA = "data"
ARCHIVO_SALIDA = os.path.join(CARPETA_DATA, "consolidado.json")

def obtener_excels(ruta):
    """
    Devuelve lista de archivos Excel válidos dentro de la carpeta.
    Ignora archivos temporales (~$).
    """
    archivos = []
    for archivo in os.listdir(ruta):
        if archivo.endswith(".xlsx") and not archivo.startswith("~$"):
            archivos.append(os.path.join(ruta, archivo))
    return archivos


def consolidar_excels(lista_archivos):
    """
    Lee y concatena todos los Excel en un solo DataFrame.
    """
    dataframes = []

    for archivo in lista_archivos:
        print(f"Procesando: {archivo}")
        df = pd.read_excel(archivo, engine="openpyxl")
        df["__archivo_origen"] = os.path.basename(archivo)
        dataframes.append(df)

    if not dataframes:
        raise ValueError("No se encontraron archivos Excel para procesar.")

    df_final = pd.concat(dataframes, ignore_index=True)

    return df_final


def limpiar_dataframe(df):
    """
    Limpia el DataFrame antes de exportar:
    - Convierte NaN a None (JSON válido)
    - Opcional: elimina filas completamente vacías
    """
    df = df.dropna(how="all")  # elimina filas totalmente vacías
    df = df.where(pd.notnull(df), None)  # NaN -> None
    return df


def exportar_json(df, ruta_salida):
    """
    Exporta el DataFrame a JSON válido.
    """
    df.to_json(
        ruta_salida,
        orient="records",
        force_ascii=False,
        indent=2
    )
    print(f"JSON generado en: {ruta_salida}")
    print(f"Registros exportados: {len(df)}")


def main():
    print("Iniciando consolidación...")

    excels = obtener_excels(CARPETA_DATA)
    print(f"Archivos encontrados: {len(excels)}")

    df_consolidado = consolidar_excels(excels)
    df_consolidado = limpiar_dataframe(df_consolidado)

    if len(df_consolidado) == 0:
        raise ValueError("El consolidado quedó vacío.")

    exportar_json(df_consolidado, ARCHIVO_SALIDA)

    print("Proceso finalizado correctamente.")


if __name__ == "__main__":
    main()
