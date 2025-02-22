FROM python:3.10
ARG MONGODB_CONN_STRING

ENV MONGODB_CONN_STRING "$MONGODB_CONN_STRING"

WORKDIR /app

COPY app.py requirements.txt ./

#Adding the flask_blueprints
COPY flask_blueprints flask_blueprints 
COPY templates templates
COPY buzzy_bee_db buzzy_bee_db 

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade ./buzzy_bee_db

EXPOSE 5000

RUN python ./buzzy_bee_db/src/buzzy_bee_db/mongo_init.py

CMD ["python", "app.py"]
