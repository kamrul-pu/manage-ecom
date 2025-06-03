import pika
import json
import sys

try:
    # RabbitMQ connection with explicit port
    # credentials = pika.PlainCredentials("kamrul", "kamrul")
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(
    #         host="localhost",
    #         port=5674,
    #         credentials=credentials,
    #         virtual_host="/",
    #     )
    # )
    # channel = connection.channel()
    # Rabbit MQ Server Connection
    url: str = (
        "amqps://gbriuwzj:xahrgtIjgs1zgR-qXCHRbK8BMWXXTXq0@possum.lmq.cloudamqp.com/gbriuwzj"
    )
    parameters = pika.URLParameters(url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare queue (durable)
    channel.queue_declare(queue="order_queue", durable=True)

    # Updated payload to match consumer expectation
    order_data = {
        "store_uid": "1987b409-1777-46e6-8c4e-b4374c6290ee",  # store ID (foreign key in Order model)
        "marketplace_order_id": "ORD1002",  # aligned with model field
        "payment_status": "PENDING",
        "payment_method": "PayPal",
        "purchase_date": "2025-03-09T11:00:00Z",
        "currency": "EUR",
        "marketplace": "Amazon",  # corrected key from "market_place"
        "dispatch_status": "OPEN_ORDER",
        "total": "135.00",
        "order_meta": {"subtotal_price": 135.00},
        "order_items": [
            {
                "marketplace_sku": "8629287785589",  # must match the consumer's expected key
                "quantity": 3,
                "price": 25.00,
                "picked_sku": "",
                "picked_item_type": "",
            },
            {
                "marketplace_sku": "9194835496273",
                "quantity": 2,
                "price": 30.00,
                "picked_sku": "",
                "picked_item_type": "",
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


# url: str = (
#     "amqps://gbriuwzj:xahrgtIjgs1zgR-qXCHRbK8BMWXXTXq0@possum.lmq.cloudamqp.com/gbriuwzj"
# )

# parameters = pika.URLParameters(url)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()

# channel.queue_declare(queue="hello")
# channel.basic_publish(exchange="", routing_key="hello", body="Hello CloudAMQP Test 2")
# print("Send hello cloudamqp Test 2")
# connection.close()
