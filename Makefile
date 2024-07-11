.PHONY: build run stop

build:
	docker build -t job_application_tracker .

run:
	@CONTAINER_ID=$$(docker run -d -p 5000:5000 -v "$(pwd)/db:/app/db" job_application_tracker); \
	echo "Contenedor iniciado. Accede a la aplicación en: \033[1mhttp://localhost:5000\033[0m"

stop:
	@docker stop $$(docker ps -q --filter ancestor=job_application_tracker) > /dev/null && \
	echo "Contenedor detenido correctamente."