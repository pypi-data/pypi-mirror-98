# -*- coding: utf-8 -*-

# django-mcadmin
# djversion/conf.py


from typing import List  # pylint: disable=W0611

from appconf import AppConf
from django.conf import settings


__all__ = ["settings"]  # type: List[str]


class DjangoDjversionAppConf(AppConf):
    """
    Django djversion settings.
    """

    EXAMPLES_PATH = getattr(
        settings, "MCADMIN_EXAMPLES_PATH", settings.STATIC_ROOT
    )  # type: str
    UPLOADS_PATH = getattr(
        settings, "MCADMIN_UPLOADS_PATH", settings.MEDIA_ROOT
    )  # type: str
    MODULE_NAME = getattr(settings, "MCADMIN_MODULE_NAME", "mcommands")  # type: str
    USE_PERMISSIONS = getattr(settings, "MCADMIN_USE_PERMISSIONS", False)  # type: bool

    class Meta:
        """
        Config settings.
        """

        prefix = "mcadmin"  # type: str
