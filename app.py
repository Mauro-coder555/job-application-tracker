from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from datetime import datetime,timedelta
import os
import difflib
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from charts import generate_charts


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
    obtuvo_respuesta = db.Column(db.String(2), nullable=False, default='NO')

# Crea la base de datos y las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    with open('config/metodos_postulacion.txt', 'r', encoding='utf-8') as file:
        metodos_postulacion = [line.strip().lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for line in file.readlines()]

    return render_template('index.html', metodos_postulacion=metodos_postulacion)

# Ruta para manejar el envío del formulario
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    app.logger.debug(f'Received data: {data}')
    empresa = request.form['empresa']
    metodo_postulacion = request.form.get('metodo_postulacion')
    comentarios = request.form.get('comentarios')
    link = request.form.get('link')
    nombre_puesto = request.form['nombre_puesto']

    # Obtener todos los nombres de empresas de la base de datos
    all_companies = JobApplication.query.all()

    # Buscar nombres de empresas similares
    similar_companies = [app for app in all_companies if difflib.get_close_matches(empresa, [app.empresa], cutoff=0.7)]

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

# Ruta para mostrar y filtrar los registros
@app.route('/view_records')
def view_records():
    # Obtener todos los registros de la base de datos
    applications = JobApplication.query.all()
    
    # Obtener el parámetro 'rowsToColor' de la URL
    rows_to_color = request.args.get('rowsToColor', default=7, type=int)

    # Pasar el número de filas a colorear a la plantilla HTML
    return render_template('view_records.html', applications=applications, rowsToColor=rows_to_color)

# Ruta para actualizar estado de respuesta a una postulacion
@app.route('/update_response',methods=['POST','GET'])
def update_response():
    if request.method == 'POST':
        id = request.form['id']
        obtuvo_respuesta = request.form['obtuvo_respuesta']
        
        # Actualizar el registro en la base de datos
        application = JobApplication.query.get(id)
        if application:
            application.obtuvo_respuesta = obtuvo_respuesta
            db.session.commit()
            flash('Respuesta actualizada exitosamente!', 'success')
        else:
            flash('No se encontró una aplicación con ese ID', 'error')
        
        return redirect(url_for('view_records'))
    return render_template('update_response.html')

@app.route('/show_charts')
def show_charts():
    return render_template('charts.html')

@app.route('/chart_image')
def chart_image():
    return generate_charts(JobApplication)

# Ruta para mostrar el formulario de eliminación
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        application = JobApplication.query.get(id)
        if application:
            return render_template('delete_confirm.html', application=application)
        else:
            flash('No se encontró una aplicación con ese ID', 'error')
            return redirect(url_for('delete'))
    return render_template('delete.html')

# Ruta para confirmar la eliminación
@app.route('/delete_confirm', methods=['POST'])
def delete_confirm():
    id = request.form['id']
    application = JobApplication.query.get(id)
    if application:
        db.session.delete(application)
        db.session.commit()
        flash('Registro eliminado exitosamente!', 'success')
    else:
        flash('No se encontró una aplicación con ese ID', 'error')
    return redirect(url_for('index'))


# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)