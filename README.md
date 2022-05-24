# fastapi-microservices

# install virtualenv
python3 -m venv .venv

# activate virtualenv
source /.venv/bin/activate

# run fastapi app
uvicorn main:app --reload


# swagger url
http://localhost:8000/redoc
