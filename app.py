from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import difflib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages

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

    # Obtener todos los nombres de empresas de la base de datos
    existing_companies = [app.empresa for app in JobApplication.query.all()]

    # Buscar nombres de empresas similares
    similar_companies = difflib.get_close_matches(empresa, existing_companies, cutoff=0.7)  # Ajustar cutoff según sea necesario

    if similar_companies:
        # Mostrar un mensaje de advertencia y pedir confirmación
        return render_template('confirm.html', empresa=empresa, similar_companies=similar_companies,
                               metodo_postulacion=metodo_postulacion, comentarios=comentarios,
                               link=link, nombre_puesto=nombre_puesto)

    # Si no hay empresas similares, proceder a agregar el registro
    add_application(empresa, metodo_postulacion, comentarios, link, nombre_puesto)
    return redirect(url_for('index'))

@app.route('/confirm', methods=['POST'])
def confirm():
    empresa = request.form['empresa']
    metodo_postulacion = request.form['metodo_postulacion']
    comentarios = request.form.get('comentarios')
    link = request.form.get('link')
    nombre_puesto = request.form['nombre_puesto']

    add_application(empresa, metodo_postulacion, comentarios, link, nombre_puesto)
    return redirect(url_for('index'))

def add_application(empresa, metodo_postulacion, comentarios, link, nombre_puesto):
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

# Nueva ruta para mostrar y filtrar los registros
@app.route('/view_records')
def view_records():
    # Obtener todos los registros de la base de datos
    applications = JobApplication.query.all()
    
    # Obtener el parámetro 'rowsToColor' de la URL
    rows_to_color = request.args.get('rowsToColor', default=7, type=int)

    # Pasar el número de filas a colorear a la plantilla HTML
    return render_template('view_records.html', applications=applications, rowsToColor=rows_to_color)

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)