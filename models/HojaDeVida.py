import os
import pandas as pd
from tabulate import tabulate
import csv

from models.Converter import convert, getData
from models.Extract import readHV
from models.Statistics import Estadistica

class HojaDeVida():
    def __init__(self): 
        self._file = r"..\data\HDV.csv"

    def create(self,filename):
        print("ENTRÓ A CREATE")
        refMat = convert(filename)
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
        df = pd.read_csv(datos,sep=',', index_col= False)
        print(df)
        _file=r"individual.csv"
        Estadistica(_file).addIndividual()

# ['FORMATO HOJA DE VIDA EQUIPO BIOMEDICO.P.S. MEDILAFNIT: 901069028-1', 'FECHA >', '04-01-2019', 'ELABORO', 'ING.BIOMEDICO', '1 OO', 'VERSION', 'CODIGO DELPRESTADOR |', '244980203/-01', 'DIRECCION', 'Cra 11A # 8-08 _', 'Ocafia', 'SEDE', '9693632 - 3185381229', 'TELEFONO', 'DISITINTIVO =', 'EMAIL', '0449602603 /-071 |', 'unidadcardiologicamedilaf@gmail.com', 'NOMBRE: =', 'Benerneart+ |', 'PISO.', 'Pnmer piso |', 'CODIGO DEL EQUIPO', '44 - 132 : oo', '', 'AREA', 'RS/ — PC/X NR/', '', 'MARCA:', 'Mindray ee', 'SERVICIO:', 'Cardiologia', 'MODELO:', '', 'SUBBUBICACION', '', 'TIPO', 'Peslbovriiadov |', '', 'SERIE', 'EQUIPO FIJO', 
# '', 'NoDEACTIVO:', '002 2 2', 'ee . Se', 'EQUIPO MOVIL', 'FORMA DE ADQUISICION', '', 'PROVEEDOR', 'No. DOCUMENTO DE ADQUSICION', '', 'CORREO', 'Oistrimedicos _', 'FECHA COMPRA', '', 'CIUDAD.', '', 'FECHA DE INSTALACION', '24 - 04% ~2021', 'TITULAR sss', 'FECHA DE OPERACION |', '', 'CORREO', '', 'FECHA DE VENCIMIENTO DE GARANTIA', 'O04 -03- 2025 |', 'CIUDAD.', '', 'FECHA FABRICACION', '', '_FABRICANTE', 'No FACTURA', '', 'VIDA UTIL Ss.', '', 'CORREO', 'CcCOsTO', '', '', 'PAIS', 'F.TE DE ALIMENTACION', '=90 ee', '', '', '', '', '', 'VOLTAJE a', '', '', 'PRESION', 'RANGO DE CORRIENTE', '', 'RANGO DE TEMPERATURA -', '', 'FRECUENCIA', 'TEMPERATURA', '', '', 'RANGO DE POTENCIA oo', '', 'RANGO DE PESO', '', '', 'CORRIENTE', 'VELOCIDAD =', '', 'FRECUENCIA :', '', 'RANGO DE LUMINOCIDAD', '', 'FOLENUIA a', 'GAPACIDAD oe', 'RANGO DE PRESION', '', 'OTRAS -', '', '', 'MANUVALES ee', 'PLANUS —', 'uso', 'RIESGO D4725/05', 'CLASIFICACION DE LA TECNOLOGIA', 'OPERACION ;', 'ee, ee', 'pe', 'ELECTRONICOS', 'MANTENIMIENTO.', 'ELECTRICOS', 'ee, ae', 'MEDICO', '', 'BAJO(I a', '> ca', '', 'TECNOLOGIA BAJA ee', '', 'PARTES sis', '', 'NEUMATICOS', 'BASICO', '', 'MODERADO(ila', '', 'TECNOLOGIA MEDIA', '', '', 'DESPIECES a', '', '', 'MECANICOS', '', 'APOYO', 'CB', 'ALTO({lib', 'TECNOLOGIA ALTA a', 'KR', '', 'HIDRAULICOS', '', 'INDUSTRIAL a', '', '', '', 'MUY ALTO (ll!', '', 'FECNOLOGIA PREDOMINANTE', 'CLASIFICACIO', 'N BIOMEDICA :', 'OBSERVACIONES Y RECOMENDACIONES', 'ELECTRICO', '', 'HIDRAULICO', 'DIAGNOS TICO', '', '', '', 'ELECTRONICO', 'NEUMATICO |', '>. ae', 'TRATAMIENTO Y SOPORTE DE VIDA', '', 'm a', 'MECANICO.', '', 'VAPOR', 'ANALISIS (LABORATORIO CLINICO)', '', '', 'Filial. <1 lal eee', '', '', 'SOLAR st', 'RERABILITACION _', '', 'NOMBRE', 'MARCA a', 'MODELO', 'SERIE BS', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '= ao. — . ’ aPO DE MANTENIMIENTO | isi DE MANTE!', 'PERIOCIOAD DE MANTENIMIENTO PREVENTIVO', 'CALIBRACION', 'PROPIOCONTRATADO', 'GARANTIA', '', 'MENSUAL oe', 'ee', '', '', 
# 'BIMENSUAL', 'a, cae', 'Sl', 'PERIODICIDAD', 'COMODATO _', 'KX', 'SEMESTRAL', '', 'TRIMESTRAL _', '', 'NO.', 'a. ee', '', 'Semesevu)']