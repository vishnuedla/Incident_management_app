import pika
import sys
import os
from  rabbitmq_code import send_message_to_queue
import psycopg2
import logging
from fastapi import FastAPI
from database import connection_database 


app = FastAPI()

app_logger = logging.getLogger("application_function_logger")
app_logger.setLevel(logging.INFO)

# File handler for this function
fh = logging.FileHandler("application.log")
fh.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

# Attach handler to the logger
app_logger.addHandler(fh)

@app.post("/incident_create")
def create_incident(DEPARTMENT,ISSUE,STATUS):
    try:
      connection = connection_database()
    except psycopg2.OperationalError as e:
      app_logger.critical(f"Database connection error: {e}")
    else:
      app_logger.info("Database connection established for incident creation")
      cur=connection.cursor()
      cur.execute("INSERT INTO incident_create (incident_id, DEPARTMENT, ISSUE, STATUS) VALUES ('inc' || nextval('incident_seq') , %s, %s, %s)", (DEPARTMENT, ISSUE, STATUS))
      connection.commit()
      # Fetch the incident_id of the newly created incident
      cur.execute("SELECT currval('incident_seq')")
      INCIDENT_ID = cur.fetchone()[0]
      INCIDENT= f"inc{INCIDENT_ID}"
      app_logger.info(f"Incident {INCIDENT} created successfully")
      cur.close()
      connection.close()
      app_logger.info("Database connection closed after incident creation")
      # Send message to RabbitMQ queue
      send_message_to_queue(INCIDENT,DEPARTMENT, ISSUE, STATUS)

@app.get("/incident_read")
def read_incident():
    try:
        connection = connection_database()
    except psycopg2.OperationalError as e:
        app_logger.critical(f"Database connection error: {e}")
    else:
      app_logger.info("Database connection established for incident reading")
      cur=connection.cursor()
      cur.execute("SELECT * FROM incident_create")
      result = cur.fetchall()
      cur.close()
      connection.close()
      app_logger.info("Database connection closed after incident reading")
      return result



