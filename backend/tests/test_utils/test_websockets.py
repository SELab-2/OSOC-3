import pytest

from src.app.utils.websockets import LiveEventParameters, EventType


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
