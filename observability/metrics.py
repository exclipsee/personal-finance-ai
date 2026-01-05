import os
from prometheus_client import start_http_server, Counter, Gauge
import threading
import logging

METRICS_PORT = int(os.getenv('METRICS_PORT', '8000'))

# Define metrics
FILES_UPLOADED = Counter('pfai_files_uploaded_total', 'Total CSV files uploaded')
TRANSACTIONS_ADDED = Counter('pfai_transactions_added_total', 'Total transactions added')
APP_STARTS = Counter('pfai_app_starts_total', 'Number of app starts')
LAST_SYNC = Gauge('pfai_last_sync_timestamp', 'Last sync unix timestamp')


def start_metrics_server(port: int = METRICS_PORT):
    logger = logging.getLogger('observability.metrics')
    def _start():
        logger.info(f"Starting Prometheus metrics server on port {port}")
        try:
            start_http_server(port)
        except Exception:
            logger.exception('metrics start failed')

    thread = threading.Thread(target=_start, daemon=True)
    thread.start()


def record_file_upload(count: int = 0):
    FILES_UPLOADED.inc()
    if count:
        TRANSACTIONS_ADDED.inc(count)


def record_manual_add(count: int = 1):
    _c = count
    TRANSACTIONS_ADDED.inc(_c)


def record_app_start():
    APP_STARTS.inc()
