import logging
from opensearchpy import OpenSearch
from django.conf import settings
from datetime import datetime, timezone

# Initialize Wazuh (OpenSearch) client
wazuh_client = OpenSearch(
    hosts=settings.WAZUH_INDEXER_HOSTS,
    http_auth=settings.WAZUH_INDEXER_AUTH,
    use_ssl=settings.WAZUH_INDEXER_USE_SSL,
    verify_certs=settings.WAZUH_INDEXER_VERIFY_CERTS,
    ssl_show_warn=False
)

# Initialize Elasticsearch (legacy) client
try:
    from elasticsearch import Elasticsearch
    es_client = Elasticsearch(
        hosts=settings.ELASTICSEARCH_HOSTS,
        api_key=settings.ELASTICSEARCH_API_KEY
    )
except ImportError:
    es_client = None
    print("Warning: elasticsearch library not found. Elasticsearch logging disabled.")

class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        if not es_client:
            return
        try:
            log_entry = {
                'event_type': getattr(record, 'event_type', record.getMessage()),
                'username': getattr(record, 'username', 'unknown'),
                'ip_address': getattr(record, 'ip_address', 'unknown'),
                'severity': record.levelname,
                'timestamp': datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                'message': record.getMessage()
            }
            es_client.index(index=settings.ELASTICSEARCH_INDEX, document=log_entry)
        except Exception as e:
            print(f"Elasticsearch logging failed: {e}")

class WazuhHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = {
                'event_type': getattr(record, 'event_type', record.getMessage()),
                'username': getattr(record, 'username', 'unknown'),
                'ip_address': getattr(record, 'ip_address', 'unknown'),
                'severity': record.levelname,
                'timestamp': datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                'message': record.getMessage()
            }
            # Index into 'django-audit-logs' (same index name, but in Wazuh)
            wazuh_client.index(index=settings.ELASTICSEARCH_INDEX, body=log_entry)
        except Exception as e:
            # Fallback: Log to console if Wazuh logging fails
            print(f"Wazuh logging failed: {e}")

# Configure audit logger
audit_logger = logging.getLogger('audit')
audit_logger.addHandler(WazuhHandler())
audit_logger.addHandler(ElasticsearchHandler())
audit_logger.setLevel(logging.INFO)
