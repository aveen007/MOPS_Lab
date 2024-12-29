from flask import Flask, request, jsonify
from pymongo import MongoClient
import pika
import json

app = Flask(__name__)

# MongoDB setup
# mongo_client = MongoClient("mongodb://mongodb:27017/")
# db = mongo_client.iot_db
# packets_collection = db.packets

# RabbitMQ setup
# rabbitmq_host = 'rabbitmq'
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
# channel = connection.channel()
# channel.queue_declare(queue='rules_queue')

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    # Validate data (simple validation)
    if 'device_id' in data and 'name' in data and 'email' in data and 'age' in data and 'x_factor' in data:
        # Save to MongoDB
        # packets_collection.insert_one(data)
        # Send to RabbitMQ for rule evaluation
        # channel.basic_publish(exchange='', routing_key='rules_queue', body=json.dumps(data))
        print(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
