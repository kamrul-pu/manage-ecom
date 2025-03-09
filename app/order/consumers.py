import pika
import json
import sys
import os

# Dynamically add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "app.settings"
)  # Module path, not filesystem path
import django

django.setup()
from order.models import Order
from order.serializers.order import OrderSerializer


# Rest of your code...
def main():
    try:
        credentials = pika.PlainCredentials("kamrul", "kamrul")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost", port=5674, credentials=credentials, virtual_host="/"
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue="order_queue", durable=True)

        def callback(ch, method, properties, body):
            try:
                order_data = json.loads(body)
                print("order data: ", order_data)
                serializer = OrderSerializer(data=order_data)
                if serializer.is_valid():
                    serializer.save()
                    print(f"Order {order_data['channel_order_id']} saved to database")
                else:
                    print(f"Invalid order data: {serializer.errors}", file=sys.stderr)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print("order data: ", order_data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode message: {e}", file=sys.stderr)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                print(f"Error processing order: {e}", file=sys.stderr)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="order_queue", on_message_callback=callback)
        print("Starting consumer... Press CTRL+C to exit")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Consumer stopped by user")
        connection.close()
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
