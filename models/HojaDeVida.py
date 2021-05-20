import os
import pandas as pd
from tabulate import tabulate
import csv

from models.Converter import convert, getData, get_matches
from models.Extract import readHV
from models.Statistics import Estadistica

class HojaDeVida():
    def __init__(self): 
        self._file = r"..\data\HDV.csv"

    def create(self,filename):
        print("ENTRÓ A CREATE")
        refMat = convert(filename)
        print(refMat)
        print("MATRIZ DE REFERENCIA SIN MODIFICAR")
        headers, values = getData(refMat)
        self.newEquipo(headers,values)

    def read(self):
        hv = readHV('HV_BENEHEART_D6.csv')
        print(hv)
        return hv
    
    def newEquipo(self,headers,values):
        print(values)
        dic = ['No DE ACTIVO','FECHA DE INSTALACION','MENSUAL','BIMENSUAL','SEMESTRAL','TRIMESTRAL','BAJO','MODERADO(IIa)','ALTO(IIb)','MUY ALTO(III)']
        selected = []
        for indx,d in enumerate(dic):
            if indx >= dic.index('MENSUAL') and indx <= dic.index('TRIMESTRAL'):
                match = get_matches(d,headers)
                idx = headers.index(match)
                if len(values[idx]) > 0 :
                    selected.append(headers[idx])
            elif indx >= dic.index('BAJO') and indx <= dic.index('MUY ALTO(III)'):
                match = get_matches(d,headers)
                idx = headers.index(match)
                if len(values[idx])> 0:
                    selected.append(headers[idx])
            else:
                match = get_matches(d,headers)
                idx = headers.index(match)
                selected.append(values[idx].strip())                
        print(selected)
        selected[0]=selected[0].strip()
        selected[1]=selected[1][0:9]
        selected[2]=selected[2].strip()
        selected[3]=selected[3].strip()

        _file=r"individual.csv"
        Estadistica(_file).addIndividual(selected)

# ['FORMATO HOJA DE VIDA EQUIPO BIOMEDICO.P.S. MEDILAFNIT: 901069028-1', 'FECHA >', '04-01-2019', 'ELABORO', 'ING.BIOMEDICO', '1 OO', 'VERSION', 'CODIGO DELPRESTADOR |', '244980203/-01', 'DIRECCION', 'Cra 11A # 8-08 _', 'Ocafia', 'SEDE', '9693632 - 3185381229', 'TELEFONO', 'DISITINTIVO =', 'EMAIL', '0449602603 /-071 |', 'unidadcardiologicamedilaf@gmail.com', 'NOMBRE: =', 'Benerneart+ |', 'PISO.', 'Pnmer piso |', 'CODIGO DEL EQUIPO', '44 - 132 : oo', '', 'AREA', 'RS/ — PC/X NR/', '', 'MARCA:', 'Mindray ee', 'SERVICIO:', 'Cardiologia', 'MODELO:', '', 'SUBBUBICACION', '', 'TIPO', 'Peslbovriiadov |', '', 'SERIE', 'EQUIPO FIJO', 
# '', 'NoDEACTIVO:', '002 2 2', 'ee . Se', 'EQUIPO MOVIL', 'FORMA DE ADQUISICION', '', 'PROVEEDOR', 'No. DOCUMENTO DE ADQUSICION', '', 'CORREO', 'Oistrimedicos _', 'FECHA COMPRA', '', 'CIUDAD.', '', 'FECHA DE INSTALACION', '24 - 04% ~2021', 'TITULAR sss', 'FECHA DE OPERACION |', '', 'CORREO', '', 'FECHA DE VENCIMIENTO DE GARANTIA', 'O04 -03- 2025 |', 'CIUDAD.', '', 'FECHA FABRICACION', '', '_FABRICANTE', 'No FACTURA', '', 'VIDA UTIL Ss.', '', 'CORREO', 'CcCOsTO', '', '', 'PAIS', 'F.TE DE ALIMENTACION', '=90 ee', '', '', '', '', '', 'VOLTAJE a', '', '', 'PRESION', 'RANGO DE CORRIENTE', '', 'RANGO DE TEMPERATURA -', '', 'FRECUENCIA', 'TEMPERATURA', '', '', 'RANGO DE POTENCIA oo', '', 'RANGO DE PESO', '', '', 'CORRIENTE', 'VELOCIDAD =', '', 'FRECUENCIA :', '', 'RANGO DE LUMINOCIDAD', '', 'FOLENUIA a', 'GAPACIDAD oe', 'RANGO DE PRESION', '', 'OTRAS -', '', '', 'MANUVALES ee', 'PLANUS —', 'uso', 'RIESGO D4725/05', 'CLASIFICACION DE LA TECNOLOGIA', 'OPERACION ;', 'ee, ee', 'pe', 'ELECTRONICOS', 'MANTENIMIENTO.', 'ELECTRICOS', 'ee, ae', 'MEDICO', '', 'BAJO(I a', '> ca', '', 'TECNOLOGIA BAJA ee', '', 'PARTES sis', '', 'NEUMATICOS', 'BASICO', '', 'MODERADO(ila', '', 'TECNOLOGIA MEDIA', '', '', 'DESPIECES a', '', '', 'MECANICOS', '', 'APOYO', 'CB', 'ALTO({lib', 'TECNOLOGIA ALTA a', 'KR', '', 'HIDRAULICOS', '', 'INDUSTRIAL a', '', '', '', 'MUY ALTO (ll!', '', 'FECNOLOGIA PREDOMINANTE', 'CLASIFICACIO', 'N BIOMEDICA :', 'OBSERVACIONES Y RECOMENDACIONES', 'ELECTRICO', '', 'HIDRAULICO', 'DIAGNOS TICO', '', '', '', 'ELECTRONICO', 'NEUMATICO |', '>. ae', 'TRATAMIENTO Y SOPORTE DE VIDA', '', 'm a', 'MECANICO.', '', 'VAPOR', 'ANALISIS (LABORATORIO CLINICO)', '', '', 'Filial. <1 lal eee', '', '', 'SOLAR st', 'RERABILITACION _', '', 'NOMBRE', 'MARCA a', 'MODELO', 'SERIE BS', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '= ao. — . ’ aPO DE MANTENIMIENTO | isi DE MANTE!', 'PERIOCIOAD DE MANTENIMIENTO PREVENTIVO', 'CALIBRACION', 'PROPIOCONTRATADO', 'GARANTIA', '', 'MENSUAL oe', 'ee', '', '', 
# 'BIMENSUAL', 'a, cae', 'Sl', 'PERIODICIDAD', 'COMODATO _', 'KX', 'SEMESTRAL', '', 'TRIMESTRAL _', '', 'NO.', 'a. ee', '', 'Semesevu)']

