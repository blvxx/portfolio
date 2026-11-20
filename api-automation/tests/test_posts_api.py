"""Contract and functional tests for the JSONPlaceholder Posts API."""

import json
from pathlib import Path

import allure
import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from api_client import PostsApiClient


SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "post.schema.json"
POST_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def api_client():
    with PostsApiClient() as client:
        yield client


@pytest.fixture
def schema():
    return POST_SCHEMA


def assert_json_response(response, expected_status=200):
    """Assert the common JSON API response contract."""
    assert response.status_code == expected_status
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower()


@allure.feature("Posts API")
@allure.story("List posts")
@pytest.mark.smoke
@pytest.mark.contract
def test_get_posts_returns_100_schema_valid_items(api_client, schema):
    response = api_client.get_posts()
    assert_json_response(response)

    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100

    validator = Draft202012Validator(schema)
    for post in posts:
        validator.validate(post)


@allure.feature("Posts API")
@allure.story("Get post details")
@pytest.mark.smoke
@pytest.mark.contract
def test_get_single_post_has_required_fields_and_schema(api_client, schema):
    response = api_client.get_post(1)
    assert_json_response(response)

    post = response.json()
    assert post["id"] == 1
    Draft202012Validator(schema).validate(post)
    allure.attach(
        json.dumps(post, ensure_ascii=False, indent=2),
        name="post-1-response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.feature("Posts API")
@allure.story("Valid post IDs")
@pytest.mark.contract
@pytest.mark.parametrize("post_id", [1, 10, 50, 100])
def test_get_post_by_valid_ids(api_client, schema, post_id):
    response = api_client.get_post(post_id)
    assert_json_response(response)

    post = response.json()
    assert post["id"] == post_id
    Draft202012Validator(schema).validate(post)


@allure.feature("Posts API")
@allure.story("Filter posts by user")
@pytest.mark.contract
@pytest.mark.parametrize("user_id", [1, 2, 5, 10])
def test_filter_posts_by_user_id(api_client, schema, user_id):
    response = api_client.get_posts(userId=user_id)
    assert_json_response(response)

    posts = response.json()
    assert posts, f"Expected posts for userId={user_id}"
    assert all(post["userId"] == user_id for post in posts)
    for post in posts:
        Draft202012Validator(schema).validate(post)


@allure.feature("Posts API")
@allure.story("Negative post ID scenarios")
@pytest.mark.negative
@pytest.mark.parametrize("post_id", [0, -1, 999999])
def test_unknown_or_invalid_post_id_returns_404(api_client, post_id):
    response = api_client.get_post(post_id)
    assert_json_response(response, expected_status=404)
    assert response.json() == {}


@allure.feature("Posts API")
@allure.story("Unknown user filter")
@pytest.mark.negative
@pytest.mark.parametrize("user_id", [0, 999, -5])
def test_filter_with_unknown_user_returns_empty_list(api_client, user_id):
    response = api_client.get_posts(userId=user_id)
    assert_json_response(response)
    assert response.json() == []


@allure.feature("JSON Schema")
@allure.story("Schema definition is valid")
@pytest.mark.unit
def test_post_schema_definition_is_valid(schema):
    Draft202012Validator.check_schema(schema)


@allure.feature("JSON Schema")
@allure.story("Reject invalid response payloads")
@pytest.mark.unit
@pytest.mark.parametrize(
    "invalid_post",
    [
        {"userId": "not-an-integer", "id": 1, "title": "Title", "body": "Body"},
        {"userId": 1, "id": 101, "title": "Title", "body": "Body"},
        {"userId": 1, "id": 1, "title": "", "body": "Body"},
        {"userId": 1, "id": 1, "title": "Title"},
        {"userId": 1, "id": 1, "title": "Title", "body": "Body", "extra": True},
    ],
)
def test_schema_rejects_invalid_post(schema, invalid_post):
    with pytest.raises(ValidationError):
        validate(instance=invalid_post, schema=schema)
