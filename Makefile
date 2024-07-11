.PHONY: run

run:
	@docker run -p 5000:5000 -v "$(pwd)/db:/app/db" job_application_tracker
