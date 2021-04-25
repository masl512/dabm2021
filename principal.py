import os
from models.Usuario import Usuario
import pandas as pd

from models.Equipo import Equipo
from models.HojaDeVida import HojaDeVida
from models.Converter import convert,box_extraction
from models.Statistics import Estadistica

global u1
global navegante
global nav
u1=''
navegante=''
nav=''
# FORMAT METHODS
def title(string):
    string =  string.upper()
    for i in range(0,40):
        print("")
    print("-"*50)
    print(string.center(50))
    print("-"*50)

# UTILS
def createEquipo():
    title("CREAR EQUIPO NUEVO")
    print("Ingrese el NOMBRE del equipo")    
    # name = input(">>")
    name = "BeneHeart D6"
    print("Ingrese el CÓDIGO del equipo")    
    # code = input(">>")
    code = "11-132"
    print("Ingrese el REGISTRO SANITARIO del equipo")    
    # rs = input(">>")
    rs = "2010EBC-0005463"
    print("Ingrese la MARCA del equipo")    
    # brand = input(">>")
    brand = "MINDRAY"
    print("Ingrese el MODELO del equipo")    
    # model = input(">>")
    model = "BeneHeart D6"
    print("Ingrese el TIPO de equipo")    
    # tipo = input(">>")
    tipo = "DESFIBRILADOR"
    print("Ingrese la SERIE de equipo")    
    # series = input(">>")
    series = "DZ91003497"
    print("Ingrese el NÚMERO DE ACTIVO del equipo")    
    numAct = input(">>")
    # numAct = "1"
    disp = Equipo(name,code,rs,brand,model,tipo,series,numAct)
    disp.create()
    return disp

def HDV_equipo():
    bol = True
    while bol:
        title("GESTOR DE HOJAS DE VIDA PARA EQUIPOS")
        print("Seleccione la opción que desea realizar:")
        print("1. Convertir hoja de vida")
        print("2. Abrir hoja de vida")
        print("3. Borrar hoja de vida")
        print("4. Volver")
        # opt = input('>>')
        opt = "1"
        opt = opt.lower()
        if opt == "1":
            valores = HojaDeVida().create()
        elif opt == "2":
            matriz = HojaDeVida().read()
            print(matriz)
            # print(datosHV)
        elif opt == "3":
            pass
        elif opt == "4":
            bol = False

def crear_usuario():
    global u1
    print("Ingrese los siguientes datos:")
    nombre= input("Nombre")
    cedula= input("Cédula")
    cargo= input("Cargo(Técnico o Ingeniero)").lower()
    contacto=input("Ingrese número de telefono o correo electrónico")
    contraseña = input("Contraseña(Debe contener letras)")
    u1=Usuario(nombre,cedula,cargo,contacto,contraseña)
    print("Se registro ha sido exitoso "+u1.nombre)
    u1.save()

def perfil_usu():
    user=Usuario(navegante[0][0],navegante[0][1],navegante[0][2],navegante[0][3],navegante[0][4])
    bol = True
    while bol:
        title("Menú perfil usuario")
        print("1. Editar usuario")
        print("2. Eliminar usuario")
        print("3. Volver")
        op2= input(">> ")
        if(op2=="1"):
            print("Su información actual es:")
            print(nav)
            print("Ingrese el dato que desea modificar nombre,cedula,cargo,contacto,contraseña")
            op2= input(">>").lower()
            op3=input("Dato actual >> ")
            user.editar(op2,op3)
        elif(op2=="2"):
            user.eliminar(navegante[0][0])
        elif(op2=="3"):
            bol = False
        else:
            print("Opción no válida")

def equipos():
    disp = Equipo('','','','','','','','')
    bol = True
    while bol:
        title("Equipos")
        print("1. Crear equipo")
        print("2. Editar equipo")
        print("3. Eliminar equipo")
        print("4. Hoja de Vida")
        print("5. Ver equipos")
        print("6. Volver")
        # opt = input(">>")
        opt = "4"
        if opt == "1":
            disp = createEquipo()
        elif opt == "2":
            if "ing" in navegante[0][2].lower():
                print("Ingrese el número de activo del equipo que desea editar")
                numAct = input(">>")
                disp.edit(numAct)
            else:
                print("No posee los permisos suficientes para realizar esta acción")
        elif opt == "3":
            print("Ingrese el número de activo del equipo que desea eliminar")
            numAct = input(">>")
            disp.erase(numAct)
        elif opt == "4":
            HDV_equipo()
        elif opt == "5":
            disp.verEquipos()
            print("-"*50)
            print("Ingrese cualquier valor para salir")
            input(">>")
        elif opt == "6":
            bol = False
        else:
            print("¡Opción inválida!")

def estadisticas():
    bol = True
    while bol:
        title("Estadísticas")
        print("1. Información General")
        print("2. Información por equipo")
        print("3. Volver")
        op2= input(">>")
        if(op2=="1"):
            _file=r"general.csv"
            estd=Estadistica(_file)
            estd.general()
        elif(op2=="2"):
            nume=input("Ingrese el número de activo del equipo a visualizar >>")
            _file=r"individual.csv"
            estd=Estadistica(_file)
            estd.ind(nume)    
        elif(op2=="3"):
            bol = False


def menu_app():
    ext = 0
    while ext == 0:
        title("Menú principal")
        print("1. Inventario")
        print("2. Estadísticas")
        print("3. Perfil del usuario")
        print("4. Salir")
        # op2= input(">> ")
        op2 = "1"
        if(op2=="1"):
            equipos()
        elif(op2=="2"):
            estadisticas()
        elif(op2=="3"):
            perfil_usu()
        elif(op2=="4"):
            ext = 1
        else:
            print("Opción no válida")
            menu_app()

def ingresar():
    global navegante
    global nav
    # cedula=input("Cédula:")
    cedula = "120"
    # password=input("contraseña:")
    password = "asd"
    directorio = os.path.dirname(__file__)
    archivoUsuarios=os.path.join(directorio,"data/usuarios.csv")
    df = pd.read_csv(archivoUsuarios)
    a=df[(df['cedula'] == int(cedula)) & (df['contraseña']==password)]
    if len(a)>0:
        nav=a
        print(nav)
        navegante=nav.to_numpy()
        print(navegante)
        menu_app()
    else:
        print("datos erróneos")
        main()

def main():
    title("LOGIN")
    print("1.Crear usuario")
    print("2.Ingresar")
    print("3.salir")
    # op= input(">>")
    op = "2"
    # op = op.lower()
    if (op=="1"):
        crear_usuario()
    elif (op=="2"):
        ingresar()
    elif (op=="3"):
        exit()
    else:
        print("Opción no válida")
        main()
    main()

if __name__=='__main__':
    main()