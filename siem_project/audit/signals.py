print(">>> AUDIT SIGNALS FILE LOADED <<<")

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditLog
from .logger import auth_logger  


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")

    # 1️⃣ DB audit (unchanged)
    AuditLog.objects.create(
        event_type="LOGIN_SUCCESS",
        username=user.username,
        ip_address=ip,
        severity="LOW"
    )

    # 2️⃣ FILE log (NEW)
    auth_logger.info(f"LOGIN_SUCCESS user={user.username} ip={ip}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")

    AuditLog.objects.create(
        event_type="LOGOUT",
        username=user.username,
        ip_address=ip,
        severity="LOW"
    )

    auth_logger.info(f"LOGOUT user={user.username} ip={ip}")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username", "UNKNOWN")
    ip = request.META.get("REMOTE_ADDR") if request else "unknown"

    AuditLog.objects.create(
        event_type="LOGIN_FAILED",
        username=username,
        ip_address=ip,
        severity="HIGH"
    )

    auth_logger.warning(f"LOGIN_FAILED user={username} ip={ip}")
