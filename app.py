from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configurar la base de datos SQLite
file_path = os.path.abspath(os.getcwd())+"/db/applications.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    metodo_postulacion = db.Column(db.String(100), nullable=False)
    comentarios = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(200), nullable=True)
    nombre_puesto = db.Column(db.String(100), nullable=False)

# Crea la base de datos y las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el envío del formulario
@app.route('/submit', methods=['POST'])
def submit():
    empresa = request.form['empresa']
    metodo_postulacion = request.form['metodo_postulacion']
    comentarios = request.form.get('comentarios')
    link = request.form.get('link')
    nombre_puesto = request.form['nombre_puesto']

    now = datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d")

    new_application = JobApplication(
        empresa=empresa,
        fecha=fecha_actual,
        metodo_postulacion=metodo_postulacion,
        comentarios=comentarios,
        link=link,
        nombre_puesto=nombre_puesto
    )

    db.session.add(new_application)
    db.session.commit()

    return redirect(url_for('index'))

# Nueva ruta para mostrar y filtrar los registros
@app.route('/view_records')
def view_records():
    # Obtener todos los registros de la base de datos
    applications = JobApplication.query.all()
    return render_template('view_records.html', applications=applications)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
