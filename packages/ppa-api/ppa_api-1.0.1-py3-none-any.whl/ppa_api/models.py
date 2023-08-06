from collections import namedtuple

Image = namedtuple(
    "Image",
    [
        "author",
        "description",
        "deployed",
        "groups",
        "id",
        "name",
        "owner",
        "tags",
        "updated_at",
        "uuid",
    ],
)

Task = namedtuple(
    "Task",
    [
        "author",
        "cancelled_at",
        "cancelled_by",
        "duration",
        "exit_code",
        "exit_message",
        "id",
        "image",
        "image_id",
        "image_uuid",
        "is_owner",
        "is_running",
        "started_at",
        "state",
        "stopped_at",
        "timed_out",
        "timeout",
        "username",
        "uuid",
    ],
)

User = namedtuple(
    "User", ["active", "authenticated_at", "deleted_at", "email", "id", "name", "username"]
)

TaskResult = namedtuple("TaskResult", ["exit_code", "exit_message", "result_json", "state"])
