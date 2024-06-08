from celery import Celery

from config import redis_host, redis_port

celery_app = Celery('tasks', broker=f'redis://{redis_host}:{redis_port}')
