"""Unit tests for the reusable API client (no network calls)."""

from unittest.mock import Mock

import pytest
import requests

from api_client import PostsApiClient


pytestmark = pytest.mark.unit


def make_session():
    session = Mock(spec=requests.Session)
    session.headers = {}
    return session


def test_client_sets_default_headers_and_timeout():
    session = make_session()
    client = PostsApiClient(session=session, timeout=4)

    assert session.headers["Accept"] == "application/json"
    assert session.headers["User-Agent"] == "blvxx-api-automation/1.0"
    assert client.timeout == 4
    assert client.base_url == PostsApiClient.DEFAULT_BASE_URL


def test_get_posts_passes_query_params_and_timeout():
    session = make_session()
    expected_response = object()
    session.get.return_value = expected_response
    client = PostsApiClient(
        session=session,
        timeout=3,
        base_url="https://api.example.test/",
    )

    response = client.get_posts(userId=2)

    assert response is expected_response
    session.get.assert_called_once_with(
        "https://api.example.test/posts",
        params={"userId": 2},
        timeout=3,
    )


def test_get_posts_without_filters_uses_no_query_params():
    session = make_session()
    client = PostsApiClient(session=session)

    client.get_posts()

    session.get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts",
        params=None,
        timeout=10.0,
    )


def test_get_post_builds_expected_resource_url():
    session = make_session()
    client = PostsApiClient(
        session=session,
        base_url="https://api.example.test",
    )

    client.get_post(42)

    session.get.assert_called_once_with(
        "https://api.example.test/posts/42",
        timeout=10.0,
    )


@pytest.mark.parametrize("timeout", [0, -1, -0.5])
def test_client_rejects_non_positive_timeout(timeout):
    with pytest.raises(ValueError, match="timeout must be greater than zero"):
        PostsApiClient(session=make_session(), timeout=timeout)


def test_transport_timeout_is_not_silently_swallowed():
    session = make_session()
    session.get.side_effect = requests.Timeout("request timed out")
    client = PostsApiClient(session=session)

    with pytest.raises(requests.Timeout, match="request timed out"):
        client.get_post(1)


def test_context_manager_closes_session():
    session = make_session()

    with PostsApiClient(session=session):
        pass

    session.close.assert_called_once_with()
