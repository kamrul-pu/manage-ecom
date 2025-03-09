import json
import pika
from django.core.management.base import BaseCommand
from django.db import transaction

# from order.models import Order, OrderItem, OrderShippingAddress  # Replace 'yourapp'
from order.serializers.order import OrderSerializer


class Command(BaseCommand):
    help = "Consume orders from RabbitMQ and save to database"

    def handle(self, *args, **options):
        credentials = pika.PlainCredentials("guest", "guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost", credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="order_queue", durable=True)

        def callback(ch, method, properties, body):
            try:
                order_data = json.loads(body)
                self.process_order(order_data)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                self.stderr.write(f"Error processing order: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="order_queue", on_message_callback=callback)
        self.stdout.write("Starting consumer... Press CTRL+C to exit")
        channel.start_consuming()

    def process_order(self, order_data):
        """Process and save order data."""
        with transaction.atomic():
            # Use serializer for validation and creation
            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save()
                self.stdout.write(
                    f"Order {order.channel_order_id} created successfully"
                )
            else:
                raise ValueError(f"Invalid order data: {serializer.errors}")
