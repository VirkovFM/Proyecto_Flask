from flask import Flask, render_template, request, jsonify
import MySQLdb
from geopy.distance import great_circle

app = Flask(__name__)

# flask --app main.py run

# Conexion a la base de datos

host = 'MrFerchoo.mysql.pythonanywhere-services.com'
user = 'MrFerchoo'
password = 'Jovencitos123'
database = 'MrFerchoo$Store'

connection = MySQLdb.connect(host=host, user=user, password=password, database=database)

cursor = connection.cursor()
cursor.execute("SELECT * FROM store")
data = cursor.fetchall()

#   Rutas
@app.route('/')   #esto sal escribiendo route y tab
def index():
    edad = 18
    #return edad, "<h1>VERDEEEEEEEEEEEEEEEEEEEEEEEE</h1>"
    return render_template('index.html', dato2 = ["1","2","3","4"])

@app.route('/contacto')
def contacto():
    total = 1000
    return "<h1>Bienvenidos a Flask - Contacto</h1>"

@app.route('/proyectos')
@app.route('/proyectos/<string:nombre>/<int:edad>')
def proyectos(nombre = None, edad = 0):
    if nombre is None:
        return render_template('proyectos.html')
    else:
        return render_template('proyectos.html',edad = edad, nombre = nombre)


@app.route('/loops')
def loops():
    lista = ["Frutas","Verdurass","Limpieza","Abarrotes"]
    return render_template('loops.html',lista = lista)  #El lista antes de lista es la variable del html


@app.route('/mapa/<float:lat>/<float(signed=True):long>/<float(signed=True):zoom>/<float(signed=True):sizemap>/<float(signed=True):sizemaps>/<string:nombre>',methods=['GET'])
def mapa(lat,long,zoom,sizemap,sizemaps,nombre):
    markers=[
   {
   'lat':lat,
   'lon':long,
   'zoom':zoom,
   'sizemap':sizemap,
   'sizemaps':sizemaps,
   'popup':nombre
    }
   ]
    return render_template('mapa.html',lat=lat,long=long,markers=markers)

@app.route('/nearest', methods=['GET'])
def nearest_stores():
    # Obtén la latitud y longitud del usuario desde los parámetros de la solicitud
    user_lat = float(request.args.get('lat'))
    user_lon = float(request.args.get('lon'))

    # Consulta las tiendas desde la base de datos
    cursor = connection.cursor()
    cursor.execute("SELECT name, lat, lon FROM store")
    stores = cursor.fetchall()

    # Calcula las distancias entre el usuario y las tiendas
    distances = []
    for store in stores:
        store_lat = store[1]
        store_lon = store[2]
        distance = great_circle((user_lat, user_lon), (store_lat, store_lon)).km
        distances.append((store[0], distance))

    # Ordena las tiendas por distancia y selecciona las 5 más cercanas
    nearest_stores = sorted(distances, key=lambda x: x[1])[:5]

    # Devuelve las 5 tiendas más cercanas en formato JSON
    result = [{'name': store[0], 'distance_km': store[1]} for store in nearest_stores]
    return jsonify(result)
