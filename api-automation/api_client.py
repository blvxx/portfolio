"""Reusable HTTP client for the JSONPlaceholder Posts API."""

from __future__ import annotations

import os
from typing import Any

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

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self) -> "PostsApiClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()
