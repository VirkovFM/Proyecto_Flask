import secrets

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(128))
    token = db.Column(db.String(64))

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        if user.token == "":
            token = secrets.token_hex(32)
            user.token = token
            db.session.commit()

        return jsonify({'name':user.name,'token':user.token})
    else :
        return jsonify({'error':'Credenciales inválidas'})

@app.route('/change_password',methods=['POST'])
def changePassword():
    data = request.get_json()
    token = data.get('token')
    password = data.get('password')

    user = User.query.filter_by(token=token).first()

    if user :
        user.password = password
        db.session.commit()
        return jsonify({'name':user.name,'token':user.token})
    else :
        return jsonify({'error':'Credenciales inválidas'})

@app.route('/update_user',methods=['POST'])
def updateUser():
    data = request.get_json()
    token = data.get('token')
    name = data.get('name')
    email = data.get('email')

    user = User.query.filter_by(token=token).first()

    if user :
        if name != "" and name != user.name:
            user.name = name
        if email != "" and email != user.email:
            user.email = email
        db.session.commit()
        return jsonify({'name':user.name,'token':user.token})
    else :
        return jsonify({'error':'Credenciales inválidas'})

if _name_ == "_main_":
    with app.app_context:
        db.create_all()

    app.run(debug=True)