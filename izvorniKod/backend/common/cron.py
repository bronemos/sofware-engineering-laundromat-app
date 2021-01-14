from datetime import datetime, timedelta

from common.models import User, Laundry, Appointment


def my_cron_job():
    ids = []
    for pending_user in User.objects.filter(is_active=False, date_joined__lte=datetime.now() - timedelta(days=30)):
        ids.append(pending_user.id)

    for user_id in ids:
        User.objects.filter(id=user_id).delete()

    laundry = Laundry.objects.filter(date_changed__lte=datetime.now()).first()

    for appointment in Appointment.objects.filter(start__gte=datetime.now(), start__lt=datetime.now() + timedelta(days=1)):
        if appointment.start.time() <= laundry.middle:
            appointment.employee = laundry.first_shift_worker
        else:
            appointment.employee = laundry.second_shift_worker
        appointment.save()

