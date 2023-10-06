from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import great_circle
import MySQLdb

app = Flask(__name__)

# Configura la URI de la base de datos MySQL
    #   Conexion Profe
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
    #   Mi Conexion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://MrFerchoo:Jovencitos123@MrFerchoo.mysql.pythonanywhere-services.com/MrFerchoo$Store'


# Inicializa la extensión SQLAlchemy
db = SQLAlchemy(app)

# Modelo para la tabla de tiendas
class Store(db.Model):
    idStore = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lat = db.Column(db.String(20))
    lng = db.Column(db.String(20))
    details = db.relationship('Detail', backref='store', lazy=True)

# Modelo para la tabla de productos
class Product(db.Model):
    idProduct = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    name = db.Column(db.String(100))
    details = db.relationship('Detail', backref='product', lazy=True)

# Modelo para la tabla de detalles
class Detail(db.Model):
    idDetalle = db.Column(db.Integer, primary_key=True)
    idProduct = db.Column(db.Integer, db.ForeignKey('product.idProduct'))
    idStore = db.Column(db.Integer, db.ForeignKey('store.idStore'))
    price = db.Column(db.Float)
    idStock = db.Column(db.Integer)

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
        .with_entities(Store.name, Store.lat, Store.lng)
        .all()
    )

    # Calcula las distancias entre el usuario y las tiendas
    distances = []
    for store in stores:
        store_lat = float(store.lat)
        store_lon = float(store.lng)
        distance = great_circle((user_lat, user_lon), (store_lat, store_lon)).km
        distances.append((store.name, distance))

    nearest_stores = sorted(distances, key=lambda x: x[1])[:num_sucursales]

    # Devuelve las tiendas más cercanas en formato JSON
    result = [{'name': store[0], 'distance_km': store[1]} for store in nearest_stores]
    return jsonify(result)

    #   Obtener el producto por tiendas(Json)
@app.route('/product', methods=['POST'])
def get_stores_by_product():
    try:
        data = request.json
        product_id = int(data.get('idProduct'))
    except (ValueError, TypeError):
        return jsonify({'error': 'ID de producto no proporcionado o no válido'}), 400

    if product_id is None:
        return jsonify({'error': 'ID de producto no proporcionado'}), 400

    # Consulta las tiendas desde la base de datos
    stores = (
        db.session.query(Store)
        .join(Detail)
        .filter(Detail.idProduct == product_id)
        .with_entities(Store.idStore, Store.name, Store.lat, Store.lng)
        .all()
    )

    # Devuelve las tiendas asociadas al producto en formato JSON
    result = [{'idStore': store.idStore, 'name': store.name, 'lat': store.lat, 'lng': store.lng} for store in stores]
    return jsonify(result)


    #   Obtener el producto por tiendas(Ruta)
@app.route('/product_rute/<int:idProduct>', methods=['POST'])
def get_product_stores(idProduct):
    try:
        product = Product.query.get(idProduct)

        if product is None:
            return jsonify({"error": f"No se encontró el producto con ID {idProduct}"}), 404

        stores = [
            {
                "idStore": detail.store.idStore,
                "lat": detail.store.lat,
                "lng": detail.store.lng,
                "name": detail.store.name
            }
            for detail in product.details
        ]

        result = {"idProduct": idProduct, "stores": stores}
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    #   Obtener productos por tienda
@app.route('/product_store/<int:idStore>', methods=['GET'])
def get_store_products(idStore):
    try:
        store = Store.query.get(idStore)

        if store is None:
            return jsonify({"error": f"No se encontró la tienda con ID {idStore}"}), 404

        products = [
            {
                "idProduct": detail.product.idProduct,
                "name": detail.product.name,
                "description": detail.product.description,
                "price": detail.price,
                "idStock": detail.idStock
            }
            for detail in store.details
        ]

        result = {"idStore": idStore, "name": store.name, "products": products}
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)