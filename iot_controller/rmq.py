import pika,time
# RabbitMQ setup
device_channels = {}
def create_connection():
    rabbitmq_host = 'rabbitmq'
    while True:
        try:
            credentials = pika.PlainCredentials('aveen', 'mops')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,virtual_host='/', credentials=credentials))
            
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print("cannot connect because ",e)
            time.sleep(2)
rmq_connection =create_connection()
def create_channel_for_device(connection, device_id):
    channel = connection.channel()
    channel.queue_declare(queue='validated_queue', durable=True)
    device_channels[device_id] = channel
    return channel
# to_do : logging