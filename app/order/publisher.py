import pika
import json
import sys

try:
    # RabbitMQ connection with explicit port
    credentials = pika.PlainCredentials("kamrul", "kamrul")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5674,
            credentials=credentials,
            virtual_host="/",
        )
    )
    channel = connection.channel()

    # Declare queue (durable)
    channel.queue_declare(queue="order_queue", durable=True)

    # Updated payload to match consumer expectation
    order_data = {
        "store_uid": 4,  # store ID (foreign key in Order model)
        "marketplace_order_id": "ORD1002",  # aligned with model field
        "payment_status": "PENDING",
        "payment_method": "PayPal",
        "purchase_date": "2025-03-09T11:00:00Z",
        "currency": "EUR",
        "marketplace": "Amazon",  # corrected key from "market_place"
        "dispatch_status": "OPEN_ORDER",
        "dispatched_by": "550e8400-e29b-41d4-a716-446655440011",
        "dispatched_at": None,
        "shipped_at": None,
        "order_meta": {"subtotal_price": 135.00},
        "order_items": [
            {
                "remote_sku": "P003",  # must match the consumer's expected key
                "quantity": 3,
                "price": 25.00,
                "picked_sku": "P003-PICKED",
                "picked_item_type": "MANUAL",
            },
            {
                "remote_sku": "P004",
                "quantity": 2,
                "price": 30.00,
                "picked_sku": "P004-PICKED",
                "picked_item_type": "AUTO",
            },
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
            "email": "jane@example.com",
            "reference_id": "ADDR-002",
        },
    }

    # Publish message
    channel.basic_publish(
        exchange="",
        routing_key="order_queue",
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent
    )

    print("✅ Order published to queue.")
    connection.close()

except pika.exceptions.AMQPConnectionError as e:
    print(f"❌ Failed to connect to RabbitMQ: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}", file=sys.stderr)
    sys.exit(1)
