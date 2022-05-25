# fastapi-microservices

# install virtualenv
 - python3 -m venv .venv

# activate virtualenv
 - source /.venv/bin/activate

# install requirements
 - pip install -r requirements.txt


# run fastapi app
# when other databases
 - uvicorn main:app --reload

# same database
#inventory app:
 - uvicorn main:app --reload --port=8000

#payment app: 
 - uvicorn main:app --reload --port=8001


# swagger url
 - http://localhost:8000/redoc
