import pika
import sys
import os
from  rabbitmq_code import send_message_to_queue
import psycopg2
import logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import connection_database 

app = FastAPI(title="Incident Management API")

# Enable CORS for cross-origin browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static assets if frontend directory exists
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

@app.get("/")
def serve_home():
    html_path = os.path.join(frontend_dir, "main.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Incident Management API is active. Frontend file not found."}



app_logger = logging.getLogger("application_function_logger")
app_logger.setLevel(logging.INFO)


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app_logger.addHandler(stream_handler)

# File handler for this function
fh = logging.FileHandler("application.log")
fh.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Attach handler to the logger
app_logger.addHandler(fh)


class IncidentRequest(BaseModel):
    department: str
    issue_type : str
    environment : str
    description : str
    priority_type : str




@app.post("/incident_create")
def create_incident(incident: IncidentRequest):
    DEPARTMENT = incident.department
    ISSUE = incident.issue_type
    ENVIRONMENT= incident.environment
    DESCRIPTION = incident.description
    PRIORITY= incident.priority_type
    try:
      connection = connection_database()
    except psycopg2.OperationalError as e:
      app_logger.critical(f"Database connection error: {e}")
    else:
      app_logger.info("Database connection established for incident creation")
      cur=connection.cursor()
      cur.execute("INSERT INTO incident_create (incident_id, DEPARTMENT, ISSUE , ENVIRONMENT , DESCRIPTION , PRIORITY ) VALUES ('inc' || nextval('incident_seq') , %s, %s, %s,%s ,%s)", (DEPARTMENT, ISSUE, ENVIRONMENT , DESCRIPTION , PRIORITY))
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
      send_message_to_queue(INCIDENT,DEPARTMENT, ISSUE , ENVIRONMENT , DESCRIPTION , PRIORITY)
      return "Incident created successfully"

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

@app.get("/incident_read/{incident_id}")
def read_single_incident(incident_id: str):
    try:
        connection = connection_database()
    except psycopg2.OperationalError as e:
        app_logger.critical(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failure")
    else:
        app_logger.info(f"Database connection established for reading incident {incident_id}")
        cur = connection.cursor()
        cur.execute("SELECT * FROM incident_create WHERE incident_id = %s", (incident_id,))
        result = cur.fetchone()
        cur.close()
        connection.close()
        app_logger.info("Database connection closed after single incident reading")
        if not result:
            raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
        return result
