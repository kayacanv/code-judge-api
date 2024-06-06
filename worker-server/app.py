import json
import redis
import pika
import boto3
import gzip
import io
from isolate import Isolate

r = redis.Redis(host='localhost', port=6379, db=0)
queue_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = queue_connection.channel()
channel.queue_declare(queue='code_queue')

s3 = boto3.client('s3')

def download_from_s3(file_name):
    response = s3.get_object(Bucket='your-bucket-name', Key=file_name)
    compressed_content = response['Body'].read()
    return gzip.decompress(compressed_content).decode()

def evaluate_code(ch, method, properties, body):
    task_data = json.loads(body)
    task_id = task_data['id']
    code = task_data['code']
    input_url = task_data['input_url']
    expected_output = task_data['expected_output']

    input_file_name = input_url.split('/')[-1]
    input_data = download_from_s3(input_file_name)

    isolate_instance = Isolate()
    result = isolate_instance.run(code, input_data)

    output = result['stdout']
    status = 'success' if output.strip() == expected_output.strip() else 'failure'

    r.set(task_id, json.dumps({
        'status': status,
        'output': output,
        'expected_output': expected_output
    }))

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='code_queue', on_message_callback=evaluate_code)

if __name__ == '__main__':
    print('Worker server started. Waiting for tasks...')
    channel.start_consuming()
