import os
import pandas as pd
import csv
from tabulate import tabulate
import numpy as np
matriz=[]
with open('HV_BENEHEART_D6.csv') as File:
    reader = csv.reader(File, delimiter=';',skipinitialspace=True,
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        row2=[item for item in row if len(item)>0]
        if row2:
            matriz.append(row2)

print(reader)

for i in range(len(matriz)):
    one=matriz[i]
    for j in range(len(one)):
        if one[j]=='x':
            print("hola")



"""
directorio=os.path.dirname(__file__)
archivo="HV_BENEHEART_D6.csv"
datos=os.path.join(directorio,archivo)
df = pd.read_csv(datos)
prin


def dispositivos():
    print("Lista de dispositivos")
    directorio = os.path.dirname(__file__)
    archivoDisp=os.path.join(directorio,"bd/dispositivos.csv")
    archivo =open(archivoDisp,"r")
    dispositivos = archivo.readlines()
    archivo.close()
    for d in dispositivos:
        datos=d.split(";")
        print(str(num)+"."+datos[0]+" "+datos[3])
        num+=1
    seleccion=int(input("Seleccione:"))
    archivo =open(archivoDisp,"r")
    dispositivos = archivo.readlines()
    archivo.close()
    
    num=1
    for d in dispositivos:
        datos=d.split(";")
        if num == seleccion:
            print("Acciones:")
            print(datos[1])
            provisional=datos
            guardat=num-1
            accion =input("Accion:").lower()
        num+=1
    actualizar=Dispositivo(provisional[0],provisional[1],provisional[2],provisional[3])
    actualizar.act(accion,guardat)



puerto= serial.Serial('COM5',9600)
puerto.close()
puerto.open()
suma=''
fecha2=''
for i in range (int(self.lecturas)):
    dato= puerto.readline().decode().strip()
    suma=str(dato)+"-"+str(suma)
    ahora = datetime.now()
    fecha = ahora.strftime("%Y/%m/%d %H:%M:%S")
    fecha2=str(fecha)+"-"+str(fecha2)

suma=suma.rstrip("-")
fecha2=fecha2.rstrip("-")
directorio=os.path.dirname(__file__)
archivo=self._file
datos=os.path.join(directorio,archivo)
df = pd.read_csv(datos)
df.loc[df['nombre'] == self.nombre, "datos"] = suma
df.to_csv(datos, index=False)
df.loc[df['nombre'] == self.nombre, "fecha"] = fecha2
df.to_csv(datos, index=False)
"""
 