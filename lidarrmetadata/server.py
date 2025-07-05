
import os
import logging
import time
import multiprocessing
import gunicorn.app.base

import lidarrmetadata
from lidarrmetadata.app import app
from lidarrmetadata.config import get_config
from lidarrmetadata.otel.config import init_otel_config
from lidarrmetadata.otel.telemetry import init_otel_app_tracing, init_otel_instrumentation

from pprint import pformat, pprint
logger = logging.getLogger(__name__)


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    """
    Entry point for script
    """
    global app
    config = get_config()
    log_level_map = {
        10: 'INFO',
        20: 'DEBUG'
    }

    log_level = logging.INFO
    if bool(config.DEBUG) is True:
        log_level = logging.DEBUG
    
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                        handlers=[logging.StreamHandler()])
    logger.info(f"logging started:: log_level={log_level_map[log_level]}")
    init_otel_config()
    app = init_otel_app_tracing(app)
    init_otel_instrumentation()
    time.sleep(3)
    

    options = {
        'bind': f'0.0.0.0:{config.HTTP_PORT}',
        'log_level': 'debug',
        'workers': 1,
        'proxy_headers': True,
        'forwarded_allow_ips': '*',
        'worker_class': 'uvicorn.workers.UvicornWorker'
    }

    StandaloneApplication(app, options).run()


if __name__ == '__main__':
    main()
