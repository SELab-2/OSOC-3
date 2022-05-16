import enum
from asyncio import Queue as AsyncQueue, Lock
from enum import Enum
from queue import Queue

from fastapi import Depends, Request, Response, FastAPI

from src.app.utils.dependencies import get_edition
from src.database.models import Edition


@enum.unique
class EventType(Enum):
    """Event Type Enum"""
    # Project
    PROJECT = 0
    # Project Role
    PROJECT_ROLE = 1
    # Project Role Suggestion
    PROJECT_ROLE_SUGGESTION = 2
    # Student
    STUDENT = 3
    # Student Suggestion
    STUDENT_SUGGESTION = 4


class LiveEventParameters:
    """Construct a live event data object"""

    def __init__(self, method: str, path_ids: dict):
        """Initialize the object"""
        self.method: str = method
        self.path_ids: dict = path_ids
        self.event_type: EventType = LiveEventParameters.get_event_type(path_ids)

    @staticmethod
    def get_event_type(path_ids: dict) -> EventType:
        """Parse the event type from given path ids"""
        match path_ids:
            case {'project_id': _, 'project_role_id': _, 'student_id': _}:
                return EventType.PROJECT_ROLE_SUGGESTION
            case {'project_id': _, 'project_role_id': _}:
                return EventType.PROJECT_ROLE
            case {'project_id': _}:
                return EventType.PROJECT
            case {'student_id': _, 'suggestion_id': _}:
                return EventType.STUDENT_SUGGESTION
            case {'student_id': _}:
                return EventType.STUDENT
            case _:
                raise Exception('Invalid path_ids')

    async def json(self) -> dict:
        """Generate json dict for live event"""
        return {
            'method': self.method,
            'pathIds': self.path_ids,
            'eventType': self.event_type.value
        }


class DataPublisher:
    """Event Bus"""

    def __init__(self):
        """Initialize"""
        self.queues: list[AsyncQueue] = []
        self._broadcast_lock: Lock = Lock()

    async def subscribe(self) -> AsyncQueue:
        """Subscribe to the event bus, returns a queue where your events will be published"""
        queue: AsyncQueue = AsyncQueue()
        self.queues.append(queue)
        return queue

    async def unsubscribe(self, queue: AsyncQueue) -> None:
        """No longer receive updates"""
        self.queues.remove(queue)

    async def broadcast(self, live_event: LiveEventParameters) -> None:
        """Notify all subscribed listeners"""
        data: dict = await live_event.json()

        async with self._broadcast_lock:
            for queue in self.queues:
                await queue.put(data)


# Map containing a publishers for each edition, since access is managed per edition
_publisher_by_edition: dict[str, DataPublisher] = {}


async def get_publisher(edition: Edition = Depends(get_edition)) -> DataPublisher:
    """Get a publisher for the given edition"""
    if edition.name not in _publisher_by_edition:
        _publisher_by_edition[edition.name] = DataPublisher()
    return _publisher_by_edition[edition.name]


async def live(request: Request, publisher: DataPublisher = Depends(get_publisher)):
    """Add the publisher for the current edition to the queue
    Indicates to the middleware the event might trigger a live data event
    """
    queue: Queue = request.state.websocket_publisher_queue
    queue.put_nowait(publisher)


def install_middleware(app: FastAPI):
    """Middleware for sending actions upon successful requests to live endpoints"""
    @app.middleware("http")
    async def live_middleware(request: Request, call_next) -> Response:
        queue: Queue[DataPublisher] = Queue()
        request.state.websocket_publisher_queue = queue

        response: Response = await call_next(request)

        if 200 <= response.status_code < 300 and not queue.empty():
            if (publisher := queue.get_nowait()) is not None:
                path_ids: dict = request.path_params.copy()
                del path_ids['edition_name']
                live_event: LiveEventParameters = LiveEventParameters(
                    request.method,
                    request.path_params
                )
                await publisher.broadcast(live_event)

        return response
