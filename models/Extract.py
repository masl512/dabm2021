import difflib
import csv
import os
import pandas as pd

def createHeaders(headers,values):
    directorio = os.path.dirname(__file__)
    archivo =  r'..\data\hdvEquipos.csv'
    datos = os.path.join(directorio,archivo)   
    file = open(datos,"a")
    file.close()
    if os.stat(datos).st_size == 0:
        columnas =pd.DataFrame([headers])
        columnas.to_csv(datos, index=None, mode="a", header=not os.path.isfile(datos))
    df1 = pd.DataFrame([values])
    df1.to_csv(datos, index=None, mode="a", header=not os.path.isfile(datos))

def  get_matches(refTitle,matrix):
    flag = False
    match = difflib.get_close_matches(refTitle,matrix)
    if len(match)>0:
        match = match[0]
        flag = True
        return match


def readHV(fileName):
    matriz=[]
    with open(fileName) as File:
        reader = csv.reader(File, delimiter=';',skipinitialspace=True,
                            quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            for col in row:
                if len(col)>0:
                    matriz.append(col)
    match = get_matches("CODIGO DEL PRESTADOR",matriz)
    idx = matriz.index(match)
    del matriz[0:idx]
    return matriz

def extract(inMatrix):
    headers = [ h[0] for h in inMatrix if len(h[0])>2]
    values = [v[1] for v in inMatrix if len(v[0])>2]
    return headers,values
