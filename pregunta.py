# Limpieza de datos usando Pandas

import re
import pandas as pd
from datetime import datetime

def clean_data():
    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col = 0)
    
    # Eliminación de datos faltantes y duplicados
    df.dropna(axis = 0, inplace = True)
    df.drop_duplicates(inplace = True)

    # Poner en minúscula las columnas de tipo texto y eliminar carácteres especiales de idea_negocio y barrio
    for columna in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', 'barrio']:
        df[columna] = df[columna].str.lower()
        df[columna] = df[columna].apply(lambda x: x.replace('_', ' '))
        df[columna] = df[columna].apply(lambda x: x.replace('-', ' '))

    # Depurar la columna monto_del_credito quitando los carácteres extraños (No numéricos)
    df['monto_del_credito'] = df['monto_del_credito'].str.replace("\$[\s*]", "")
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(",", "")
    df['monto_del_credito'] = df['monto_del_credito'].str.replace("\.00", "")
    df['monto_del_credito'] = df['monto_del_credito'].astype(int)
    
    # Corregir tipo de dato de la columna comuna_ciudadano
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(float)

    # Corregir tipo de dato de la columna comuna_ciudadano -> Pasar a formato de fecha
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d") if (len(re.findall("^\d+/", x)[0]) - 1) == 4 else datetime.strptime(x, "%d/%m/%Y"))

    # Luego de depurar, se pueden haber generado duplicados, por lo que se eliminan de nuevo
    df.drop_duplicates(inplace = True)

    return df