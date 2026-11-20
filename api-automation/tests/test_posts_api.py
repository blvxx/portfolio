"""API checks for JSONPlaceholder Posts endpoint."""

import pytest

from api_client import PostsApiClient


@pytest.fixture
def api_client():
    client = PostsApiClient()
    yield client
    client.session.close()


@pytest.mark.smoke
def test_get_posts_returns_success_and_list(api_client):
    response = api_client.get_posts()
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100


@pytest.mark.smoke
def test_get_single_post_has_required_fields(api_client):
    response = api_client.get_post(1)
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == 1
    assert isinstance(post["userId"], int)
    assert isinstance(post["title"], str) and post["title"].strip()
    assert isinstance(post["body"], str) and post["body"].strip()


@pytest.mark.parametrize("post_id", [1, 10, 100])
def test_get_post_by_valid_ids(api_client, post_id):
    response = api_client.get_post(post_id)
    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.parametrize("user_id", [1, 2, 10])
def test_filter_posts_by_user_id(api_client, user_id):
    response = api_client.get_posts(userId=user_id)
    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(post["userId"] == user_id for post in posts)


@pytest.mark.parametrize("post_id", [0, -1, 999999])
def test_unknown_or_invalid_post_id_returns_404(api_client, post_id):
    response = api_client.get_post(post_id)
    assert response.status_code == 404
    assert response.json() == {}


@pytest.mark.parametrize("user_id", [0, 999, -5])
def test_filter_with_unknown_user_returns_empty_list(api_client, user_id):
    response = api_client.get_posts(userId=user_id)
    assert response.status_code == 200
    assert response.json() == []
