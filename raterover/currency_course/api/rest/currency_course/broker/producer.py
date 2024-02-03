# import aio_pika
# import json
#
#
# class RabbitMQProducer:
#     def __init__(self, exchange_name, routing_key):
#         self.exchange_name = exchange_name
#         self.routing_key = routing_key
#
#     async def connect(self):
#         self.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
#         self.channel = await self.connection.channel()
#         self.exchange = await self.channel.declare_exchange(self.exchange_name, type='fanout')
#
#     async def send_message(self, data):
#         print(f"ПРОДЮСЕР {data}")
#         await self.exchange.publish(
#             aio_pika.Message(body=json.dumps(data).encode()),
#             routing_key=self.routing_key,
#         )
#
#     async def close(self):
#         await self.connection.close()
#
