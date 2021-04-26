import numpy as np
from math import isnan
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
import pandas as pd
from models.Extract import get_matches

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
        turistas = [nume[0][0],nume[0][1],nume[0][2]]
        paises = ['Mantenimiento: '+ str(turistas[0]), 'Disponibles: '+ str(turistas[1]), 'Fuera de servicio: ' + str(turistas[2])]
        explode = [0.1, 0, 0]  # Destacar algunos
        plt.pie(turistas, labels=paises, explode=explode,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Estado de los equipos del hospital')
        plt.show()

    def ind(self,numer):
        directorio = os.path.dirname(__file__)
        archivoUsuarios=os.path.join(directorio,self._file)
        file = open(archivoUsuarios,"a")
        file.close()
        df = pd.read_csv(archivoUsuarios)
        a=df[(df['n_act'] == int(numer))]
        print(a)
        nume=a.to_numpy()
        fechaN=nume[0][1]
        arr = fechaN.split('-')
        fecha2 = datetime(int(arr[2]),int(arr[1]),int(arr[0]))
        if nume[0][2]=="mensual":
            diferencia = fecha2 + timedelta(days=30)
        elif nume[0][2]=="bimestral":
            diferencia = fecha2 + timedelta(days=15)
        elif nume[0][2]=="trimestral":
            diferencia = fecha2 + timedelta(days=90)
        else:
            diferencia = fecha2 + timedelta(days=180)
        today = datetime.today()
        remaining_days = (diferencia - today).days
        remaining_days2 = (diferencia - fecha2).days
        rest=remaining_days2-remaining_days
        turi = [remaining_days,rest]
        paises = ['Días restantes: '+ str(turi[0]), 'Dias abarcados: '+ str(turi[1])]
        explode = [0, 0]  # Destacar algunos
        plt.pie(turi, labels=paises, explode=explode,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Tiempo hasta el proximo matenimiento')
        plt.show()

    def addIndividual(self):
        directorio = os.path.dirname(__file__)
        file = r"..\data\hdvEquipos.csv"
        archivoUsuarios=os.path.join(directorio,file)
        # file = open(archivoUsuarios,"r")
        # datos = file.readlines()
        # file.close()
        datos = pd.read_csv(archivoUsuarios)
        tam = len(datos)
        col_n_act = get_matches("No DE ACTIVO",datos.loc[[0]])
        n_act = datos.loc[tam-1,col_n_act]
        col_fecha = get_matches("FECHA DE INSTALACION",datos.loc[[0]])
        fecha = datos.loc[tam-1,col_fecha]
        mants = ["MENSUAL","BIMENSUAL","TRIMESTRAL","SEMESTRAL"]
        mantenimiento = self.search(mants,datos)
        risk = ["BAJO(I)","MODERADO(IIa)","ALTO(IIb)","MUY ALTO(III)"]
        riesgo = self.search(risk,datos)
        clasificacion = "-"
        use = ["MEDICO","BASICO","APOYO","INDUSTRIAL"]
        uso = self.search(use,datos)
        indiv = [[n_act , fecha , mantenimiento , riesgo , clasificacion , uso]]
        archivoUsuarios=os.path.join(directorio,"individual.csv")
        df1 = pd.DataFrame(indiv)
        df1.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))

    
    def search(self,opts,datos):
        tam = len(datos)
        for m in opts:
            idx_opt = get_matches(m,datos.loc[[0]])
            item = datos.loc[tam-1,idx_opt]
            if not isnan(item):
                opt = datos.loc[tam-1,idx_opt]
            else:
                opt = "-"
        return opt

