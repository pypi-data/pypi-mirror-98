import functools

from typing import Callable, List, Optional, Union

from .models import Image, Task, User, TaskResult


def _creator(
    tuple_type: Union[Image, Task, User, TaskResult], results: Union[List[dict], dict]
) -> Optional[List]:

    if results is None:
        return None

    def _create_named_tuple(item):
        return tuple_type(**{field: item.get(field) for field in list(tuple_type._fields)})

    if isinstance(results, list):
        return [_create_named_tuple(d) for d in results]
    elif isinstance(results, dict):
        return _create_named_tuple(results)
    else:
        raise TypeError(
            f"Can only create API records from a list or dictionary, received {type(results)}."
        )


def _sort(items, key, reverse: Optional[bool] = False):
    return (
        sorted(items, key=lambda x: getattr(x, key), reverse=reverse)
        if isinstance(items, list)
        else items
    )


def images(func: Callable) -> Callable:
    @functools.wraps(func)
    def _image_creator(*args, **kwargs) -> Optional[List[Image]]:
        return _sort(_creator(Image, func(*args, **kwargs)), "name")

    return _image_creator


def tasks(func: Callable) -> Callable:
    @functools.wraps(func)
    def _task_creator(*args, **kwargs) -> Optional[List[Task]]:
        return _sort(_creator(Task, func(*args, **kwargs)), "started_at", reverse=True)

    return _task_creator


def users(func: Callable) -> Callable:
    @functools.wraps(func)
    def _user_creator(*args, **kwargs) -> Optional[List[User]]:
        return _sort(_creator(User, func(*args, **kwargs)), "name")

    return _user_creator


def task_result(func: Callable) -> Callable:
    @functools.wraps(func)
    def _task_result_creator(*args, **kwargs) -> Optional[List[TaskResult]]:
        return _creator(TaskResult, func(*args, **kwargs))

    return _task_result_creator
