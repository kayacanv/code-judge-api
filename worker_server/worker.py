import json
import pika
import os
from Evaluator import Evaluator
import time


print('test test worker worker HEYYyY')
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))


def establish_connection(host, port, retry_interval=5, max_retries=12):
    attempts = 0
    while attempts < max_retries:
        try:
            # Attempt to connect to RabbitMQ
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port=port)
            )
            print("Connected to RabbitMQ")
            return connection
        except:
            attempts += 1
            wait_time = retry_interval * \
                (2 ** (attempts - 1))  # Exponential backoff
            print(
                f"Connection failed. Retry attempt {attempts} in {wait_time} seconds.")
            time.sleep(wait_time)
    raise Exception(
        f"Could not connect to RabbitMQ after {max_retries} attempts")


# Establish the RabbitMQ connection with retry logic
connection = establish_connection(rabbitmq_host, rabbitmq_port)

# Get the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='code_queue')

print('Connection Established')


def evaluate_code(ch, method, properties, body):
    # Parse the task data
    print('HEYYY NEW ONE ', body)

    task_data = json.loads(body)
    task_id = task_data['id']
    code = task_data['code']
    expected_output = task_data['expected_output']

    # Initialize Evaluator and evaluate the code
    evaluator = Evaluator()
    result = evaluator.evaluate(code, None, expected_output)

    # Print or log the result
    print(f"Task ID: {task_id}, Result: {result}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up RabbitMQ to consume from 'code_queue'
channel.basic_consume(queue='code_queue', on_message_callback=evaluate_code)

if __name__ == '__main__':
    print('Worker server started. Waiting for tasks...')
    channel.start_consuming()
