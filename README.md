# Job Application Tracker

Este proyecto es una aplicación web simple para rastrear las postulaciones de trabajo. Utiliza Flask como framework web y SQLAlchemy para manejar la base de datos SQLite. La aplicación está empaquetada y ejecutada dentro de un contenedor Docker.

# Estructura del proyecto

| Directorio | Descripción |
|---|---|
| `app.py` | Archivo principal de la aplicación Flask |
| `charts.py` | Archivo con lógica para graficar estado de postulaciones |
| `db` | Directorio para almacenar la base de datos SQLite |
| `Dockerfile` | Archivo Docker para construir la imagen |
| `requirements.txt` | Archivo de requisitos de Python |
| `static` | Directorio para archivos estáticos |
| `logo.png` | Imagen para fines estéticos |
| `templates` | Directorio de plantillas HTML |
| `index.html` | Plantilla HTML para el formulario de solicitudes |


## Características

- Registrar postulaciones de trabajo con información como la empresa, método de postulación, comentarios, link, nombre del puesto y estado de respuesta.
- Visualizar todas las aplicaciones registradas en una tabla.
- Visualizar gráficas para analizar el recorrido y planificar estrategias acordes.

## Tecnologías Utilizadas

- [![Docker](https://img.shields.io/badge/Docker-blue.svg?style=flat)](https://www.docker.com/) Para la contenerización del proyecto y facilitar su despliegue.

- [![Flask](https://img.shields.io/badge/Flask-orange.svg?style=flat)](https://flask.palletsproject.com/) Un framework de Python para crear aplicaciones web.

- [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-green.svg?style=flat)](https://www.sqlalchemy.org/) Una biblioteca de Python que facilita el trabajo con bases de datos relacionales desde Python.

- [![SQLite](https://img.shields.io/badge/SQLite-red.svg?style=flat)](https://www.sqlite.org/) Un sistema de gestión de bases de datos relacional incluido con Python.

- [![HTML5](https://img.shields.io/badge/HTML5-orange.svg?style=flat)](https://www.w3.org/TR/html5/) [![CSS3](https://img.shields.io/badge/CSS3-blue.svg?style=flat)](https://www.w3.org/TR/css3/) Para la estructura y el diseño de la interfaz de usuario.

## Instalación

Para el uso de esta aplicación debe tener Docker instalado e iniciado en su sistema.
Puede hacerlo a través de la web oficial: https://docs.docker.com/get-docker/

### Clonar el repositorio

* En Windows: Abre la terminal de Git Bash haciendo clic derecho y seleccionando "Git Bash Here" dentro de la carpeta de tu preferencia.

* En Linux: Abre la terminal convencional dentro de la carpeta de tu preferencia.

#### Ejecuta los siguientes comandos:

```bash
git clone https://github.com/Mauro-coder555/job-application-tracker.git
cd job-application-tracker
```

## Construir la imagen Docker<a id="construir-imagen-docker"></a>
```bash
docker build -t job_application_tracker .
```
## Ejecutar el contenedor Docker
```bash
docker run -p 5000:5000 -v "$(pwd)/db:/app/db" job_application_tracker
```
##  Uso

### Acceder a la aplicación.
La aplicación estará disponible en http://localhost:5000.


### Formulario de Registro

Llena el formulario con la información de la postulación y haz clic en "Enviar" para guardar el registro. Si estás postulando a una empresa con un nombre similar al de una postulación previamente registrada, se te llevará a una pestaña con más información para que puedas confirmar si la nueva postulación es correcta o si se trata de una repetición.

### Visualizar Registros

Haz clic en "Ver Registros" para ver todas las postulaciones guardadas. Las filas están coloreadas alternadamente para distinguir los registros consecutivos de dias distintos en los que se hizo una postulación.

### Actualizar Respuesta

Haz clic en "Actualizar Respuesta" para cambiar el estado de respuesta de una postulación. Ingresa el ID de la postulación y selecciona si obtuviste respuesta ("SI" o "NO").

### Mostrar Gráficos

Haz clic en "Mostrar Gráficos" para ver gráficos de las postulaciones.

### Eliminar Registros

Haz clic en "Eliminar Registro" y proporciona el ID del registro que deseas eliminar. Confirma la eliminación del registro.

### Configurar métodos de postulación

Los métodos de postulación disponibles en la página principal se configuran mediante el archivo metodos_postulacion.txt ubicado en la carpeta config. En cada línea del archivo, escriba el nombre de un método de postulación para habilitarlo. El programa se encargará de mostrarlos en la aplicación de forma estandarizada (en minúsculas, sin tildes y con guiones bajos en lugar de espacios). Agregue o elimine líneas para gestionar la lista de métodos. Los cambios se aplican al re-construir la imagen y ejecutar nuevamente el contenedor como fue indicado en esta [sección.](#construir-imagen-docker)

