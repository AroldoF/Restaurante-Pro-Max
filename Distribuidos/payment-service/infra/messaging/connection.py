import pika

def get_connection():

    credentials = pika.PlainCredentials(
        username="guest",
        password="guest"
    )

    parameters = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=credentials,
    )

    return pika.BlockingConnection(parameters)