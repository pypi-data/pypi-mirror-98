import time

from typing import List, Optional, Union, Callable

import timeout_decorator

from . import create, exceptions
from ._client import (
    API,
    user_query_params,
    validate_uuid,
    validate_payload,
    OptionalDict,
)
from .models import Image, Task, User, TaskResult


class PPAClient:
    def __init__(self, address: str, *, api_key: str, verify_cert: Optional[bool] = True) -> None:
        self.address = address
        self.api_key = api_key
        self.verify_cert = verify_cert

        # Doing this on instantiation also checks the credentials for us.
        try:
            self.version = self._request(API.base, endpoint="version")["appliance"]
        except exceptions.NotFound:
            # Any PPA older than 2.7.1 won't have the version endpoint.
            raise exceptions.VersionError(
                "This package does not support PPA appliances older than v2.7.1."
            )

    def _request(self, api_method: Callable, **kwargs):
        return api_method(
            address=self.address,
            api_key=self.api_key,
            verify_cert=self.verify_cert,
            **kwargs,
        )

    @create.images
    def images(self, latest: Optional[bool] = False) -> List[Image]:
        return self._request(API.images if latest else API.revisions)

    @create.images
    def image_by_name(self, name: str) -> Optional[Image]:
        try:
            return self._request(API.images, params={"name": f"eq.{name}"})[0]
        except IndexError:
            return None

    @create.images
    def images_by_name(self, name: str) -> List[Image]:
        return self._request(API.revisions, params={"name": f"eq.{name}"})

    @create.images
    def image_by_id(self, image_id: int) -> Optional[Image]:
        try:
            return self._request(API.revisions, params={"id": f"eq.{image_id}"})[0]
        except IndexError:
            return None

    @create.tasks
    def tasks(self) -> List[Task]:
        return self._request(API.tasks)

    @create.tasks
    def task_by_uuid(self, uuid: str) -> Optional[Task]:
        try:
            return self._request(API.tasks, params={"uuid": f"eq.{validate_uuid(uuid)}"})[0]
        except IndexError:
            return None

    @create.tasks
    def tasks_started_by_me(self) -> List[Task]:
        return self._request(API.tasks, params={"is_owner": "eq.true"})

    @create.users
    def users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "is.null"},
        )

    @create.users
    def licensed_users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "is.null", "active": "eq.true"},
        )

    @create.users
    def deleted_users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "not.is.null"},
        )

    @create.users
    def user_by_id(self, user_id: Union[str, int]) -> Optional[User]:
        try:
            return self._request(
                API.users,
                params={"id": f"eq.{user_id}", "select": user_query_params},
            )[0]
        except IndexError:
            return None

    @create.users
    def user_by_username(self, name: str) -> Optional[User]:
        try:
            return self._request(
                API.users,
                params={"username": f"ilike.*\\{name}", "select": user_query_params},
            )[0]
        except IndexError:
            return None

    def task_running(self, uuid: str) -> bool:
        uuid = validate_uuid(uuid)
        if task := self.task_by_uuid(uuid):
            return task.is_running
        raise exceptions.NoTaskFound(f"No task was found with UUID '{uuid}'.")

    def wait_for_task(
        self,
        uuid: str,
        timeout: Optional[int] = 600,
        interval: Optional[Union[int, float]] = 5,
    ) -> Task:
        @timeout_decorator.timeout(
            timeout,
            timeout_exception=exceptions.WaitTimeout,
            exception_message=f"Task has not finished after {timeout} seconds.",
        )
        def _execute():
            while self.task_running(uuid):
                time.sleep(interval)
            return self.task_by_uuid(uuid)

        return _execute()

    def start_task_async(self, name: str, *, payload: OptionalDict = None) -> Task:
        if not self.image_by_name(name):
            raise exceptions.NoImageFound(
                f"There are no images delegated to your identity with the name '{name}'."
            )
        try:
            return self.task_by_uuid(
                self._request(
                    API.rpc,
                    endpoint="start_task",
                    data={"image_name": name, "payload": payload},
                )
            )
        except exceptions.RequestError as e:
            if "must be deployed" in str(e):
                raise exceptions.ImageNotDeployed(
                    f"The task cannot be started as image '{name}' is not deployed."
                )
            raise e

    def start_task(
        self,
        name: str,
        *,
        payload: OptionalDict = None,
        timeout: Optional[int] = 600,
        interval: Optional[int] = 5,
    ) -> Task:
        return self.wait_for_task(
            self.start_task_async(name, payload=validate_payload(payload)).uuid,
            timeout=timeout,
            interval=interval,
        )

    def cancel_task(
        self,
        uuid: str,
    ) -> None:
        uuid = validate_uuid(uuid)
        try:
            self._request(API.rpc, endpoint="cancel_task", data={"uuid": validate_uuid(uuid)})
        except exceptions.NotFound:
            raise exceptions.NoTaskFound(
                f"Task with UUID '{uuid}' is either not running or does not exist."
            )

    def task_succeeded(self, uuid: str) -> bool:
        exit_code = self.task_by_uuid(uuid).exit_code
        if exit_code is None:
            raise exceptions.TaskStillRunning(f"Task with UUID '{uuid}' is still running.")
        return exit_code == 0

    @create.task_result
    def get_task_result(self, uuid: str) -> TaskResult:
        if task_result := self._request(
            API.rpc, endpoint="task_result", data={"uuid": validate_uuid(uuid)}
        ):
            return task_result
        raise exceptions.NoData(f"No result data was saved by task with UUID '{uuid}'.")
