"""Shared base behavior for feature-specific API services."""

import requests


class APIService:
    def __init__(self, client):
        self._client = client

    @staticmethod
    def _delete_items(response, delete_item, item_name):
        total = response.get("totalItems", 0)
        failed_ids = []
        for item_id in range(1, total + 1):
            try:
                delete_item(item_id)
            except requests.HTTPError as error:
                if (
                    error.response is None
                    or f"Cannot delete {item_name}" not in error.response.text
                ):
                    raise
                failed_ids.append(item_id)

        return total, failed_ids
