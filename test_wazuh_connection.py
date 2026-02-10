import os
import sys
import django
from opensearchpy import OpenSearch

# Setup Django environment
sys.path.append('/home/kali/Django/siem_project')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siem_project.settings")
django.setup()

from django.conf import settings

def test_wazuh_connection():
    print(f"Connecting to Wazuh Indexer at {settings.WAZUH_INDEXER_HOSTS}...")
    try:
        client = OpenSearch(
            hosts=settings.WAZUH_INDEXER_HOSTS,
            http_auth=settings.WAZUH_INDEXER_AUTH,
            use_ssl=settings.WAZUH_INDEXER_USE_SSL,
            verify_certs=settings.WAZUH_INDEXER_VERIFY_CERTS,
            ssl_show_warn=False
        )
        info = client.info()
        print("Successfully connected to Wazuh Indexer!")
        print(info)
        return True
    except Exception as e:
        print(f"Failed to connect to Wazuh Indexer: {e}")
        return False

if __name__ == "__main__":
    test_wazuh_connection()
