import pika
import json
import sys

try:
    # RabbitMQ connection with explicit port
    credentials = pika.PlainCredentials("kamrul", "kamrul")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5674,  # Match Docker port mapping
            credentials=credentials,
            virtual_host="/",  # Explicitly specify vhost
        )
    )
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue="order_queue", durable=True)

    # Payload
    order_data = {
        "channel": 2,
        "channel_order_id": "ORD1002",
        "payment_status": "PENDING",
        "payment_method": "PayPal",
        "purchase_date": "2025-03-09T11:00:00Z",
        "currency": "EUR",
        "company_uid": "COMP123",
        "dispatch_status": "PENDING",
        "dispatched_by": "550e8400-e29b-41d4-a716-446655440011",
        "order_items": [
            {"remote_sku": "P003", "quantity": 3, "price": 25.00},
            {"remote_sku": "P004", "quantity": 2, "price": 30.00},
        ],
        "shipping_address": {
            "buyer_name": "Jane Smith",
            "address1": "456 Market St",
            "address2": "",
            "city": "San Francisco",
            "state": "CA",
            "post_code": "94105",
            "country": "USA",
            "phone": "9876543210",
        },
    }

    # Publish message
    channel.basic_publish(
        exchange="",
        routing_key="order_queue",
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent
    )

    print("Order published to queue")
    connection.close()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Failed to connect to RabbitMQ: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    sys.exit(1)
