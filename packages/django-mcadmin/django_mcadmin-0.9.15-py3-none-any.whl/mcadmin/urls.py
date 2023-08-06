# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/urls.py


from typing import List, Union  # pylint: disable=W0611

from django.urls import re_path
from django.views.static import serve
from django.contrib.admin.views.decorators import staff_member_required
from django.urls.resolvers import URLPattern, URLResolver  # pylint: disable=W0611

from mcadmin.conf import settings
from mcadmin.views import ManagementCommandsAdminIndex


__all__ = ["urlpatterns"]  # type: List[str]


# mcadmin urls
urlpatterns = [
    re_path(r"^$", ManagementCommandsAdminIndex.as_view(), name="mcadmin-index"),
    re_path(
        r"^examples/(?P<path>.*)$",
        staff_member_required(serve),
        {"document_root": settings.MCADMIN_EXAMPLES_PATH, "show_indexes": False},
        name="mcadmin-example-file",
    ),
]  # type: List[Union[URLPattern, URLResolver]]
