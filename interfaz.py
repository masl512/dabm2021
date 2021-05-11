from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
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
u1=''
navegante=''
nav=''
disp = Equipo('','','','','','','','')

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

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registro')
def parametros():
    return render_template('registro.html', titulo="Registra tus datos")

@app.route('/menu_principal') 
def menu_principal():
    return render_template('mainmenu.html', user=navegante)

@app.route('/inventario')
def inventario():
    df = disp.verEquipos()
    # print(df)
    return render_template('inventario.html',equipos=df)

@app.route('/createEquipo') 
def createEquipo():
    return render_template('createEquipo.html', titulo="Crear Equipo")

@app.route('/editEquipo') 
def editEquipo():
    return render_template('editEquipo.html', titulo="Crear Equipo")

@app.route('/estadisticas') 
def estadisticas():
    _file=r"general.csv"
    estd=Estadistica(_file)
    datosGen=estd.general()
    return render_template('estadisticas.html', titulo="Estadisticas", datos = datosGen)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      name = secure_filename(f.filename)
      print("-"*60)
      print(name)
      HojaDeVida().create(str(name))
      return 'file uploaded successfully'

@app.route('/user')
def usuario():
    return render_template('user.html', user=navegante)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        n_act = request.form.get("act", None)
        print(n_act)
        _file=r"individual.csv"
        estd=Estadistica(_file)
        data=estd.ind(n_act) 
        if car_brand!=None:
            return render_template("estadisticas.html", datosT = data[0], datosT1 = data[1])
    return render_template("estadisticas.html") 

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        doc = request.form['doc']
        passw = request.form['pw']
        if doc and passw:
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
        nombre = request.form['name']
        documento = request.form['doc']
        cargo = request.form['cargo']
        celular = request.form['cel']
        contraseña = request.form['pw']
        u1=Usuario(nombre,documento,cargo,celular,contraseña)
        u1.save()
        return redirect(url_for("inicio"))
    return "Registro no permitido"

@app.route('/creareq', methods=["POST"])
def creareq():
    global disp
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

@app.route('/editeq',methods=["POST"])
def editeq():
    disp.edit(numAct)

@app.route('/convert',methods=["POST"])
def convertHV():
    convert()

if __name__ == "__main__":
    app.run(debug=True)