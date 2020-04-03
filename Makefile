ifdef env
	ENV=${env}
else
	ENV=local
endif

run:
	@if [ -n ${ENV} ] && ( [ "${ENV}" = local ] || [ "${ENV}" = prd ] );then echo "ENV: ${ENV}";else exit 1; fi
	cp ${ENV}.env .env
	docker-compose build
	docker-compose up -d
stop:
	docker-compose down
enter:
	docker-compose exec es_vis /bin/bash
log:
	docker-compose logs -f es_vis
log-nginx:
	docker-compose logs -f nginx
format:
	docker-compose run es_vis autopep8 -ivr .
test:
	docker-compose run v python -m unittest discover -v
lint:
	docker-compose run es_vis flake8 --show-source .