"""Reusable HTTP client for JSONPlaceholder posts API."""

from typing import Any


import requests


class PostsApiClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"


    def __init__(self, session: requests.Session | None = None, timeout: int = 10):
        self.session = session or requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Accept": "application/json"})


    def get_posts(self, **params: Any) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/posts", params=params, timeout=self.timeout
        )


    def get_post(self, post_id: int) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/posts/{post_id}", timeout=self.timeout
        )
