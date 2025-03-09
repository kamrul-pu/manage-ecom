# Manage Multi platform Ecommerce


# Docker create rabbit mq
docker run -d   --name order-rabbitmq   -p 5674:5672   -p 15674:15672   -e RABBITMQ_DEFAULT_USER=kamrul   -e RABBITMQ_DEFAULT_PASS=kamrul   -e RABBITMQ_DEFAULT_VHOST=/   -v rabbitmq_data:/var/lib/rabbitmq   rabbitmq:3.13.6-management-alpine