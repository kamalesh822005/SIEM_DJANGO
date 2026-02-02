from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        event_type="LOGIN_SUCCESS",
        username=user.username,
        ip_address=request.META.get('REMOTE_ADDR'),
        severity="LOW"
    )
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        event_type="LOGOUT",
        username=user.username,
        ip_address=request.META.get('REMOTE_ADDR'),
        severity="LOW"
    )
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(
        event_type="LOGIN_FAILED",
        username=credentials.get('username', 'UNKNOWN'),
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        severity="HIGH"
    )
