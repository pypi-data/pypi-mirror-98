import logging

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.db import connections


class AbstractScrubbingService:
    DEFAULT_USER_PASSWORD = 'Admin0404!'

    # Overwritable values
    keep_scrubber_data = False
    keep_django_admin_log = False
    pre_scrub_functions = []
    post_scrub_functions = []

    def __init__(self):
        self._logger = logging.getLogger('django_scrubber')

    def _get_hashed_default_password(self):
        return make_password(self.DEFAULT_USER_PASSWORD)

    def _validation(self):
        if not settings.DEBUG:
            self._logger.warning('Attention! Needs to be run in DEBUG mode!')
            return False

        if 'django_scrubber' not in settings.INSTALLED_APPS:
            self._logger.warning('Attention! django-scrubber needs to be installed!')
            return False

        if 'django_scrubber' not in list(settings.LOGGING['loggers'].keys()):
            self._logger.warning('Attention! Logging for django-scrubber is not activated!')

        return True

    def process(self):
        self._logger.info('Start scrubbing process...')

        self._logger.info('Validating setup...')
        if not self._validation():
            self._logger.warning('Aborting process!')
            return False

        # Custom pre-scrubbing
        for name in self.pre_scrub_functions:
            self._logger.info(f'Pre-Scrubbing: Calling "{name}()"...')
            method = getattr(self, name)
            method()

        self._logger.info('Scrubbing data with "scrub_data"...')
        call_command('scrub_data')

        # Custom post-scrubbing
        for name in self.post_scrub_functions:
            self._logger.info(f'Post-Scrubbing: Calling "{name}()"...')
            method = getattr(self, name)
            method()

        # Empty django admin log (may contain user-related data)
        if not self.keep_django_admin_log:
            LogEntry.objects.all().delete()

        # Reset scrubber data to avoid huge db dumps
        if not self.keep_scrubber_data:
            self._logger.info('Scrubbing data from "scrub_data" ...')
            # We truncate and don't scrub because the table is huge and will stay the same size if we just
            # delete the records.
            cursor = connections['default'].cursor()
            cursor.execute('TRUNCATE TABLE django_scrubber_fakedata;')

        self._logger.info('Scrubbing finished!')

        return True
