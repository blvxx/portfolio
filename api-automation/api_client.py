"""Reusable HTTP client for the JSONPlaceholder Posts API."""

from __future__ import annotations

import os
from typing import Any, Mapping

import requests


class PostsApiClient:
    """Small requests-based client used by the API test suite.

    The base URL can be overridden with API_BASE_URL or the constructor,
    which makes it possible to point the same tests at another compatible
    environment without changing test code.
    """

    DEFAULT_BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(
        self,
        session: requests.Session | None = None,
        timeout: float = 10.0,
        base_url: str | None = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.session = session if session is not None else requests.Session()
        self.timeout = timeout
        self.base_url = (
            base_url or os.getenv("API_BASE_URL") or self.DEFAULT_BASE_URL
        ).rstrip("/")

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "blvxx-api-automation/1.0",
            }
        )

    def get_posts(self, **params: Any) -> requests.Response:
        """Return posts, optionally filtered by query parameters."""
        return self.session.get(
            f"{self.base_url}/posts",
            params=params or None,
            timeout=self.timeout,
        )

    def get_post(self, post_id: int) -> requests.Response:
        """Return a post by ID.

        The client intentionally does not validate the ID locally: negative
        and unknown values are useful inputs for API negative tests.
        """
        return self.session.get(
            f"{self.base_url}/posts/{post_id}",
            timeout=self.timeout,
        )

    def get_post_comments(self, post_id: int) -> requests.Response:
        """Return comments related to a post through the nested resource route."""
        return self.session.get(
            f"{self.base_url}/posts/{post_id}/comments",
            timeout=self.timeout,
        )

    def create_post(self, payload: Mapping[str, Any]) -> requests.Response:
        """Send POST /posts with a JSON payload."""
        return self.session.post(
            f"{self.base_url}/posts",
            json=dict(payload),
            timeout=self.timeout,
        )

    def replace_post(
        self, post_id: int, payload: Mapping[str, Any]
    ) -> requests.Response:
        """Send PUT /posts/{id} with a complete replacement payload."""
        return self.session.put(
            f"{self.base_url}/posts/{post_id}",
            json=dict(payload),
            timeout=self.timeout,
        )

    def patch_post(
        self, post_id: int, payload: Mapping[str, Any]
    ) -> requests.Response:
        """Send PATCH /posts/{id} with a partial update payload."""
        return self.session.patch(
            f"{self.base_url}/posts/{post_id}",
            json=dict(payload),
            timeout=self.timeout,
        )

    def delete_post(self, post_id: int) -> requests.Response:
        """Send DELETE /posts/{id}. The demo API simulates the deletion."""
        return self.session.delete(
            f"{self.base_url}/posts/{post_id}",
            timeout=self.timeout,
        )

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self) -> "PostsApiClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()
