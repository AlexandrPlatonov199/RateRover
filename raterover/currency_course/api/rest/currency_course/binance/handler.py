# import asyncio
# import json
#
# import websockets
# from loguru import logger
#
# from raterover.currency_course.broker.service import CourseBrokerService
# from raterover.currency_course.database.service import CurrencyCourseDatabaseService
#
#
# async def get_price_feed(symbol, request):
#     broker_service: CourseBrokerService = request.app.service.broker
#     uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"
#
#     async with websockets.connect(uri) as websocket:
#         response = await websocket.recv()
#         data = json.loads(response)
#         logger.debug(f"Получены данные (Binance): {data}")
#         logger.info(f"Цена для {symbol} (Binance): {data['p']}")
#
#         result = {
#             "exchanger": "binance",
#             "direction": data["s"],
#             "value": float(data["p"])
#         }
#
#         await broker_service._publish_events(data=json.dumps(result), message_id=1)
#
#
#
#
#
#         await asyncio.sleep(5)



# async def update_currency_course(request):
#     try:
#         broker_service: CourseBrokerService = request.app.service.broker
#         database: CurrencyCourseDatabaseService = request.app.service.database
#
#         result = await broker_service.consume_from_queue()
#
#         async with database.transaction() as session:
#             await database.create_currency_course(
#                 session=session,
#                 exchanger=result.exchanger,
#                 direction=result.direction,
#                 value=result.value,
#             )
#
#     except Exception as e:
#         logger.error(f"Ошибка при получении данных для с Binance: {str(e)}")

# async def binance_price_feed(request, base_symbol):
#     symbol = base_symbol
#     uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"
#
#     async with websockets.connect(uri) as websocket:
#         try:
#             response = await websocket.recv()
#             data = json.loads(response)
#
#             logger.debug(f"Получены данные (Binance): {data}")
#
#             logger.info(f"Цена для {symbol} (Binance): {data['p']}")
#
#             database: CurrencyCourseDatabaseService = request.app.service.database
#
#             async with database.transaction() as session:
#                 await database.create_currency_course(
#                     session=session,
#                     exchanger="binance",
#                     direction=data["s"],
#                     value=float(data["p"]),
#                 )
#
#             await asyncio.sleep(5)
#         except Exception as e:
#             logger.error(f"Ошибка при получении данных для {symbol} с Binance: {str(e)}")

