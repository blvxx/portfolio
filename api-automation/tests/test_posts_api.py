"""Smoke and contract-style checks for JSONPlaceholder Posts API."""

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10


@pytest.fixture
def api_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


def test_get_posts_returns_success_and_list(api_session):
    response = api_session.get(f"{BASE_URL}/posts", timeout=TIMEOUT)


    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0



def test_get_single_post_has_required_fields(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=TIMEOUT)


    assert response.status_code == 200
    post = response.json()
    assert post["id"] == 1
    assert isinstance(post["userId"], int)
    assert isinstance(post["title"], str) and post["title"]
    assert isinstance(post["body"], str) and post["body"]



def test_filter_posts_by_user_id(api_session):
    user_id = 1
    response = api_session.get(
        f"{BASE_URL}/posts", params={"userId": user_id}, timeout=TIMEOUT
    )


    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(post["userId"] == user_id for post in posts)



def test_unknown_post_returns_not_found(api_session):
    response = api_session.get(f"{BASE_URL}/posts/999999", timeout=TIMEOUT)


    assert response.status_code == 404
