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

from order.choices import DispatchStatus
from order.models import Order, OrderItem, ShippingAddress
from product.models import Product, MarketplaceProduct, Mapping
from store.models import Store
from inventory.models import Stock


def update_related_stock(order, order_items):
    for item in order_items:
        stock = Stock.objects.get(sku=item.local_sku).first()
        if stock:
            quantity = item.quantity

            if (
                order.dispatch_status == DispatchStatus.OPEN_ORDER
                or order.dispatch_status == DispatchStatus.PENDING
            ):
                stock.in_open += quantity
            elif order.dispatch_status == DispatchStatus.CANCELLED:
                stock.in_open = max(0, stock.in_open - quantity)
            elif order.dispatch_status == DispatchStatus.DISPATCHED:
                stock.in_open = max(0, stock.in_open - quantity)
                stock.stock_level = max(0, stock.stock_level - quantity)

            stock.available = max(0, stock.stock_level - stock.in_open)
            stock.save()
            print(
                f"✅ Stock updated for product local: {item.local_sku} Marketplace: {item.sku}"
            )
        else:
            print(
                f"Stock not found for this local: {item.local_sku} Marketplace: {item.sku}"
            )


def main():
    try:
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
        # Queue From CloudAmqp Server
        url: str = (
            "amqps://gbriuwzj:xahrgtIjgs1zgR-qXCHRbK8BMWXXTXq0@possum.lmq.cloudamqp.com/gbriuwzj"
        )
        parameters = pika.URLParameters(url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue="order_queue", durable=True)

        def callback(ch, method, properties, body):
            try:
                order_data = json.loads(body)

                store_uid = order_data.get("store_uid")
                if not store_uid:
                    raise ValueError("Missing store ID in order data")
                try:
                    store = Store.objects.get(uid=store_uid)
                except Exception as e:
                    print("Invalid store uid ", str(e))
                    store = None

                order = Order.objects.create(
                    store=store,
                    marketplace_order_id=order_data.get("marketplace_order_id", ""),
                    payment_status=order_data.get("payment_status", "PENDING").upper(),
                    payment_method=order_data.get("payment_method", ""),
                    purchase_date=order_data.get("purchase_date"),
                    currency=order_data.get("currency", "USD"),
                    # total=Decimal(
                    #     order_data.get("order_meta", {}).get("subtotal_price", "0.00")
                    # ),
                    total=Decimal(order_data.get("total", "0.00")),
                    marketplace=order_data.get("marketplace", "OTHER"),
                    dispatch_status=order_data.get(
                        "dispatch_status", "OPEN_ORDER"
                    ).upper(),
                    # dispatch_identifier=order_data.get("dispatch_identifier", ""),
                    # dispatched_by=order_data.get("dispatched_by", ""),
                    # dispatched_at=order_data.get("dispatched_at"),
                    # shipped_at=order_data.get("shipped_at"),
                    order_meta=order_data.get("order_meta", {}),
                )
                print(f"Order {order.marketplace_order_id} created.")

                # === Order Items & Local SKU Mapping ===
                order_items_data = order_data.get("order_items", [])
                marketplace_skus = [
                    item["marketplace_sku"] for item in order_items_data
                ]

                marketplace_products = MarketplaceProduct.objects.filter(
                    sku__in=marketplace_skus,
                    # store=store,
                )

                mappings = Mapping.objects.filter(
                    marketplace_product__in=marketplace_products,
                    # store=store,
                ).select_related("product", "marketplace_product")
                print("mappings: ", mappings)
                marketplace_sku_to_local_sku = {
                    m.marketplace_product.sku: m.product.sku for m in mappings
                }
                print("marketplace sku to local sku: ", marketplace_sku_to_local_sku)

                order_items: List[OrderItem] = []
                for item_data in order_items_data:
                    marketplace_sku = item_data.get("marketplace_sku")
                    local_sku = marketplace_sku_to_local_sku.get(marketplace_sku, "")

                    order_items.append(
                        OrderItem(
                            order=order,
                            sku=marketplace_sku,
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
                    update_related_stock(order, order_items)
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


# Order with update mechanism

# from django.utils.dateparse import parse_datetime
# from django.utils.timezone import now

# def callback(ch, method, properties, body):
#     try:
#         order_data = json.loads(body)
#         store_uid = order_data.get("store_uid")
#         if not store_uid:
#             raise ValueError("Missing store ID in order data")

#         try:
#             store = Store.objects.get(uid=store_uid)
#         except Store.DoesNotExist:
#             print("Invalid store UID")
#             ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
#             return

#         marketplace_order_id = order_data.get("marketplace_order_id", "")
#         existing_order = Order.objects.filter(marketplace_order_id=marketplace_order_id).first()

#         order_fields = {
#             "store": store,
#             "payment_status": order_data.get("payment_status", "PENDING").upper(),
#             "payment_method": order_data.get("payment_method", ""),
#             "purchase_date": parse_datetime(order_data.get("purchase_date")),
#             "currency": order_data.get("currency", "USD"),
#             "total": Decimal(order_data.get("total", "0.00")),
#             "marketplace": order_data.get("marketplace", "OTHER"),
#             "dispatch_status": order_data.get("dispatch_status", "OPEN_ORDER").upper(),
#             "order_meta": order_data.get("order_meta", {}),
#         }

#         if existing_order:
#             # Update the order
#             for key, value in order_fields.items():
#                 setattr(existing_order, key, value)
#             existing_order.save()
#             order = existing_order
#             print(f"Order {order.marketplace_order_id} updated.")
#         else:
#             # Create a new order
#             order = Order.objects.create(
#                 marketplace_order_id=marketplace_order_id,
#                 **order_fields
#             )
#             print(f"Order {order.marketplace_order_id} created.")

#         # === Order Items ===
#         order_items_data = order_data.get("order_items", [])
#         marketplace_skus = [item["marketplace_sku"] for item in order_items_data]

#         marketplace_products = MarketplaceProduct.objects.filter(
#             sku__in=marketplace_skus,
#             store=store,
#         )

#         mappings = Mapping.objects.filter(
#             marketplace_product__in=marketplace_products,
#             store=store,
#         ).select_related("product", "marketplace_product")

#         marketplace_sku_to_local_sku = {
#             m.marketplace_product.sku: m.product.sku for m in mappings
#         }

#         # Existing items in DB
#         existing_items = {item.sku: item for item in order.order_items.all()}
#         new_skus = set()

#         for item_data in order_items_data:
#             marketplace_sku = item_data.get("marketplace_sku")
#             local_sku = marketplace_sku_to_local_sku.get(marketplace_sku, "")

#             quantity = item_data.get("quantity", 1)
#             price = Decimal(item_data.get("price", "0.00"))
#             total_amount = price * quantity

#             new_skus.add(marketplace_sku)

#             if marketplace_sku in existing_items:
#                 # Update existing item
#                 item = existing_items[marketplace_sku]
#                 item.local_sku = local_sku
#                 item.quantity = quantity
#                 item.price = price
#                 item.total_amount = total_amount
#                 item.save()
#             else:
#                 # Create new item
#                 OrderItem.objects.create(
#                     order=order,
#                     sku=marketplace_sku,
#                     local_sku=local_sku,
#                     quantity=quantity,
#                     price=price,
#                     total_amount=total_amount,
#                 )

#         # Remove order items that are no longer in the updated list
#         for sku, item in existing_items.items():
#             if sku not in new_skus:
#                 item.delete()

#         print(f"Order items synced. {len(new_skus)} current item(s).")

#         # === Shipping Address ===
#         shipping_data = order_data.get("shipping_address", {})
#         if shipping_data:
#             shipping_address, created = ShippingAddress.objects.update_or_create(
#                 order=order,
#                 defaults={
#                     "buyer_name": shipping_data.get("buyer_name", ""),
#                     "address1": shipping_data.get("address1", ""),
#                     "address2": shipping_data.get("address2", ""),
#                     "city": shipping_data.get("city", ""),
#                     "state": shipping_data.get("state", ""),
#                     "post_code": shipping_data.get("post_code", ""),
#                     "country": shipping_data.get("country", ""),
#                     "phone": shipping_data.get("phone", ""),
#                     "reference_id": shipping_data.get("reference_id"),
#                     "email": shipping_data.get("email", ""),
#                 },
#             )
#             print("Shipping address updated.")
#         else:
#             print("No shipping address provided.")

#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     except Exception as e:
#         print(f"Error processing message: {e}", file=sys.stderr)
#         ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
