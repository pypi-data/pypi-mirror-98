class ParameterError(Exception):
    pass


class RequestError(TypeError):
    pass


class ServerError(Exception):
    pass


class InvalidResponse(Exception):
    pass


class PermissionDenied(Exception):
    pass


class NoTaskFound(Exception):
    pass


class NoImageFound(Exception):
    pass


class ImageNotDeployed(Exception):
    pass


class WaitTimeout(Exception):
    pass


class TaskStillRunning(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


class CreditsRequired(Exception):
    pass


class UnhandledRequestError(Exception):
    pass


class NotFound(Exception):
    pass


class NoData(Exception):
    pass


class VersionError(Exception):
    pass


def _format_exception_string(json):
    return list(
        map(lambda key: json.get(key, f"no {key} provided"), ["message", "details", "hint"])
    )


EXCEPTION_MAP = {
    400: lambda json, _: RequestError(
        "Request Error (400). Message: {}. Details: {}. Hint: {}.".format(
            *_format_exception_string(json)
        )
    ),
    402: lambda _, __: CreditsRequired(
        "Credits Required (402). Cannot start the task as there are 0 credits available."
    ),
    403: lambda _, endpoint: PermissionDenied(
        f"Forbidden (403). The user associated with the API key does not have the required {endpoint} permissions."
    ),
    404: lambda _, __: NotFound(
        "Not Found (404). Either the endpoint or supplied record does not exist."
    ),
    500: lambda json, _: ServerError(
        "Internal Server Error (500). Message: {}. Details: {}. Hint: {}.".format(
            *_format_exception_string(json)
        )
    ),
}
