from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import great_circle
import MySQLdb

app = Flask(__name__)

# Configura la URI de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://MrFerchoo:Jovencitos123@MrFerchoo.mysql.pythonanywhere-services.com:3306/MrFerchoo$Store'

# Inicializa la extensión SQLAlchemy
db = SQLAlchemy(app)

# Define el modelo de datos Store
class Store(db.Model):
    idStore = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lat = db.Column(db.String(20))
    lon = db.Column(db.String(20))

"""host = 'MrFerchoo.mysql.pythonanywhere-services.com'
user = 'MrFerchoo'
password = 'Jovencitos123'
database = 'MrFerchoo$Store'

connection = MySQLdb.connect(host=host, user=user, password=password, database=database)

cursor = connection.cursor()
cursor.execute("SELECT * FROM store")
data = cursor.fetchall()
"""

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
    try:
        user_lat = float(request.args.get('lat'))
        user_lon = float(request.args.get('lon'))
        num_sucursales = int(request.args.get('num_sucursales', 5))
    except ValueError:
        return jsonify({"error": "Coordenadas inválidas o num_sucursales inválido"}), 400

    # Consulta las tiendas desde la base de datos
    stores = (
        db.session.query(Store)
        .with_entities(Store.name, Store.lat, Store.lon)  # Ajusté 'Store.long' a 'Store.lon'
        .all()
    )

    # Calcula las distancias entre el usuario y las tiendas
    distances = []
    for store in stores:
        store_lat = float(store.lat)
        store_lon = float(store.lon)  # Ajusté 'store.long' a 'store.lon'
        distance = great_circle((user_lat, user_lon), (store_lat, store_lon)).km
        distances.append((store.name, distance))

    # Ordena las tiendas por distancia y selecciona las 'num_sucursales' más cercanas
    nearest_stores = sorted(distances, key=lambda x: x[1])[:num_sucursales]

    # Devuelve las tiendas más cercanas en formato JSON
    result = [{'name': store[0], 'distance_km': store[1]} for store in nearest_stores]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)