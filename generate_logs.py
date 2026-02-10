import os
import sys
import django
import logging

# Setup Django environment
sys.path.append('/home/kali/Django/siem_project')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siem_project.settings")
django.setup()

from audit.logger import audit_logger

def generate_test_logs():
    print("Generating test login events...")
    
    # Simulate a successful login
    audit_logger.info("Test login successful", extra={
        'event_type': 'LOGIN_SUCCESS',
        'username': 'test_user',
        'ip_address': '127.0.0.1'
    })
    print("Sent: LOGIN_SUCCESS")

    # Simulate a failed login
    audit_logger.warning("Test failed login attempt", extra={
        'event_type': 'LOGIN_FAILED',
        'username': 'bad_actor',
        'ip_address': '192.168.1.50'
    })
    print("Sent: LOGIN_FAILED")
    
    print("Done! Check Wazuh Dashboard.")

if __name__ == "__main__":
    generate_test_logs()
