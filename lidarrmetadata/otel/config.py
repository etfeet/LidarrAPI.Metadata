import os
import socket
import logging
from opentelemetry.sdk.resources import Resource
from lidarrmetadata.util import string_to_bool


logger = logging.getLogger(__name__)

class OTLP:
    RESOURCE = None
    class CONFIG:
        INSTANCE_NAME = 'unset'
        SERVICE_NAME = 'unset'
        CONSOLE_EXPORTER_ENABLED = False
        REMOTE_EXPORTER_ENABLED =  False
        REMOTE_EXPORTER_EDNPOINT = 'localhost:4317'
        REMOTE_EXPORTER_INSECURE =  False

def init_otel_config():
    OTLP.CONFIG.INSTANCE_NAME = os.getenv('OTLP_INSTANCE_NAME', socket.gethostname())
    OTLP.CONFIG.SERVICE_NAME = os.getenv('OTLP_SERVICE_NAME', 'lidarr-metadata-api')
    OTLP.CONFIG.CONSOLE_EXPORTER_ENABLED = string_to_bool(str(os.getenv('OTLP_CONSOLE_EXPORTER_ENABLED', False)))
    OTLP.CONFIG.REMOTE_EXPORTER_ENABLED =  string_to_bool(str(os.getenv('OTLP_REMOTE_EXPORTER_ENABLED', False)))
    OTLP.CONFIG.REMOTE_EXPORTER_EDNPOINT = os.getenv('OTLP_REMOTE_EXPORTER_EDNPOINT', 'localhost:4317')
    OTLP.CONFIG.REMOTE_EXPORTER_INSECURE =  string_to_bool(str(os.getenv('OTLP_REMOTE_EXPORTER_INSECURE', False)))
    
    OTLP.RESOURCE = Resource.create({
        "instance.name": OTLP.CONFIG.INSTANCE_NAME,
        "service.name": OTLP.CONFIG.SERVICE_NAME,
    })
    
    logger.info("initializing opentelemetry config: \n"
            f"                OTLP_INSTANCE_NAME: {OTLP.CONFIG.INSTANCE_NAME}\n"
            f"                 OTLP_SERVICE_NAME: {OTLP.CONFIG.SERVICE_NAME}\n"
            f"     OTLP_CONSOLE_EXPORTER_ENABLED: {OTLP.CONFIG.CONSOLE_EXPORTER_ENABLED}\n"
            f"      OTLP_REMOTE_EXPORTER_ENABLED: {OTLP.CONFIG.REMOTE_EXPORTER_ENABLED}\n"
            f"     OTLP_REMOTE_EXPORTER_EDNPOINT: {OTLP.CONFIG.REMOTE_EXPORTER_EDNPOINT}\n"
            f"     OTLP_REMOTE_EXPORTER_INSECURE: {OTLP.CONFIG.REMOTE_EXPORTER_INSECURE}")

