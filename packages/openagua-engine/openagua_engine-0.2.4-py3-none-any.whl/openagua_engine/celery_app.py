from os import environ
from celery import Celery
from openagua_engine.utils import get_broker_url
from openagua_engine import constants


def create_app(model_key=None, run_key=None):
    model_key = model_key or environ.get(constants.MODEL_KEY)
    if not model_key:
        raise Exception("No model key provided. Please provide a model key as an argument\
         or as the environment variable {}".format(constants.MODEL_KEY))
    run_key = run_key or environ.get(constants.RUN_KEY)
    broker_url = get_broker_url(model_key)

    # redis_host = environ.get('REDIS_HOST', 'localhost')

    # test redis
    # redis.set('test', 1)

    # environ['FORKED_BY_MULTIPROCESSING'] = '1'

    app = Celery(
        'openagua',
        broker=broker_url,
        include=['tasks'],
    )

    task_queue_name = 'model-{}'.format(model_key)
    if run_key:
        task_queue_name += '-{}'.format(run_key)

    app.conf.update(
        task_default_queue=task_queue_name,
        task_default_exchange='tasks',
        broker_heartbeat=10,
        accept_content=['json', 'pickle'],
        result_expires=3600
    )

    return app
