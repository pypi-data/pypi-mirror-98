from typing import Any


class NtfnException(Exception):
    def __init__(self, code: str, detail: Any) -> None:
        self.code = code
        self.detail = detail
        msg = f"{code}: {detail}"
        super().__init__(self, msg)


class PublishError(NtfnException):
    pass


class UserAddError(NtfnException):
    pass
