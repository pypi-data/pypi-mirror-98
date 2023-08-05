from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@localhost//")

celery_app.conf.task_routes = {"cntr.worker.test_celery": "main-queue"}
