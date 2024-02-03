# import aio_pika
# import json
#
# from raterover.currency_course.api.rest.currency_course.binance.handler import update_currency_course
#
#
# class RabbitMQConsumer:
#     def __init__(self, queue_name, exchange_name, request):
#         self.queue_name = queue_name
#         self.exchange_name = exchange_name
#         self.request = request
#
#     async def connect(self):
#         self.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
#         self.channel = await self.connection.channel()
#         self.exchange = await self.channel.declare_exchange(self.exchange_name, type='fanout')
#
#         queue = await self.channel.declare_queue(self.queue_name, durable=True)
#         await queue.bind(self.exchange)
#
#         await queue.consume(self.callback)
#
#
#     async def callback(self, message: aio_pika.IncomingMessage):
#         async with message.process():
#             data = json.loads(message.body)
#             print(f"CONSUMER{data}")
#             await update_currency_course(self.request, data)
#
#     async def start_consuming(self):
#         await self.connect()