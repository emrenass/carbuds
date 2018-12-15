import pika
import Backend_API.rabbitmq.config as cfg


def connection():
    credentials = pika.PlainCredentials(username=cfg.USERNAME, password=cfg.PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=cfg.HOST, port=cfg.PORT, credentials=credentials))
    return connection.channel()


def exchange_initialize(channel, exchange_name):
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type='fanout',
                             durable=True)


def init_queue(channel, exchange, binding_key=None):
    result = channel.queue_declare()
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=binding_key)
    return queue_name


# exp_time=60000 refers to 60 seconds
def send_message(channel, exchange, routing_keys, body, corr_id, exp_time='60000'):
    # String conversions for compatibility
    corr_id = str(corr_id)
    exp_time = str(exp_time)

    channel.basic_publish(exchange=exchange,
                          routing_key=routing_keys,
                          body=body,
                          mandatory=True,
                          properties=pika.BasicProperties(correlation_id=corr_id,
                                                          expiration=exp_time))
    print(" [x] Sent %r:%r" % (routing_keys, body))
    # connection().connection.close()
