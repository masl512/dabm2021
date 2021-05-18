import os
import pandas as pd
import numpy

class Usuario:
    _file = r"..\data\usuarios.csv"
    def __init__(self,nombre,cedula,cargo,contacto,contraseña):
        self.nombre=nombre
        self.cedula=cedula
        self.cargo=cargo
        self.contacto=contacto
        self.contraseña=contraseña
    def save(self):
        directorio = os.path.dirname(__file__)
        archivoUsuarios=os.path.join(directorio,self._file)
        if os.stat(archivoUsuarios).st_size == 0:
            columnas =pd.DataFrame([["nombre","cedula","cargo","contacto","contraseña"]])
            columnas.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
        data1 = [[self.nombre,str(self.cedula),self.cargo,self.contacto,self.contraseña]]
        df1 = pd.DataFrame(data1)
        df1.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
    
    def editar(self,cambio,variable):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        df = pd.read_csv(datos)
        df.loc[df['nombre'] == self.nombre, cambio] = variable
        df.to_csv(datos, index=False)
    
    def eliminar(self,dato):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        df = pd.read_csv(datos)
        df = df.drop(df[df['nombre']==dato].index)
        df.to_csv(datos, index=False)
    
    def selUser(self,num):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        df = pd.read_csv(datos)
        # print("-"*60)
        # print(df)
        # print(type(df.loc[df['cedula']]))
        lista = df['cedula'].to_numpy()
        lista = list(df['cedula'])
        print(lista)
        print(num)
        # new_df = df.loc[df['cedula'].astype(str).str.contains(num,case=False)]
        idx = lista.index(int(num))
        # print("-"*30)
        # print(new_df)
        # idx = new_df.index
        return df,idx,datos
    
    def editUser(self,cambios,_id):
        df , idx , datos = self.selUser(_id)
        df.at[idx,'nombre'] = cambios[0]
        df.at[idx,'cedula'] = cambios[1]
        df.at[idx,'cargo'] = cambios[2]
        df.at[idx,'contacto'] = cambios[3]
        df.at[idx,'contraseña'] = cambios[4]     
        df.to_csv(datos, index=None, mode="w", header=["nombre","cedula","cargo","contacto","contraseña"])

 