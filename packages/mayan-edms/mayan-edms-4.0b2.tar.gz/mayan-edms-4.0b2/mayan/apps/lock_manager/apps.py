import logging
import sys

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .backends.base import LockingBackend
from .literals import PURGE_LOCKS_COMMAND, TEST_LOCK_NAME
from .settings import setting_backend

logger = logging.getLogger(name=__name__)


class LockManagerApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.lock_manager'
    verbose_name = _('Lock manager')

    def ready(self):
        super().ready()

        if PURGE_LOCKS_COMMAND not in sys.argv:
            # Don't test for locks during the `purgelocks` command as there
            # may be some stuck locks which will block the command.
            lock_instance = LockingBackend.get_instance()
            try:
                lock = lock_instance.acquire_lock(
                    name=TEST_LOCK_NAME, timeout=1
                )
                lock.release()
            except Exception as exception:
                logger.critical(
                    'Error initializing the locking backend: %s; %s',
                    setting_backend.value, exception
                )
                raise
