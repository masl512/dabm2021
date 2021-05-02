from flask import Flask
from flask import render_template, request, redirect, url_for
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
global disp
global user
u1=''
navegante=''
nav=''
disp=''
user=''


app = Flask(__name__)

def ingresar(cedula,password):
    global navegante
    global nav
    directorio = os.path.dirname(__file__)
    archivoUsuarios=os.path.join(directorio,"data/usuarios.csv")
    df = pd.read_csv(archivoUsuarios)
    a=df[(df['cedula'] == int(cedula)) & (df['contraseña']==password)]
    if len(a)>0:
        nav=a
        navegante=nav.to_numpy()
        val=True
    else:
        val=False
    return val

def extraccionedit():
    _file = r"..\data\dispositivos.csv"
    directorio=os.path.dirname(__file__)
    archivo=_file
    datos=os.path.join(directorio,archivo)
    df = pd.read_csv(datos)
    a=df.loc[:,'NumAct']
    dat_edit=a.to_numpy()
    return dat_edit



@app.route('/')
def inicio():
    return render_template('index.html', titulo="Bienvenido")

@app.route('/registro')
def parametros():
    return render_template('registro.html', titulo="Registra tus datos")

@app.route('/menu_principal') 
def menu_principal():
    return render_template('menuprincial.html', titulo="Menú Principal")

@app.route('/createEquipo') 
def createEquipo():
    return render_template('createEquipo.html', titulo="Crear Equipo")


@app.route('/Hoja_de_Vida') 
def Hoja_de_Vida():
    return render_template("Hoja_de_Vida.html", titulo="GESTOR DE HOJAS DE VIDA PARA EQUIPOS")

@app.route('/perfil_usu') 
def perfil_usu():
    global user
    user=Usuario(navegante[0][0],navegante[0][1],navegante[0][2],navegante[0][3],navegante[0][4])
    return render_template("perfil_usu.html", titulo="Perfil del usuario", datos=navegante)


@app.route('/Equipo') #esta funcion diseñarla con desplegable
def Equipo():
    global disp
    disp = Equipo('','','','','','','','')
    return render_template('Equipo.html', titulo="Equipo")

@app.route('/log', methods=['GET', 'POST'])
def log():
    global user
    if request.method == "POST":
        car_brand = request.form.get("car", None)
        print(car_brand)
        if eqp=="Editar usuario":
            return render_template("perfil_usu.html", activo="activo")
        else:
            user.eliminar(navegante[0][0])
            return render_template("perfil_usu.html", activo2="desactivo")
    return render_template("perfil_usu.html")


@app.route('/creareq', methods=['GET', 'POST'])
def creareq():
    global user
    if request.method == "POST":
        dato = request.form.get("car", None)
        actual = request.form['actual']
        user.editar(dato,actual)
        return redirect(url_for("perfil_usu"))
    return "Registro no permitido"

@app.route('/estadisticas') 
def estadisticas():
    _file=r"general.csv"
    estd=Estadistica(_file)
    datosGen=estd.general()
    return render_template('estadisticas.html', titulo="Estadisticas", datos = datosGen)

@app.route('/login', methods=['GET', 'POST'])#adquisicion de datos de estadisticas
def login():
    if request.method == "POST":
        n_act = request.form.get("act", None)
        print(n_act)
        _file=r"individual.csv"
        estd=Estadistica(_file)
        data=estd.ind(n_act) 
        if car_brand!=None:
            return render_template("estadisticas.html", datosT = data[0], datosG = data[1])
    return render_template("estadisticas.html") 

@app.route('/equipo2', methods=['GET', 'POST'])#adquisicion de datos de equipo
def equipo2():
    if request.method == "POST":
        eqp = request.form.get("eqp", None)
        print("1. Crear equipo")
        print("2. Editar equipo")
        print("3. Eliminar equipo")
        print("4. Hoja de Vida")
        print("5. Ver equipos")
        if eqp=="Crear equipo":
            return render_template("createEquipo.html")
        elif eqp=="Editar equipo":
            if "ing" in navegante[0][2].lower():
                da_edita=extraccionedit()
                return render_template("Equipo.html", num_acti = da_edita)
            else:
                return "Acceso no permitido"
        elif eqp=="Eliminar equipo":
            da_edita=extraccionedit()
            return render_template("Equipo.html", num_acti = da_edita)
        elif eqp=="Hoja de Vida":
            return render_template("Hoja_de_Vida.html")
        else:
            ver=disp.verEquipos()
            return render_template("Equipo.html", ver_acti = ver)

    return render_template("estadisticas.html") 


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == "POST":
        numAct = request.form.get("num", None)
        if numAct!=None:
            disp.edit(numAct)
    return render_template("Equipo.html")

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    if request.method == "POST":
        numAct = request.form.get("num", None)
        if numAct!=None:
            disp.erase(numAct)
    return render_template("Equipo.html")





@app.route('/guardar', methods=["POST"])
def guardar():
    if request.method == 'POST':
        doc = request.form['documento']
        passw = request.form['contraseña']
        bandera=ingresar(doc,passw)
        if bandera:
            return redirect(url_for("menu_principal"))
        else:
            return redirect(url_for("inicio"))
    return "Acceso no permitido"


@app.route('/registrar', methods=["POST"])
def registrar():
    global u1
    if request.method == 'POST':
        nombre = request.form['nombre']
        documento = request.form['documento']
        cargo = request.form['cargo']
        celular = request.form['celular']
        contraseña = request.form['contraseña']
        u1=Usuario(nombre,documento,cargo,celular,contraseña)
        u1.save()
        return redirect(url_for("inicio"))
    return "Registro no permitido"

@app.route('/creareq', methods=["POST"])
def creareq():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        rs = request.form['rs']
        brand = request.form['brand']
        model = request.form['model']
        tipo = request.form['tipo']
        series = request.form['series']
        numAct = request.form['numAct']
        disp = Equipo(name,code,rs,brand,model,tipo,series,numAct)
        disp.create()
        return redirect(url_for("inicio"))
    return "Registro no permitido"


###
@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == "POST":
        car_brand = request.form.get("cars", None)
        #print(car_brand)
        if car_brand!=None:
            return render_template("test.html", car_brand = car_brand)

            disp.edit(numAct)
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug = True)