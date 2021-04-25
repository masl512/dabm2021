import os
import pandas as pd
from tabulate import tabulate
import csv

from models.Converter import convert,getData
from models.Extract import readHV

class HojaDeVida():
    def __init__(self): 
        self._file = r"..\data\HDV.csv"

    def create(self):
        refMat = convert()
        print("MATRIZ DE REFERENCIA SIN MODIFICAR")
        print(refMat)
        getData(refMat)
        self.newEquipo()

    def read(self):
        hv = readHV('HV_BENEHEART_D6.csv')
        print(hv)
        return hv
    
    def newEquipo(self):
        directorio = os.path.dirname(__file__)
        archivo =  r'..\data\hdvEquipos.csv'
        datos = os.path.join(directorio,archivo)        
        file = open(datos,"a")
        file.close()
        df = pd.read_csv(datos)
        print(df)
