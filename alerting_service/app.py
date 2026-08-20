import pika, sys , os
import multiprocessing
import json
import logging
import smtplib
from function import email_alert
from email.message import EmailMessage


alertworker_logger=logging.getLogger("alertworker_function_logger")
alertworker_logger.setLevel(logging.INFO)


console_log=logging.StreamHandler()
console_log.setLevel(logging.INFO)

file_log=logging.FileHandler("worker.log")
file_log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_log.setFormatter(formatter)
file_log.setFormatter(formatter)


alertworker_logger.addHandler(console_log)
alertworker_logger.addHandler(file_log)     

def main():
    credentials = pika.PlainCredentials('vishnu', 'bichu@#123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
    )
    channel = connection.channel()
    alertworker_logger.info("Connected to RabbitMQ server successfully")

    channel.queue_declare(
        queue='incident_queue_creation',
        durable=True,
        arguments={'x-queue-type': 'quorum'}
    )

    def callback(ch, method, properties, body):
        try:
            decode_body = body.decode('utf-8')
            converted_body = json.loads(decode_body)
            alertworker_logger.info("Message is converted for further processing")

            INCIDENT_ID = converted_body['IncidentId']
            DEPARTMENT = converted_body['Department']
            DESCRIPTION = converted_body['Issue']
            STATUS = converted_body['Status']

            alertworker_logger.info("Message was prepared for sending email alert")
            email_alert(INCIDENT_ID, DESCRIPTION, DEPARTMENT, STATUS)
            alertworker_logger.info("Email alert Incident creation was sent successfully")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            alertworker_logger.exception(f"Error processing RabbitMQ message: {exc}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(
        queue='incident_queue_creation',
        on_message_callback=callback,
        auto_ack=False
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


    
if __name__ == '__main__':
        try:
           main()
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
