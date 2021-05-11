import os
import pandas as pd
import tabulate

class Equipo():
    _file = r"..\data\dispositivos.csv"
    def __init__(self,name,code,rs,brand,model,tipo,series,numAct):
        self.name = name
        self.code = code
        self.rs = rs
        self.brand = brand
        self.model = model
        self.tipo = tipo
        self.series = series
        self.numAct = numAct
    
    def create(self):
        directorio = os.path.dirname(__file__)
        archivoUsuarios=os.path.join(directorio,self._file)
        if os.stat(archivoUsuarios).st_size == 0:
            columnas =pd.DataFrame([["Nombre","Cod","RegSan","Marca","Modelo","Tipo","Serial","NumAct"]])
            columnas.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
        data1 = [[self.name,self.code,self.rs,self.brand,self.model,self.tipo,self.series,self.numAct]]
        df1 = pd.DataFrame(data1)
        df1.to_csv(archivoUsuarios, index=None, mode="a", header=not os.path.isfile(archivoUsuarios))
    
    def selDisp(self,num):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        df = pd.read_csv(datos)
        print(df)
        new_df = df.loc[df['NumAct'].astype(str).str.contains(num,case=False)]
        print("-"*30)
        print(new_df)
        idx = new_df.index
        return df,idx,datos
    
    def edit(self,num):
        df , idx , datos = self.selDisp(num)
        print(idx)
        print("¿Qué parámetro desea modificar?")
        print("[N]ombre")
        print("[C]ódigo")
        print("[R]egistro Sanitario")
        print("[M]arca")
        print("m[O]delo")
        print("[T]ipo")
        print("[S]erial")
        print("Número de [A]ctivo")
        opt = input(">>")
        if opt == "n":
            n_name = input("Ingrese el nuevo nombre >>")
            df.at[idx,'Nombre'] = n_name
        elif opt == "c":
            n_code = input("Ingrese el nuevo código >>")
            df.at[idx,'Cod'] = n_code
        elif opt == "r":
            n_rs = input("Ingrese el nuevo registro sanitario >>")
            df.at[idx,'RegSan'] = n_rs
        elif opt == "m":
            n_brand = input("Ingrese la nueva marca >>")
            df.at[idx,'Marca'] = n_brand
        elif opt == "o":
            n_model = input("Ingrese el nuevo modelo >>")
            df.at[idx,'Modelo'] = n_model
        elif opt == "t":
            n_tipo = input("Ingrese el nuevo tipo >>")
            df.at[idx,'Tipo'] = n_tipo
        elif opt == "s":
            n_series = input("Ingrese el nuevo serial >>")
            df.at[idx,'Serial'] = n_series
        elif opt == "a":
            n_activo = input("Ingrese el nuevo número de activo >>")
            df.at[idx,'NumAct'] = n_activo+"\n"     
        
        df.to_csv(datos, index=None, mode="w", header=["Nombre","Cod","RegSan","Marca","Modelo","Tipo","Serial","NumAct"])
        
        # df.to_csv(datos, index=False)

        # directory = os.path.dirname(__file__)
        # filePath = os.path.join(directory,self._file)
        # file = open(filePath,"r")
        # disp = file.readlines()
        # indx = 0
        # print(disp)
        # d,indx = self.selDisp(disp,num)

        # d_edit = [d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]]
        # d_edit = ";".join(d_edit)
        # disp[indx] = d_edit
        # disp = " ".join(disp)
        # file.close()
        # f = open(filePath, "w")
        # f.write(disp)
        # f.close()

    def erase(self,num):
        directory = os.path.dirname(__file__)
        filePath = os.path.join(directory,self._file)
        file = open(filePath,"r")
        disp = file.readlines()
        print(disp)
        d,indx = self.selDisp(disp,num)
        disp.remove(disp[indx])
        disp = "".join(disp)
        file.close()
        f = open(filePath, "w")
        f.write(disp)
        f.close()

    def verEquipos(self):
        directorio=os.path.dirname(__file__)
        archivo=self._file
        datos=os.path.join(directorio,archivo)
        df = pd.read_csv(datos)
        print(df)
        headers = df.columns.values.tolist()
        values = df.values.tolist()
        return (headers,values)
        # print(tabulate(df,headers='keys',tablefmt="github"))




