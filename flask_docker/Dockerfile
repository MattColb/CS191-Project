FROM python:3.10

WORKDIR /app

COPY app.py requirements.txt ./

#Adding the flask_blueprints
COPY flask_blueprints flask_blueprints
COPY templates templates
COPY buzzy_bee_db buzzy_bee_db

RUN pip install 

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
