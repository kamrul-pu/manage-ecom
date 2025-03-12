import os
import sys

from decimal import Decimal

from typing import List, Dict
import pika
import json


# Dynamically add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "app.settings"
)  # Module path, not filesystem path
import django

django.setup()
from order.models import Order, OrderItem, OrderShippingAddress
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

                # Create the Order object
                # Channel id hardcoded to 4 for now
                order: Order = Order(
                    channel_id=4,
                    channel_order_id=order_data.get("channel_order_id", ""),
                    payment_status=order_data.get("payment_status", "PENDING").upper(),
                    payment_method=order_data.get("payment_method", ""),
                    purchase_date=order_data.get("purchase_date", None),
                    currency=order_data.get("currency", ""),
                    market_place=order_data.get("market_place", ""),
                    dispatch_status=order_data.get(
                        "dispatch_status", "PENDING"
                    ).upper(),
                    dispatch_identifier=order_data.get("dispatch_identifier", ""),
                    dispatched_by=order_data.get("dispatched_by", ""),
                    dispatched_at=order_data.get("dispatched_at", None),
                    shipped_at=order_data.get("shipped_at", None),
                    total=Decimal(
                        order_data.get("order_meta", {}).get(
                            "subtotal_price", Decimal("0.0")
                        )
                    ),
                    order_meta=order_data.get("order_meta", {}),
                )
                order.save()
                print(f"Order {order.channel_order_id} saved to database")

                # Prepare list of OrderItem objects for bulk create
                order_items: List[OrderItem] = [
                    OrderItem(
                        order=order,
                        sku=item_data.get("sku", ""),
                        quantity=item_data.get("quantity", 1),
                        price=Decimal(item_data.get("price", Decimal("0.0"))),
                        total_amount=item_data.get("quantity", 1)
                        * Decimal(item_data.get("price", Decimal("0.0"))),
                        position_item_ids=item_data.get("product_id", []),
                    )
                    for item_data in order_data.get("order_items", [])
                ]
                if order_items:
                    OrderItem.objects.bulk_create(order_items)
                    print(
                        f"Bulk created {len(order_items)} OrderItems for order {order.channel_order_id}"
                    )
                else:
                    print(
                        f"No Orderitems to create for order {order.channel_order_id}!!!"
                    )

                shipping_address = OrderShippingAddress(
                    order_id=order.id, **order_data.get("shipping_address", {})
                )
                shipping_address.save()
                if shipping_address:
                    print(
                        f"Shipping address created for order: {order.channel_order_id}"
                    )
                else:
                    print(
                        f"Failed to create shipping address for order: {order.channel_order_id}"
                    )

                ch.basic_ack(delivery_tag=method.delivery_tag)
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
