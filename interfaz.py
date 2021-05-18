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
global user
u1=''
navegante=''
nav=''
disp = Equipo('','','','','','','','')

app = Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

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
    return render_template('createEquipo.html')

@app.route('/editEquipo', methods=['POST']) 
def editEquipo():
    global disp
    if request.method == "POST":
        numAct = str(request.form.get("numAct"))
        print('Número de Activo')
        print(numAct)
        df , idx , datos = disp.selDisp(numAct)
        print(idx)
        if not idx.empty:
            idx = idx[0]
            n_name = df.at[idx,'Nombre']
            n_code = df.at[idx,'Cod']
            n_rs = df.at[idx,'RegSan']
            n_brand = df.at[idx,'Marca']
            n_model = df.at[idx,'Modelo']
            n_tipo = df.at[idx,'Tipo']
            n_series = df.at[idx,'Serial']
            n_activo = df.at[idx,'NumAct']
            dispSel = [n_name,n_code,n_rs,n_brand,n_model,n_tipo,n_series,n_activo]
            return render_template('editEquipo.html',dispSel = dispSel)
        return redirect(url_for('inventario'))

@app.route('/eliminar', methods=['POST'])
def eliminar():
    global disp
    if request.method == "POST":
        numAct = str(request.form.get("numAct"))
        print('Número de Activo')
        print(numAct)
        if numAct!=None:
            disp.erase(numAct)
    return redirect(url_for('inventario'))

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
      name = os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename))
      f.save(name)
    #   f.save(secure_filename(f.filename))
    #   name = secure_filename(f.filename)
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

@app.route('/guardar', methods=["POST"])
def guardar():
    if request.method == 'POST':
        doc = request.form['doc']
        passw = request.form['pw']
        if doc and passw:
            bandera=ingresar(doc,passw)
            print(bandera)
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

@app.route('/getEdit',methods=['POST'])
def getEdit():
    global disp
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cod = request.form.get("cod")
        rs = request.form.get("rs")
        brand = request.form.get("brand")
        model = request.form.get("model")
        tipo = request.form.get("tipo")
        series = request.form.get("series")
        numAct = request.form.get("numAct")
        cambios = [nombre,cod,rs,brand,model,tipo,series,numAct]
        disp.editEq(cambios,numAct)
        return redirect(url_for("inventario"))

        
         









###


if __name__ == '__main__':
    app.run(debug = True)
