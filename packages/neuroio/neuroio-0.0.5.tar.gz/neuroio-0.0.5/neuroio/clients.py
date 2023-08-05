import enum
from typing import Any, Dict, Optional, Type, Union

import httpx

from neuroio import constants
from neuroio.api.base import APIBase
from neuroio.auth import AuthorizationTokenAuth
from neuroio.utils import cached_property, dynamic_import, get_package_version


class Service(str, enum.Enum):
    API = "api"
    IAM = "iam"


class Client:
    def __init__(
        self,
        api_token: Optional[str] = None,
        api_version: int = 1,
        timeout: float = constants.HTTP_CLIENT_TIMEOUT,
    ):
        """
        Creates and manages singleton of HTTP client, that is used to make
        request to API.
        """
        self.api_token = api_token
        self.api_version = api_version

        self.api_settings = self.client_settings(
            timeout=timeout, base_url=constants.API_BASE_URL
        )
        self.iam_settings = self.client_settings(
            timeout=timeout, base_url=constants.IAM_BASE_URL
        )

    @property
    def common_headers(self) -> dict:
        return {"User-Agent": f"neuroio-python/{get_package_version()}"}

    def client_settings(self, base_url: str, timeout: float) -> Dict[Any, Any]:
        settings = {
            "base_url": base_url,
            "timeout": timeout,
            "headers": self.common_headers,
        }
        if self.api_token:
            settings["auth"] = AuthorizationTokenAuth(api_token=self.api_token)

        return settings

    def get_api_class_instance(
        self, namespace: str, clsname: str, service: Service = Service.API
    ) -> APIBase:
        abs_path = f"neuroio.{service}.{namespace}.v{self.api_version}"
        cls = dynamic_import(abs_path=abs_path, attribute=clsname)
        if service == Service.API:
            return cls(settings=self.api_settings)
        return cls(settings=self.iam_settings)

    @cached_property
    def auth(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="auth", clsname="Auth", service=Service.IAM
        )

    @cached_property
    def sources(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="sources", clsname="Sources"
        )

    @cached_property
    def entries(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="entries", clsname="Entries"
        )

    @cached_property
    def utility(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="utility", clsname="Utility"
        )

    @cached_property
    def settings(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="settings", clsname="Settings"
        )

    @cached_property
    def groups(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="groups", clsname="Groups"
        )

    @cached_property
    def persons(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="persons", clsname="Persons"
        )

    @cached_property
    def notifications(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="notifications", clsname="Notifications"
        )

    @cached_property
    def spaces(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="spaces", clsname="Spaces", service=Service.IAM
        )

    @cached_property
    def whoami(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="whoami", clsname="Whoami", service=Service.IAM
        )

    @cached_property
    def tokens(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="tokens", clsname="Tokens", service=Service.IAM
        )


class AsyncClient(Client):
    @property
    def common_headers(self) -> dict:
        return {"User-Agent": f"neuroio-async-python/{get_package_version()}"}

    @cached_property
    def auth(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="auth", clsname="AuthAsync", service=Service.IAM
        )

    @cached_property
    def sources(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="sources", clsname="SourcesAsync"
        )

    @cached_property
    def entries(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="entries", clsname="EntriesAsync"
        )

    @cached_property
    def utility(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="utility", clsname="UtilityAsync"
        )

    @cached_property
    def settings(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="settings", clsname="SettingsAsync"
        )

    @cached_property
    def groups(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="groups", clsname="GroupsAsync"
        )

    @cached_property
    def persons(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="persons", clsname="PersonsAsync"
        )

    @cached_property
    def notifications(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="notifications", clsname="NotificationsAsync"
        )

    @cached_property
    def spaces(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="spaces", clsname="SpacesAsync", service=Service.IAM
        )

    @cached_property
    def whoami(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="whoami", clsname="WhoamiAsync", service=Service.IAM
        )

    @cached_property
    def tokens(self) -> APIBase:
        return self.get_api_class_instance(
            namespace="tokens", clsname="TokensAsync", service=Service.IAM
        )
