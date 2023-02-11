import logging
import time
from tests.functional.settings import test_settings
from elasticsearch import Elasticsearch


if __name__ == '__main__':
    host = test_settings.ELASTIC_HOST
    port = test_settings.ELASTIC_PORT
    protocol = test_settings.ELASTIC_PROTOCOL
    while True:
        es_client = Elasticsearch(
            hosts=host + "://" + host + ":" + str(port),
            validate_cert=False, use_ssl=False
        )
        if es_client.ping():
            logging.info("Successfully connected to elasticsearch")
            break
        time.sleep(1)
