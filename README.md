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

# Tecnologías Utilizadas

- Docker: Para la contenerización del proyecto y facilitar su despliegue.
- Flask: Un framework de Python para crear aplicaciones web.
- SQLAlchemy: Una biblioteca de Python que facilita el trabajo con bases de datos relacionales desde Python.
- SQLite: Un sistema de gestión de bases de datos relacional incluido con Python.
- HTML/CSS: Para la estructura y el diseño de la interfaz de usuario.

## Instalación

Para el uso de esta aplicación debe tener instalado Docker en su sistema.
Puede hacerlo a través de la web oficial: https://docs.docker.com/get-docker/

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


### Formulario de Registro

Llena el formulario con la información de la postulación y haz clic en "Enviar" para guardar el registro. Si estás postulando a una empresa con un nombre similar al de una postulación previamente registrada, se te llevará a una pestaña con más información para que puedas confirmar si la nueva postulación es correcta o si se trata de una repetición.

### Visualizar Registros

Haz clic en "Ver Registros" para ver todas las postulaciones guardadas. Las filas están coloreadas alternadamente para una mejor visualización.

### Actualizar Respuesta

Haz clic en "Actualizar Respuesta" para cambiar el estado de respuesta de una postulación. Ingresa el ID de la postulación y selecciona si obtuviste respuesta ("SI" o "NO").

### Mostrar Gráficos

Haz clic en "Mostrar Gráficos" para ver gráficos de las postulaciones.

### Eliminar Registros

Haz clic en "Eliminar Registro" y proporciona el ID del registro que deseas eliminar. Confirma la eliminación del registro.

### Actualizar métodos de postulación

Puedes configurar los métodos de postulación según tus necesidades mediante un recuadro y botones en esa sección. Algunos vienen cargados por defecto, pero puedes agregar nuevos o eliminar existentes según tu preferencia.
