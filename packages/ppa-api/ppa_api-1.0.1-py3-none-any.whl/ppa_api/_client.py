import logging
import functools
import json

from uuid import UUID
from typing import Optional, Dict, Any, List, Union, Callable

import requests

from requests.compat import urljoin  # type: ignore
from requests.utils import prepend_scheme_if_needed

from . import exceptions


logger = logging.getLogger(__name__)

user_query_params = "id,username,name,email,authenticated_at,active,deleted_at"

OptionalDict = Optional[Dict[str, Any]]
AnyJson = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]


def validate_uuid(uuid: str) -> str:
    try:
        UUID(uuid, version=4)
        return uuid
    except ValueError:
        raise exceptions.ParameterError("The format of the supplied UUID is invalid.")


def validate_payload(payload: AnyJson) -> AnyJson:
    try:
        json.dumps(payload)
    except TypeError:
        raise exceptions.ParameterError("The supplied payload cannot be converted to JSON.")
    return payload


def api_call(func) -> Callable:
    @functools.wraps(func)
    def _execute(*, address: str, api: str, endpoint: str, **kwargs: Any) -> AnyJson:
        response = func(address=address, api=api, endpoint=endpoint, **kwargs)
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            if response.status_code == 204:
                # The request was processed but no data was returned.
                return None
            if response.status_code == 403:
                raise exceptions.AuthenticationFailed(
                    "Forbidden (403). Failed to authenticate to PPA using the supplied API key."
                )
            elif response.status_code == 404:
                raise exceptions.NotFound(
                    f"Not Found (404). The {endpoint} endpoint does not exist."
                )
            raise exceptions.InvalidResponse(
                f"Unhandled Non-JSON Response ({response.status_code}). Response body: {response.text}."
            )

        if response.status_code == 200:
            return response_json

        try:
            raise exceptions.EXCEPTION_MAP[response.status_code](response_json, endpoint)
        except KeyError:
            raise exceptions.UnhandledRequestError(
                f"Unhandled ({response.status_code}). Response body: {response_json}."
            )

    return _execute


@api_call
def _get_request(
    *,
    address: str,
    api: Optional[str],
    endpoint: Optional[str] = None,
    api_key: str,
    verify_cert: bool,
    params: OptionalDict = None,
):
    return requests.get(
        urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        ),
        params=params,
        headers={"Accept": "application/json", "Authorization": f"Bearer {api_key}"},
        verify=verify_cert,
    )


@api_call
def _post_request(
    *,
    address: str,
    api: str,
    endpoint: str,
    api_key: str,
    verify_cert: bool,
    data: OptionalDict = None,
):
    return requests.post(
        urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        ),
        headers={"Accept": "application/json", "Authorization": f"Bearer {api_key}"},
        json=data,
        verify=verify_cert,
    )


class API:
    base = functools.partial(_get_request, api=None)
    tasks = functools.partial(_get_request, api="rest", endpoint="tasks")
    users = functools.partial(_get_request, api="rest", endpoint="users")
    images = functools.partial(_get_request, api="rest", endpoint="images")
    revisions = functools.partial(_get_request, api="rest", endpoint="revisions")
    rpc = functools.partial(_post_request, api="rest/rpc")
