import io
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from flask import make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def generate_charts(JobApplication):
    # Generar gráficos
    fig, axs = plt.subplots(2, 2, figsize=(14, 12), gridspec_kw={'hspace': 0.5, 'wspace': 0.3})  # Tamaño de la figura más grande

    section_colors = ['#c7e9ff', '#7fc3ff', '#3ba0ff', '#f0ffff']  # Colores para cada sección

    # Dividir visualmente la figura en cuatro secciones y colorear el fondo de cada una
    for i in range(2):
        for j in range(2):
            axs[i, j].set_facecolor(section_colors[i*2+j])
            axs[i, j].patch.set_alpha(0.5)  # Ajuste de la transparencia del fondo

    # Gráfico 1: Top 5 Puestos de Trabajo Más Comunes
    puestos = [app.nombre_puesto for app in JobApplication.query.all()]
    puestos_counts = {puesto: puestos.count(puesto) for puesto in set(puestos)}
    top_puestos = sorted(puestos_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [puesto for puesto, _ in top_puestos]
    values = [count for _, count in top_puestos]
    axs[0, 0].bar(labels, values, color='#0077ff')  # Azul más oscuro
    axs[0, 0].set_title('Top 5 Puestos de Trabajo Más Comunes')
    axs[0, 0].set_xlabel('Puesto de Trabajo')
    axs[0, 0].set_ylabel('Cantidad')

    # Gráfico 2: Cantidad de Respuestas por Método de Postulación
    responses = JobApplication.query.filter_by(obtuvo_respuesta='SI').all()
    metodo_respuesta_counts = {app.metodo_postulacion: 0 for app in responses}
    for app in responses:
        metodo_respuesta_counts[app.metodo_postulacion] += 1
    axs[0, 1].bar(metodo_respuesta_counts.keys(), metodo_respuesta_counts.values(), color='#7fc3ff')  # Azul medio
    axs[0, 1].set_title('Cantidad de Respuestas por Método de Postulación')
    axs[0, 1].set_xlabel('Método de Postulación')
    axs[0, 1].set_ylabel('Cantidad')

    # Gráfico 3: Postulaciones por Método
    metodos = [app.metodo_postulacion for app in JobApplication.query.all()]
    metodo_counts = {metodo: metodos.count(metodo) for metodo in set(metodos)}
    sorted_metodos = sorted(metodo_counts.items(), key=lambda x: x[1], reverse=True)
    top_metodos = sorted_metodos[:4]
    otros_count = sum(count for _, count in sorted_metodos[4:])
    top_metodos.append(('Otros', otros_count))
    labels = [metodo for metodo, _ in top_metodos]
    values = [count for _, count in top_metodos]
    axs[1, 0].pie(values, labels=labels, autopct='%1.1f%%', colors=['#3ba0ff', '#7fc3ff', '#9ad7ff', '#c7e9ff','#6ca0ff'])  # Tonos de azul más claros
    axs[1, 0].set_title('Postulaciones por Método')

    # Gráfico 4: Obtención de Respuestas por Semana (barras)
    # Obtener solo las últimas 5 semanas
    four_weeks_ago = datetime.now() - timedelta(weeks=4)
    recent_applications = JobApplication.query.filter(JobApplication.fecha >= four_weeks_ago).order_by(JobApplication.fecha).all()

    respuestas_por_semana = defaultdict(lambda: {'SI': 0, 'NO': 0})

    for app in recent_applications:
        fecha = datetime.strptime(app.fecha, "%Y-%m-%d")
        semana = fecha - timedelta(days=fecha.weekday())
        semana_numero = int(semana.strftime("%U"))
        respuestas_por_semana[semana_numero][app.obtuvo_respuesta] += 1

    semanas_ordenadas = sorted(respuestas_por_semana.keys())
    respuestas_si = [respuestas_por_semana[semana]['SI'] for semana in semanas_ordenadas]
    respuestas_no = [respuestas_por_semana[semana]['NO'] for semana in semanas_ordenadas]
    etiquetas_semanas = [f"Semana {semana}" for semana in semanas_ordenadas]

    bar_width = 0.35
    index = range(len(semanas_ordenadas))
    bars1 = axs[1, 1].bar(index, respuestas_si, bar_width, label='Respuestas Positivas', color='#90ee90')  # light green
    bars2 = axs[1, 1].bar([i + bar_width for i in index], respuestas_no, bar_width, label='Respuestas Negativas', color='#ffc0cb')  # light red
    axs[1, 1].set_xlabel('Semana')
    axs[1, 1].set_ylabel('Cantidad de Respuestas')
    axs[1, 1].set_title('Obtención de Respuestas por Semana (Ultimas 4 semanas)')
    axs[1, 1].set_xticks([i + bar_width / 2 for i in index])
    axs[1, 1].set_xticklabels(etiquetas_semanas)
    axs[1, 1].legend([bars1, bars2], ['SI RESPONDIÓ', 'NO RESPONDIÓ'])

    # Ajuste del diseño y exportación de la imagen
    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
