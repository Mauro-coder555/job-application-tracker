# Job Application Tracker

Este proyecto es una aplicación web simple para rastrear las postulaciones de trabajo. Utiliza Flask como framework web y SQLAlchemy para manejar la base de datos SQLite. La aplicación está empaquetada y ejecutada dentro de un contenedor Docker.

# Estructura del proyecto

| Directorio | Descripción |
|---|---|
| `app.py` | Archivo principal de la aplicación Flask |
| `db` | Directorio para almacenar la base de datos SQLite |
| `Dockerfile` | Archivo Docker para construir la imagen |
| `requirements.txt` | Archivo de requisitos de Python |
| `static` | Directorio para archivos estáticos |
| `logo.png` | Imagen para fines estéticos |
| `templates` | Directorio de plantillas HTML |
| `index.html` | Plantilla HTML para el formulario de solicitudes |
| `view_records.html` | Plantilla HTML para visualizar los registros |

## Características

- Registrar postulaciones de trabajo con información como la empresa, método de postulación, comentarios, link y nombre del puesto.
- Visualizar todas las aplicaciones registradas en una tabla.

# Tecnologías Utilizadas

- Docker: Para la contenerización del proyecto y facilitar su despliegue.
- Flask: Un framework de Python para crear aplicaciones web.
- SQLAlchemy: Una biblioteca de Python que facilita el trabajo con bases de datos relacionales desde Python.
- SQLite: Un sistema de gestión de bases de datos relacional incluido con Python.
- HTML/CSS: Para la estructura y el diseño de la interfaz de usuario.

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/tuusuario/job-application-tracker.git
cd job-application-tracker
```

## Construir la imagen Docker
```bash
docker build -t job_application_tracker .
```
## Ejecutar el contenedor Docker
```bash
docker run -p 5000:5000 -v "$(pwd)/db:/app/db" job_application_tracker
```
##  Uso

Acceder a la aplicación
La aplicación estará disponible en http://localhost:5000.

## Cargar una nueva postulacion
Completa el formulario en la página principal y haz clic en "Enviar".

## Ver registros de aplicaciones
Accede a http://localhost:5000/view_records para ver todas las aplicaciones registradas en una tabla.