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

# Project Summary
This app helps users find an optimal weight allocation among chosen stocks listed in the US market. It supports <br />
-Min-var (minimum variance/volatility) portfolio <br />
-max-return (maximum expected return) portfolio <br />
-max-sharpe (max return/volatility ratio) portfolio <br /><br />

Users can define multiple types of constraints: <br />
-sector constraint (ex: percentage weight of a specific sector is smaller/larger/equal to x%) <br />
-industry constraint <br />
-individual equity constraint (percentage weight of a specific stock is smaller/larger/equal to x%) <br />
Long only / No shorting <br /><br />

Work in progress: <br />
-Integrate interactive broker API & support portfolio sync <br />
-support auto-rebalancing rules <br />
-better error handling & caching strategy



