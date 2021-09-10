# Local dev environment setup
`make local-mysql-start` <br />
run mysql server in docker at port 3306 <br />
`make python-install` <br />
install dependencies used by the flask app, pipenv is required <br />
`make init-db` <br />
initialize database schemas and update the schema to the most recent version <br />
`make local-backend` <br />
run the flask-app locally on port 5000 <br />
`make local-frontend` <br />
run react frontend locally visiable via port 3000 <br />

# Directory Structure
-python (Backend code) <br /> 
-api-doc (api examples which can be imported into Postman, might be replaced by a mock server) <br /> 
-migration (alembic configuration and schema related files) <br /> 



