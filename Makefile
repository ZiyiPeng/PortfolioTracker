build-frontend:
	cd frontend; npm run build

local-frontend:
	cd frontend; npm run start

python-install:
	pipenv install

local-backend: python-install local-mysql-start
	pipenv run flask run

init-db:
	flask db init; flask db migrate; flask db upgrade

local-mysql-start:
	docker start mysql || docker run --name mysql \
		-e MYSQL_ROOT_PASSWORD=Passw0rd \
	 	-e MYSQL_DATABASE=port-tracker \
	 	-d -p 3306:3306 mysql:8.0

local-mysql-stop:
	docker stop mysql