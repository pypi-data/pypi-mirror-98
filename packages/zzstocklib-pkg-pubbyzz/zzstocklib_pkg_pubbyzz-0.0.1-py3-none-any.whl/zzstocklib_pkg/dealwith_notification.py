import pika
from propertiesUtility import properties

prop = properties
print(prop.get('rabbitMQ_Host'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=prop.get('rabbitMQ_Host')))
channel = connection.channel()

channel.exchange_declare(exchange='directexchangenotifcation',
                         exchange_type='direct')

result = channel.queue_declare(queue=prop.get('notification_queue_name'), exclusive=True)
queue_name = result.method.queue
print(queue_name)

channel.queue_bind(exchange='directexchangenotifcation',
                   queue=queue_name,
                   routing_key = "msg")

print(' [*] Waiting for info. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(queue=queue_name,
					  on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()