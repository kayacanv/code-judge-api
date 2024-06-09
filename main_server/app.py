from flask import Flask, request, jsonify
import uuid
import json
import pika
import os
import time
from error_handlers import register_error_handlers
from custom_exceptions import MissingParameterError


print('can you see thisss')
time.sleep(10)
app = Flask(__name__)
register_error_handlers(app)


rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))

# Setup RabbitMQ connection
queue_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))

channel = queue_connection.channel()
channel.queue_declare(queue='code_queue')


@app.route('/evaluate', methods=['POST'])
def evaluate_code():
    data = request.json
    print(data)
    code = data.get('code')
    input_data = data.get('input')
    expected_output = data.get('expected_output')
    if code is None:
        raise MissingParameterError('code')
    if expected_output is None:
        raise MissingParameterError('expected_output')

    task_id = str(uuid.uuid4())

    task_data = {
        'id': task_id,
        'code': code,
        'expected_output': expected_output
    }

    # Send task to the RabbitMQ queue
    channel.basic_publish(
        exchange='', routing_key='code_queue', body=json.dumps(task_data))
    return jsonify({'task_id': task_id}), 202

# No need for the /result/<task_id> endpoint as we're not storing results in Redis anymore


@app.route('/test', methods=['POST'])
def test_api():
    return jsonify({'Hey': 'hi!!!'}), 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
