import pika

from callback import take_callback

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare('echo')

channel.basic_consume(queue='echo', on_message_callback=take_callback, auto_ack=True)

channel.start_consuming()