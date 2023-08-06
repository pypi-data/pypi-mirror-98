from typing import Any

from us_libraries.client.base_client import BaseClient

service_name = "usf-auth-service"


class AuthClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(service_name)

    def login(self, username: str, password: str) -> Any:
        return self.post('login', username=username, password=password)

    def has_permission(self, login_token: str, permission_id: int) -> Any:
        return self.post('permission/has_permission', login_token=login_token, permission_id=permission_id)