# [('FECHA >', '04-01-2019'), ('ELABORO', 'ING, BIOMEDICO'), ('VERSION', 'f] is'), ('CODIGO DELPRESTADOR', 'D44980ZOS/-01'), ('D44980ZOS/-01', 'DIRECCION'), ('DIRECCION', 'Cra 11A # 8-08'), ('SEDE', 'Ocaha _'), ('TELEFONO.', '5693632 - 3185381229'), ('DISITINTIVO 7', '9449802037-0F'), ('9449802037-0F', 'EMAIL. ;'), ('EMAIL. ;', 'unidadcardiologicamedilaf@gmail.com'), ('NOMBRE:', ''), ('PISO.', 'Pomerpiso.'), ('CODIGO DEL EQUIPO', ''), ('MARCA: 7', ''), ('SERVICIO:', 'Cardiologia :'), ('MODELO: 7', ''), ('TIPO', ''), ('SERIE', ''), ('5 EE', 'EQUIPO MOVIL'), ('EQUIPO MOVIL', ''), ('FORMA DE ADQUISICION', ''), ('CORREO', 'Distrimedicos |'), ('FECHA COMPRA 7', ''), ('CIUDAD. 7', ''), ('FECHA DE INSTALACION BS', ''), ('FECHA DE OPERATION', ''), ('CORREO', 'ON'), ('FECHA DE VENCIMIENTO DE GARANTIA', ''), ('CIUDAD.', 'Ne'), ('FECHA FABRICACION |', ''), ('VIDA UTIL', 'CORREO'), ('CORREO', ''), ('PAIS', ''), ('F,.TE DE ALIMENTACION', ''), 
# ('=SO :', ''), ('VOLTAJE', 'XX'), ('XX', 'PRESION |'), ('PRESION |', 'XX'), ('XX', 'RANGO DE CORRIENTE'), ('RANGO DE CORRIENTE', 'XX'), ('XX', 'RANGO De TEMPERATURA |'), ('FRECUENCIA ;', ''), ('TEMPERATURA', ''), ('RANGO DE POTENCIA', ''), ('RANGO DE PESO', ''), ('CORRIENTE', ''), ('VELOCIDAD 7', ''), ('FRECUENCIA', ''), ('RANGO DE LUMINOCIDAD —', ''), ('POTENCOA', 'GAPAGIDAD'), ('GAPAGIDAD', ''), ('RANGO DE PRESION', ''), ('RIESGO D4725/05', 'CLASIFICACION DE LA TECNOLOGIA'), ('ELECTRONICOS', ''), ('MANTENIMIENTO', 'xx'), ('ELECTRICOS', 'xX'), ('BAJO', ''), ('TECNOLOGIA BAJA', 'XX'), ('NEUMATICOS', ''), ('BASICO.', 'xx'), ('XK', 'TECNROLOGIA MEDIA 7'), ('TECNROLOGIA MEDIA 7', ''), ('MECANICOS', ''), ('APOYO', ''), ('HIDRAULICOS', ''), ('_—“CSECNOLOGIA PREDOMINANTE', 'oD'), 
# ('LASIFICACIO', 'NBIOMEDICA |'), ('NBIOMEDICA |', 'OBSERVACIONES Y RECOMENDACIONES 7'), ("'HIDRAULICO", ''), ('DIAGNOS TICO _—', ''), ('NEUMATICO.', ''), ('TRATAMIENTO Y SOPORTE DE VIDA', ''), ('MECANICO', ''), ('VAPOR', ''), ('ANALISIS (LABORATORIO CLINICO)', ''), ('REMABILITACION =', ''), ('7 NOMBRE |', 'MARCA'), ('MARCA', '~MODELO oe'), ('FE', ''), ('PERIOCIDAD DE MANTENIMIENTOPREVENTIVO', 'GCALIBRACION'), ('GARANTIA', ''), ('MENSUAL', 'Xx'), ('BIMENSUAL >', ''), 
# ('COMODATO —__', ''), ('SEMESTRAL', ''), ('TRIMESTRAL', ''), ('NO', '')]