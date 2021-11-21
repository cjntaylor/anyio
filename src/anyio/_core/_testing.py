from typing import Coroutine, List, Optional

from ._eventloop import get_asynclib


class TaskInfo:
    """
    Represents an asynchronous task.

    :ivar int id: the unique identifier of the task
    :ivar parent_id: the identifier of the parent task, if any
    :vartype parent_id: Optional[int]
    :ivar str name: the description of the task (if any)
    :ivar ~collections.abc.Coroutine coro: the coroutine object of the task
    """

    __slots__ = '_name', 'id', 'parent_id', 'name', 'coro'

    def __init__(self, id: int, parent_id: Optional[int], name: Optional[str], coro: Coroutine):
        func = get_current_task
        self._name = f'{func.__module__}.{func.__qualname__}'
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.coro = coro

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TaskInfo):
            return self.id == other.id

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id!r}, name={self.name!r})'

    def _unwrap(self) -> 'TaskInfo':
        return self


def get_current_task() -> TaskInfo:
    """
    Return the current task.

    :return: a representation of the current task

    """
    return get_asynclib().get_current_task()


def get_running_tasks() -> List[TaskInfo]:
    """
    Return a list of running tasks in the current event loop.

    :return: a list of task info objects

    """
    return get_asynclib().get_running_tasks()


async def wait_all_tasks_blocked() -> None:
    """Wait until all other tasks are waiting for something."""
    await get_asynclib().wait_all_tasks_blocked()
