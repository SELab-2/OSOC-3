from asyncio import Queue

import pytest

from src.app.utils.websockets import LiveEventParameters, EventType, DataPublisher


async def test_parse_event_type_project():
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'project_id': 1}
    )

    assert live_event.event_type == EventType.PROJECT


async def test_parse_event_type_project_role():
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'project_id': 1, 'project_role_id': 2}
    )

    assert live_event.event_type == EventType.PROJECT_ROLE


async def test_parse_event_type_pr_suggestion():
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'project_id': 1, 'project_role_id': 2, 'student_id': 2}
    )

    assert live_event.event_type == EventType.PROJECT_ROLE_SUGGESTION


async def test_parse_event_type_student():
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'student_id': 2}
    )

    assert live_event.event_type == EventType.STUDENT


async def test_parse_event_type_student_suggestion():
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'student_id': 2, 'suggestion_id': 1}
    )

    assert live_event.event_type == EventType.STUDENT_SUGGESTION


async def test_parse_event_type_invalid():
    with pytest.raises(Exception):
        LiveEventParameters(
            'POST',
            {'blargh': 1}
        )


async def test_event_format():
    live_event: dict = await LiveEventParameters(
        'POST',
        {'student_id': 2, 'suggestion_id': 1}
    ).json()

    assert 'method' in live_event
    assert 'pathIds' in live_event
    assert type(live_event['pathIds']) == dict
    assert 'eventType' in live_event


async def test_data_publisher_subscribe():
    dp: DataPublisher = DataPublisher()
    assert await dp.subscribe() is not None
    assert len(dp.queues) == 1


async def test_data_publisher_unsubscribe():
    dp: DataPublisher = DataPublisher()
    q: Queue = await dp.subscribe()
    await dp.unsubscribe(q)
    assert len(dp.queues) == 0


async def test_data_publisher_broadcast():
    dp: DataPublisher = DataPublisher()
    qs: list[Queue] = [await dp.subscribe() for _ in range(10)]
    live_event: LiveEventParameters = LiveEventParameters(
        'POST',
        {'project_id': 1}
    )

    await dp.broadcast(live_event)
    for q in qs:
        data: dict = await q.get()
        assert data == await live_event.json()
