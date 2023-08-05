from typing import Any

from django.conf import settings

from revns import DEV, PROD, STG
from revns import BaseNotification as PureBaseNotification
from revns import EmailNotification as PureEmailNotification
from revns import MobileNotification as PureMobileNotification
from revns import SmsNotification as PureSmsNotification
from revns import TemplatedEmailNotification as PureTemplatedNotification


class BaseNotification(PureBaseNotification):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["client_secret"] = settings.CLIENT_SECRET
        kwargs["client_id"] = settings.CLIENT_ID
        stage = getattr(settings, "STAGE")
        if stage in ["prod", "PROD"]:
            kwargs["stage"] = PROD
        elif stage in ["stg", "STG"]:
            kwargs["stage"] = STG
        else:
            kwargs["stage"] = DEV
        super().__init__(*args, **kwargs)


class MobileNotification(BaseNotification, PureMobileNotification):
    pass


class EmailNotification(BaseNotification, PureEmailNotification):
    pass


class TemplatedNotification(BaseNotification, PureTemplatedNotification):
    pass


class SmsNotification(BaseNotification, PureSmsNotification):
    pass
