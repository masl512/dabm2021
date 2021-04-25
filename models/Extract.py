import difflib
import csv
import os
import pandas as pd

def create(headers,values):
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
            # row2=[item for item in row if len(item)>0]
            # # print(row2)
            # if len(row2)>0 :
            #     matriz.append(row2)
    match = get_matches("CODIGO DEL PRESTADOR",matriz)
    idx = matriz.index(match)
    del matriz[0:idx]
    return matriz

def extract(refMatrix,inMatrix):
    # direct = os.path.dirname(__file__)
    # datos = os.path.join(direct,self._file) # Path completo de los datos
    # dataset = pd.read_csv(datos) # Leer los datos con Panda  
    headers = []
    values = []
    buff = ''
    for item in refMatrix:
        header = get_matches(item,inMatrix)
        if (header in inMatrix) and (buff is not header):
            idx = inMatrix.index(header)
            buff = inMatrix[idx+1]
            headers.append(header)
            values.append(buff)
    print(headers)
    print(values)
    return headers,values


# matrix = ["OMedizar ", "FORMATO HOJA DE VIDA EQUIPO BIOMEDICO1.P.S. MEDILAFNIT: 901069028-1 ", 
# "FECHA", "04-01-2019", "ELABORO", "ING.BIOMEDICO", "VERSION", "", "CODIGO DELPRES TADOR", "9449002035 /-U1T", 
# "Cra 11A # 6-06", "", "SEDE", "Ocana", "96936032 - 3185381229", "", "VDISITINTIVO", " ", 
# "unidadcardiologicamedilaf@gmail.com ", "", "NOMBRE:", "", "rioU.", "Frimer piso.", "CODIGO DEL EQUIPO", 
# "", "AREA", "", "RS/ PC/", "", "MARCA:", "", "Cardiologia", "", "MODELO:", "", "", "SUBBUBICACION", "TIPO", 
# "", "", "", "EQUIPO FIJO", "", "No DE ACTIVO:", "", "EQUIPO MOVIL", "", "FURMA VE AUQIUISICION", "", 
# "ROVECUOR   ", "NO. VDOCUMENTO DE ADQUSICION", " ", "CORREO |Vistrimedicos ", "FECHA COMPRA", " ", 
# "CIUDAD. ", "FECHA VEINO |TALACION", "", "TTULAR   ", "FECHA DE OPERACION", " ", "CORREO ", 
# "FECHA DE VENCIMIENTO DE GARANTIA", " ", "CIUDAD. ", "FECHA FABRICACION", " ", " FABRICANTE —  ", 
# "No FACTURA", "", "", "", "", "9", "", "", "", "F.1e DE ALIMENTACION", " ", " ", " ", "RANGYO UC VOLIAJE", 
# "", "RANGO VE VELUUIDAUD", "2 ", "", " ", "PROOION", "", "KANG! ", "RANGO DE TEMPERATURA", " ", "", 
# "FRECUENCIA", "", "TEMPERATURA", "", "RANGO VDE POTENCIA", "  ", "RANGO VDE PESO", "", "CORRIENTE", "", 
# "VELOCIDAUD", "", "", "", "RANGO VDE LUMINOCIDAD", "", "rPUTENUIA ", "VLAPAULIVAU", "", "", "", 
# "", "", " ", "", " ", "_RIESGO D4725/05 —", "CLASIFICACION DE LA TECNOLOGIA ", "", "  ", " ", "", "", "", 
# " ", "", "", "", " ", "", "ITCUNUOLUGIA BAJA ", "", " ", "", "", "", " ", "", "", "ITCUNULUGIA ME! ", "", 
# "", "", "", " ", "", " ", "", "ITCUNULOGIA ALIA ", "", "", "", "", "", "", "", "", "", 
# "TECNOLOGIA PREDOMINANTE ", " ", "", "VY DIOMCVUICA |", "UBSERVACIONES Y RECOMENDACIONES", "", "", "", " ", 
# "VIA ", "", "", "", " ", "", " ", "TRALANIciN1U ¥ ", "", "", " ", "", "ANALIOlo (LABORA | ORIO CLINICO)", 
# "", "", "", "", "", "", " ", " ", "  ", " ", " ", " ", "", "", "", "", "", "", "", "", "", "", "", "", "", 
# "", "", "", "  ", "FERIDCIVDAD DE MANIENIMICNIO PREVENTIVO ©", "ISRACION      ", 
# " PROPIO GARANTIACONTRATADO IODATO ", "MENSUAL iz |BIMENSUAL ", "PERIODICIDAD", "STRAL ", ""]
