import pandas as pd
import glob
import json
import os

archivos = glob.glob("data/*.xlsx")

consolidado = []

for archivo in archivos:
    df = pd.read_excel(archivo)

    # Validar columnas
    columnas_esperadas = ["Proyecto", "Fecha_Base", "Fecha_Proyectada"]
    if not all(col in df.columns for col in columnas_esperadas):
        continue

    df["Fecha_Base"] = pd.to_datetime(df["Fecha_Base"])
    df["Fecha_Proyectada"] = pd.to_datetime(df["Fecha_Proyectada"])

    df["Dias_Atraso"] = (
        df["Fecha_Proyectada"] - df["Fecha_Base"]
    ).dt.days

    # Agregar nombre del archivo como mes
    df["Fuente"] = os.path.basename(archivo)

    consolidado.extend(df.to_dict(orient="records"))

os.makedirs("data", exist_ok=True)

with open("data/consolidado.json", "w", encoding="utf-8") as f:
    json.dump(consolidado, f, default=str, indent=2)
