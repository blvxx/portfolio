"""API checks for JSONPlaceholder Posts endpoint."""

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from api_client import PostsApiClient


SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "post.schema.json"
POST_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def api_client():
    client = PostsApiClient()
    yield client
    client.session.close()


@pytest.fixture
def schema():
    return POST_SCHEMA


@pytest.mark.smoke
def test_get_posts_returns_success_and_schema_valid_list(api_client, schema):
    response = api_client.get_posts()
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100
    for post in posts:
        validate(instance=post, schema=schema)


@pytest.mark.smoke
def test_get_single_post_has_required_fields_and_schema(api_client, schema):
    response = api_client.get_post(1)
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == 1
    validate(instance=post, schema=schema)


@pytest.mark.parametrize("post_id", [1, 10, 100])
def test_get_post_by_valid_ids(api_client, schema, post_id):
    response = api_client.get_post(post_id)
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == post_id
    validate(instance=post, schema=schema)


@pytest.mark.parametrize("user_id", [1, 2, 10])
def test_filter_posts_by_user_id(api_client, schema, user_id):
    response = api_client.get_posts(userId=user_id)
    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(post["userId"] == user_id for post in posts)
    for post in posts:
        validate(instance=post, schema=schema)

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


def test_schema_rejects_invalid_post(schema):
    invalid_post = {"userId": "not-an-integer", "id": 101, "title": "", "body": ""}
    with pytest.raises(ValidationError):
        validate(instance=invalid_post, schema=schema)
