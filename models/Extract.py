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
    data1 = [values]
    df1 = pd.DataFrame(data1)
    df1.to_csv(datos, index=None, mode="a", header=not os.path.isfile(datos))

def  get_matches(refTitle,matrix):
    match = difflib.get_close_matches(refTitle,matrix)
    if len(match)>0:
        match = match[0]
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
    # direct = os.path.dirname(__file__)
    # datos = os.path.join(direct,self._file) # Path completo de los datos
    # dataset = pd.read_csv(datos) # Leer los datos con Panda  
    headers = []
    values = []
    # buff = ''
    # for item in refMatrix:
    #     # header = get_matches(item,inMatrix)
    #     if (header in inMatrix) and (buff is not header):
    #         idx = inMatrix.index(header)
    #         buff = inMatrix[idx+1]
    #         headers.append(header)
    #         values.append(buff)
    match = get_matches("CODIGO DEL PRESTADOR",inMatrix)
    idx = inMatrix.index(match)
    del inMatrix[0:idx]
    for item in inMatrix:
        cnt = 0
        for i in item:
            if i.isupper():
                cnt += 1
        if len(item) > 0:
            rate = cnt/len(item)
            if rate > 0.3 and len(item) > 3:            
                headers.append(item)
            else:
                values.append(item)
    print(headers)
    print(values)
    return headers,values
