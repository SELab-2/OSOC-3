import enum
from asyncio import Queue, Lock
from enum import Enum
from typing import Any

from fastapi import Depends, Request

from src.app.utils.dependencies import get_edition
from src.database.models import Edition


@enum.unique
class EventType(Enum):
    # Project
    PROJECT = 1
    # Project Role
    PROJECT_ROLE = 2
    # Project Role Suggestion
    PROJECT_ROLE_SUGGESTION = 3
    # Student
    STUDENT = 4
    # Student Suggestion
    STUDENT_SUGGESTION = 5


class LiveEventParameters:
    def __init__(self, method: str, path_ids: dict):
        self.method: str = method
        self.path_ids: dict = path_ids
        self.event_type: EventType = LiveEventParameters.get_event_type(path_ids)

    @staticmethod
    def get_event_type(path_ids: dict) -> EventType:
        match path_ids:
            case {'project_id': _}:
                return EventType.PROJECT
            case {'project_id': _, 'project_role_id': _}:
                return EventType.PROJECT_ROLE
            case {'project_id': _, 'project_role_id': _, 'student_id': _}:
                return EventType.PROJECT_ROLE_SUGGESTION
            case {'student_id': _}:
                return EventType.STUDENT
            case {'student_id': _, 'suggestion_id': _}:
                return EventType.STUDENT_SUGGESTION
            case _:
                raise Exception('Invalid path_ids')

    async def json(self) -> dict:
        return {
            'method': self.method,
            'pathIds': self.path_ids,
            'eventType': self.event_type.value()
        }


class DataPublisher:
    def __init__(self):
        self.queues: list[Queue] = []
        self._broadcast_lock: Lock = Lock()

    async def subscribe(self) -> Queue:
        queue: Queue = Queue()
        self.queues.append(queue)
        return queue

    async def unsubscribe(self, queue: Queue) -> None:
        self.queues.remove(queue)

    async def broadcast(self, live_event: LiveEventParameters) -> None:
        data: dict = await live_event.json()

        async with self._broadcast_lock:
            for queue in self.queues:
                await queue.put(data)


# Map containing a publishers for each edition, since access is managed per edition
_publisher_by_edition: dict[Edition, DataPublisher] = dict()


async def get_publisher(edition: Edition = Depends(get_edition)) -> DataPublisher:
    if edition not in _publisher_by_edition:
        _publisher_by_edition[edition] = DataPublisher()
    return _publisher_by_edition[edition]


async def live(request: Request, publisher: DataPublisher = Depends(get_publisher)):
    path_ids: dict = request.path_params.copy()
    del path_ids['edition_name']
    live_event: LiveEventParameters = LiveEventParameters(
        request.method,
        request.path_params
    )
    yield  # yield to make sure this part happens after the request has been handled
    await publisher.broadcast(live_event)
