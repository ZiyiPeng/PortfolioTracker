build-frontend:
	cd frontend; npm run build

local-frontend:
	cd frontend; npm run start

python-install:
	cd python; pipenv install

init-db:
	flask db init; flask db migrate; flask db upgrade