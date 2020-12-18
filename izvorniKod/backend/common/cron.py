from datetime import datetime, timedelta

from common.models import User


def my_cron_job():
    ids = []
    for pending_user in User.objects.filter(is_active=False, date_joined__lte=datetime.now() - timedelta(days=30)):
        ids.append(pending_user.id)

    for user_id in ids:
        User.objects.filter(id=user_id).delete()


