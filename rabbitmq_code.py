import json
import pika
import logging


rabbitmq_logger = logging.getLogger("rabbitmq_function_logger")
rabbitmq_logger.setLevel(logging.INFO)

# File handler for this function
fh = logging.FileHandler("application.log")
fh.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

# Attach handler to the logger
rabbitmq_logger.addHandler(fh)
  
def send_message_to_queue(incident_id , DEPARTMENT,ISSUE,STATUS):


   incident_store = {
      "IncidentId": incident_id,
      "Department": DEPARTMENT,
      "Issue": ISSUE, 
      "Status": STATUS
   }
   rabbitmq_logger.info(f"Preparing to send message to RabbitMQ queue")   
   incident_message= json.dumps(incident_store)
   rabbitmq_logger.info(f"Message prepared for RabbitMQ queue")

  
   credentials = pika.PlainCredentials('vishnu', 'bichu@#123')
   connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
   rabbitmq_logger.info("RabbitMQ connection established")
   channel = connection.channel()
   channel.queue_declare(queue='incident_queue_creation', durable=True, arguments={'x-queue-type': 'quorum'})
   channel.basic_publish(exchange='',
                      routing_key='incident_queue_creation',
                      body= incident_message, properties=pika.BasicProperties(
            delivery_mode=2)
            )
   rabbitmq_logger.info(f"Message sent to RabbitMQ queue for futher processing")
   connection.close()
   rabbitmq_logger.info("RabbitMQ connection closed after sending message")
