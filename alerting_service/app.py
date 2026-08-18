import pika, sys , os
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
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='incident_queue_creation', durable=True, arguments={'x-queue-type': 'quorum'})

    def callback(ch, method, properties, body): 
        decode_body = body.decode('utf-8')
        coverted_body= json.loads(decode_body)
        alertworker_logger.info("Message is coverted for futher processing")
        INCIDENT_ID= coverted_body['IncidentId']
        DEPARTMENT = coverted_body['Department']
        DESCRIPTION= coverted_body['Issue']
        STATUS= coverted_body['Status']
        alertworker_logger.info(f"Message was prepared for sending email alert")
        email_alert(INCIDENT_ID,DESCRIPTION,DEPARTMENT,STATUS)
        alertworker_logger.info(f"Email alert Incident creation was sent successfully")
        
        

        


    channel.basic_consume(queue='incident_queue_creation', on_message_callback=callback, auto_ack=True)
    
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
