from flask import Flask, render_template, url_for

app = Flask(__name__)

# flask --app main.py run
app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
db = SQLAlchemy(app)

class Store(db.Model):
    idStore = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    lat = db.Column(db.String(20))
    long = db.Column(db.String(20))

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

@app.route('/nearest_stores', methods=['GET'])
def nearest_stores():
    try:
        latitud_usuario = float(request.args.get('latitud'))
        longitud_usuario = float(request.args.get('longitud'))
    except ValueError:
        return jsonify({"error": "Coordenadas inválidas"}), 400

    # Consulta las 5 ubicaciones más cercanas en la base de datos utilizando SQLAlchemy
    ubicaciones_cercanas = (
        db.session.query(Store)
        .order_by(
            ((Store.lat.cast(db.Float) - latitud_usuario) ** 2 + (Store.long.cast(db.Float) - longitud_usuario) ** 2)
        )
        .limit(5)
        .all()
    )

    # Convierte los resultados a un formato JSON
    ubicaciones_json = [
        {"name": store.name, "lat": store.lat, "long": store.long}
        for store in ubicaciones_cercanas
    ]

    return jsonify({"ubicaciones_cercanas": ubicaciones_json})

if __name__ == '__main__':
    app.run(debug=True)