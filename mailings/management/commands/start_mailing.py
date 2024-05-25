import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailings.models import Mailing, MailingLog
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        mailings = Mailing.objects.all()
        logs = MailingLog.objects.all()
        time = datetime.datetime.now().replace(tzinfo=None)

        for mailing in mailings:

            if self.get_info_for_mailing_start(mailing, logs, time):
                related_clients = mailing.clients.all()

                if len(related_clients) == 0:
                    log = MailingLog.objects.create(
                        status='failed',
                        mailing_list=mailing,
                        server_response='Отсутствуют клиенты для рассылки.',
                        user=mailing.user,
                    )
                    log.save()
                    break

                for client in related_clients:

                    try:
                        status = send_mail(
                            mailing.mail_subject,
                            mailing.mail_text,
                            settings.EMAIL_HOST_USER,

                            [client.email],
                            fail_silently=False
                        )
                        mailing.status = 'started'
                        mailing.save()
                    except ConnectionRefusedError as error:
                        log = MailingLog.objects.create(
                            timestamp=time,
                            status='failed',
                            mailing_list=mailing,
                            server_response=error,
                            user=mailing.user,
                        )
                        log.client.set([client])
                        log.save()
                        mailing.status = 'created'
                        mailing.save()
                    else:

                        if status:
                            log = MailingLog.objects.create(
                                timestamp=time,
                                status='success',
                                mailing_list=mailing,
                                user=mailing.user,
                            )
                            log.client.set([client])
                            log.save()
                            mailing.status = 'completed'
                            mailing.save()
                        else:
                            log = MailingLog.objects.create(
                                timestamp=time,
                                status='failed',
                                mailing_list=mailing,
                                user=mailing.user,
                            )
                            log.client.set([client])
                            log.save()
                            mailing.status = 'created'
                            mailing.save()

            else:
                continue

    @staticmethod
    def get_info_for_mailing_start(mailing, logs, time):
        mailing_latest_log = logs.filter(mailing_list=mailing).all().order_by('-timestamp').first()

        if mailing_latest_log is None:

            if not mailing.is_active:
                return False

            elif mailing.mailing_time.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=None
            ) <= time:
                return True

        elif not mailing.is_active:
            return False

        elif mailing_latest_log.status == 'failed':
            return True

        else:

            log_time = mailing_latest_log.timestamp.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=None
            )
            time_difference = (time - log_time).days

            if mailing.frequency == 'daily':

                if time_difference == 1:
                    return True

            elif mailing.frequency == 'weekly':

                if time_difference == 7:
                    return True

            else:

                if time_difference == 30:
                    return True
