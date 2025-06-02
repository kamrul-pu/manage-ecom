import os
import sys
import json
from decimal import Decimal
from typing import List

import pika

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django

django.setup()

from order.models import Order, OrderItem, ShippingAddress
from product.models import Product, MarketplaceProduct, Mapping
from store.models import Store


def main():
    try:
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
        channel.queue_declare(queue="order_queue", durable=True)

        def callback(ch, method, properties, body):
            try:
                order_data = json.loads(body)

                store_uid = order_data.get("store_uid")
                if not store_uid:
                    raise ValueError("Missing store ID in order data")

                store = Store.objects.get(id=store_uid)

                order = Order.objects.create(
                    store=store,
                    marketplace_order_id=order_data.get("marketplace_order_id", ""),
                    payment_status=order_data.get("payment_status", "PENDING").upper(),
                    payment_method=order_data.get("payment_method", ""),
                    purchase_date=order_data.get("purchase_date"),
                    currency=order_data.get("currency", "USD"),
                    total=Decimal(
                        order_data.get("order_meta", {}).get("subtotal_price", "0.00")
                    ),
                    marketplace=order_data.get("marketplace", "other"),
                    dispatch_status=order_data.get(
                        "dispatch_status", "OPEN_ORDER"
                    ).upper(),
                    dispatch_identifier=order_data.get("dispatch_identifier", ""),
                    dispatched_by=order_data.get("dispatched_by", ""),
                    dispatched_at=order_data.get("dispatched_at"),
                    shipped_at=order_data.get("shipped_at"),
                    order_meta=order_data.get("order_meta", {}),
                )
                print(f"Order {order.marketplace_order_id} created.")

                # === Order Items & Local SKU Mapping ===
                order_items_data = order_data.get("order_items", [])
                remote_skus = [item["remote_sku"] for item in order_items_data]

                marketplace_products = MarketplaceProduct.objects.filter(
                    sku__in=remote_skus,
                    store=store,
                )
                sku_to_marketplace_product = {mp.sku: mp for mp in marketplace_products}

                mappings = Mapping.objects.filter(
                    marketplace_product__in=marketplace_products,
                    store=store,
                ).select_related("product", "marketplace_product")

                remote_sku_to_local_sku = {
                    m.marketplace_product.sku: m.product.sku for m in mappings
                }

                order_items: List[OrderItem] = []
                for item_data in order_items_data:
                    remote_sku = item_data.get("remote_sku")
                    local_sku = remote_sku_to_local_sku.get(remote_sku, "")

                    order_items.append(
                        OrderItem(
                            order=order,
                            sku=remote_sku,
                            local_sku=local_sku,
                            quantity=item_data.get("quantity", 1),
                            price=Decimal(item_data.get("price", "0.00")),
                            total_amount=Decimal(item_data.get("price", "0.00"))
                            * item_data.get("quantity", 1),
                        )
                    )

                if order_items:
                    OrderItem.objects.bulk_create(order_items)
                    print(f"Created {len(order_items)} OrderItems.")
                else:
                    print("No order items found in the message.")

                # === Shipping Address ===
                shipping_data = order_data.get("shipping_address", {})
                if shipping_data:
                    ShippingAddress.objects.create(
                        order=order,
                        buyer_name=shipping_data.get("buyer_name", ""),
                        address1=shipping_data.get("address1", ""),
                        address2=shipping_data.get("address2", ""),
                        city=shipping_data.get("city", ""),
                        state=shipping_data.get("state", ""),
                        post_code=shipping_data.get("post_code", ""),
                        country=shipping_data.get("country", ""),
                        phone=shipping_data.get("phone", ""),
                        reference_id=shipping_data.get("reference_id"),
                        email=shipping_data.get("email", ""),
                    )
                    print("Shipping address saved.")
                else:
                    print("No shipping address found in the message.")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"Error processing message: {e}", file=sys.stderr)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="order_queue", on_message_callback=callback)
        print(" [*] Waiting for messages. Press CTRL+C to exit.")
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
