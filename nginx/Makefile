# Zertifikate generieren, falls nicht vorhanden
certs:
	mkdir -p deployments/nginx/certs
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout deployments/nginx/certs/nginx.key \
		-out deployments/nginx/certs/nginx.crt \
		-subj "/CN=localhost"

# 3. Reproduzierbarkeit: Projekt starten [4]
start-project: certs
	docker-compose up -d --build
	@echo "Grafana UI: http://localhost:3000"

# Projekt stoppen
stop-project:
	docker-compose down

# 5. Automation: Tests ausführen [4], [5]
test:
	bash tests/run_tests.sh