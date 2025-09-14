This is FastAPi that takes an input requests from front-end and queues the long running tasks in Celery workers.

One of the processes sends the message through Redis broker to Celery worker with Redis backend.
The other process sends the message through RabbitMQ broker to Celery worker with Postgresql backend.