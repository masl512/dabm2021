import re
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
disp = Equipo('','','','','','','','','')
user = Usuario('','','','','')


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

def updateGeneral():
    global disp
    h,v = disp.verEquipos()
    mant = [fila for fila in v if fila[8]=='mantenimiento']
    dispo = [e for e in v if e[8]=='disponible']
    fuera = [e for e in v if e[8]=='fuera de servicio']
    data = [[len(mant),len(dispo),len(fuera)]]
    df = pd.DataFrame(data)
    print(df)
    directorio=os.path.dirname(__file__)
    archivo='general.csv'
    datos=os.path.join(directorio,'models',archivo)
    df.to_csv(datos, index=None, mode="w", header=["mantenimiento","disponibles","fuera de servicio"])


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
    updateGeneral()
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
            n_estado = df.at[idx,'Estado']
            dispSel = [n_name,n_code,n_rs,n_brand,n_model,n_tipo,n_series,n_activo,n_estado]
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
    updateGeneral()
    _file=r"general.csv"
    estd=Estadistica(_file)
    datosGen=estd.general()
    directorio = os.path.dirname(__file__)
    archivoUsuarios=os.path.join(directorio,'models','individual.csv')
    df = pd.read_csv(archivoUsuarios)
    numActs = df['n_act']
    numActs = numActs.to_numpy()    
    # numActs,datosInd,diff = estd.ind()
    return render_template('estadisticas.html', numActs = numActs, datosGen = datosGen)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      name = os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename))
      f.save(name)
      print("-"*60)
      print(name)
      HojaDeVida().create(str(name))
      return redirect(url_for("inventario"))

@app.route('/user')
def usuario():
    return render_template('user.html', user=navegante)

@app.route('/individual', methods=['GET', 'POST'])
def indivEstad():
    if request.method == "POST":
        n_act = request.form.get("numAct", None)
        print(n_act)
        _file=r"individual.csv"
        estd=Estadistica(_file)
        headers = ['Num. Activo','Fecha de Instalación','Mantenimiento','Riesgo']
        indiv , data=estd.ind(n_act) 
        if data!=None:
            return render_template("indivdual.html", headers=headers, dias=data, indiv = indiv)
    return redirect(url_for("estadisticas"))

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
    return redirect(url_for("inicio"))

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
    return redirect(url_for("inicio"))

@app.route('/creareq', methods=["POST"])
def creareq():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        code = request.form['cod']
        rs = request.form['rs']
        brand = request.form['brand']
        model = request.form['model']
        tipo = request.form['type']
        series = request.form['serial']
        numAct = request.form['numAct']
        estado = request.form['estado']
        dis = Equipo(name,code,rs,brand,model,tipo,series,numAct,estado)
        # disp = Equipo()
        dis.create()
        return redirect(url_for("inventario"))
    return redirect(url_for("inventario"))

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
        estado = request.form.get("estado")
        cambios = [nombre,cod,rs,brand,model,tipo,series,numAct,estado]
        disp.editEq(cambios,numAct)
        return redirect(url_for("inventario"))

@app.route('/editUser') 
def editUser():
    return render_template('editUser.html',user = navegante)

@app.route('/getEditUser',methods=['POST'])
def getEditUser():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cedula = request.form.get("cedula")
        cargo = request.form.get("cargo")
        cel = request.form.get("contact")
        pw = request.form.get("pw")
        pw = pw.strip('"')
        
        cambios = [nombre,cedula,cargo,cel,pw]
        user.editUser(cambios,cedula)
        return redirect(url_for("usuario"))

# PUNTO DE ACCESO
if __name__ == '__main__':
    app.run(debug = True)
