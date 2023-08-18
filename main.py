from flask import Flask, render_template, url_for

app = Flask(__name__)

# flask --app main.py run

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
