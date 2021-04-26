import os
# from models.Extract import get_matches

def addIndividual():
    directorio = os.path.dirname(__file__)
    file = r"..\data\hdvEquipos.csv"
    archivoUsuarios=os.path.join(directorio,file)
    file = open(archivoUsuarios,"r")
    datos = file.readlines()
    print(datos[0])
    # n_act = get_matches(datos[0][:])

if __name__ == "__main__":
    addIndividual()