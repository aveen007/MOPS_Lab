import pika,time, logging
# RabbitMQ setup
device_channels = {}
def create_connection():
    rabbitmq_host = 'rabbitmq'
    while True:
        try:
            credentials = pika.PlainCredentials('aveen', 'mops')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,virtual_host='/', credentials=credentials))
            logging.info("connected to rabbit mq")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("cannot connect to rabbit mq")
            time.sleep(2)
rmq_connection =create_connection()
def create_channel_for_device(connection, device_id):
    channel = connection.channel()
    channel.queue_declare(queue='validated_queue', durable=True)
    device_channels[device_id] = channel
    return channel
