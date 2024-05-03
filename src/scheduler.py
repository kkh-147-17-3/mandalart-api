from apscheduler.schedulers.background import BackgroundScheduler
from logging import getLogger

logger = getLogger('main')

scheduler = BackgroundScheduler()


# @scheduler.scheduled_job('interval', seconds=3)
# def hello_world():
#     print("Hello")
#     logger.info({
#         "url": "www.naver.com",
#         "method": "POST",
#         "request_body": {
#             "text": "hello world"
#         },
#         "response_body": ["hello~"]
#     })
#     logger.debug("DEBUG Test")
#     logger.warning("Warning Test")
