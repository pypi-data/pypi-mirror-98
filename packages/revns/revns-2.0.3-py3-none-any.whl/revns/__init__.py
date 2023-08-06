from typing import Any, Dict, Optional

import requests

from revns import exceptions

__version__ = "2.0.0"

DEV = "DEV"
STG = "STG"
PROD = "PROD"
HOST = "https://notification.revtel-api.com/v4"
STG_HOST = "https://notification-stg.revtel-api.com/v4"
DEV_HOST = "https://notification-dev.revtel-api.com/v4"


class BaseNotification:
    target_type = "mobile"
    publish_path = ""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        instance: Any = None,
        stage: str = STG,
        **kwargs: Any,
    ) -> None:
        stage = stage.upper()
        if stage not in [DEV, PROD, STG]:
            raise ValueError("stage should be in [PROD, STG, DEV]")
        self.stage = stage
        self.instance = instance
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def host(self) -> str:
        if self.stage == PROD:
            return HOST
        elif self.stage == STG:
            return STG_HOST
        else:
            return DEV_HOST

    @property
    def auth_param(self) -> str:
        return f"client_id={self.client_id}&client_secret={self.client_secret}"

    def build_request_payload(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError

    def get_url(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    def _post(self, url: str, data: Dict[str, Any]) -> requests.Response:
        resp = requests.post(url, json=data)
        return resp

    def build_title(self) -> str:
        raise NotImplementedError

    def build_body(self) -> str:
        raise NotImplementedError

    def build_target(self) -> str:
        raise NotImplementedError

    def build_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def publish(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        raise_exception = kwargs.pop("raise_exception", False)
        url = self.get_url(*args, **kwargs)
        payload = self.build_request_payload(*args, **kwargs)
        try:
            resp = self._post(url, data=payload)
            resp.raise_for_status()
            return resp.json()  # type: ignore
        except requests.exceptions.HTTPError:
            resp_json = resp.json()
            if raise_exception:
                raise exceptions.PublishError(
                    code=resp_json["error"], detail=resp_json["detail"]
                )
            return resp_json  # type: ignore


class MobileNotification(BaseNotification):
    target_type = "mobile"
    public_topic = "public-topic"
    dest = "user"

    def get_url(self, target: Optional[str] = None, **kwargs: Any) -> str:  # type: ignore
        if target is None:
            target = self.build_target()
        return (
            f"{self.host}/notification/publish/{self.dest}/{target}?{self.auth_param}"
        )

    def build_subtitle(self) -> str:
        raise NotImplementedError("build_subtitle() should be implement")

    def build_request_payload(  # type: ignore[override]
        self,
        target: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        subtitle: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not title:
            title = self.build_title()
        if not body:
            body = self.build_body()
        if not data:
            data = self.build_data()

        payload = {"subject": title, "title": title, "body": body, "data": data}

        if not subtitle:
            try:
                payload["subtitle"] = self.build_subtitle()
            except:
                pass

        return payload


class EmailNotification(BaseNotification):
    target_type = "email"
    sender_name = "default"

    def get_url(self, **kwargs: Any) -> str:  # type: ignore[override]
        return f"{self.host}/email/extra/send/{self.sender_name}?{self.auth_param}"

    def build_request_payload(  # type: ignore[override]
        self,
        target: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not target:
            target = self.build_target()
        if not title:
            title = self.build_title()
        if not body:
            body = self.build_body()

        payload = {"html": body, "subject": title, "to": target}
        return payload


class TemplatedEmailNotification(EmailNotification):
    def get_url(self, **kwargs: Any) -> str:  # type: ignore[override]
        return f"{self.host}/email/send/{self.sender_name}?{self.auth_param}"

    def build_request_payload(  # type: ignore[override]
        self,
        target: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not target:
            target = self.build_target()
        if not data:
            data = self.build_data()

        payload = {"to": target, "data": data}
        return payload


class SmsNotification(BaseNotification):
    def get_url(self, **kwargs: Any) -> str:  # type: ignore[override]
        return f"{self.host}/sms/send?{self.auth_param}"

    def format_target(self, raw: str) -> str:
        pn = ""

        if raw:
            if raw[0] == "0":
                pn = "+886 " + raw[1:]
            elif raw[0] == "+":
                pn = raw
            else:
                pn = "+" + raw

        return pn

    def build_request_payload(  # type: ignore[override]
        self,
        target: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not target:
            target = self.format_target(self.build_target())
        else:
            target = self.format_target(target)
        if not title:
            title = self.build_title()
        if not body:
            body = self.build_body()

        payload = {"message": body, "subject": title, "phone": target}
        return payload
