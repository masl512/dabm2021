import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
import pandas as pd

class Estadistica():
    def __init__(self,_file):
        self._file=_file
    def general(self):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        file = open(datos,"a")
        file.close()
        df = pd.read_csv(datos)
        nume=df.to_numpy()
        valores = [nume[0][0],nume[0][1],nume[0][2]]
        headers = ['En mantenimiento','Disponibles','Fuera de Servicio']
        estGen = [headers,valores]
        # mantenimiento, disponibles, fuera de servicio
        return estGen

    def ind(self,numer):
        directorio = os.path.dirname(__file__)
        archivoUsuarios=os.path.join(directorio,self._file)
        file = open(archivoUsuarios,"a")
        file.close()
        df = pd.read_csv(archivoUsuarios)
        a=df[(df['n_act'] == numer)]
        print(a)
        nume=a.to_numpy()
        fechaN=nume[0][1]
        arr = fechaN.split('-')
        fecha2 = datetime(int(arr[2]),int(arr[1]),int(arr[0]))
        tipoMant = nume[0][2]
        tipoMant = tipoMant.lower()
        if tipoMant =="mensual":
            diferencia = fecha2 + timedelta(days=30)
        elif tipoMant=="bimestral":
            diferencia = fecha2 + timedelta(days=15)
        elif tipoMant=="trimestral":
            diferencia = fecha2 + timedelta(days=90)
        else:
            diferencia = fecha2 + timedelta(days=180)
        today = datetime.today()
        remaining_days = (diferencia - today).days
        remaining_days2 = (diferencia - fecha2).days
        rest=remaining_days2-remaining_days
        diff = [remaining_days,rest]
        return nume,diff
    
    def addIndividual(self, values):
        directorio = os.path.dirname(__file__)
        archivoUsuarios=os.path.join(directorio,self._file)
        if os.stat(archivoUsuarios).st_size == 0:
            columnas =pd.DataFrame([["n_act","fecha","mantenimiento","riesgo"]])
            columnas.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
        data1 = [[values[0],values[1],values[2],values[3]]]
        df1 = pd.DataFrame(data1)
        df1.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
