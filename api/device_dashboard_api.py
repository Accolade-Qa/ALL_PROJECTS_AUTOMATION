from utils.logger import get_logger
from .endpoints import (
    GET_DISCARDED_DEVICE_COUNT,
    GET_DISPATCHED_DEVICE_COUNT,
    GET_INSTALLED_DEVICE_COUNT,
    GET_PRODUCTION_DEVICE_COUNT,
)

logger = get_logger(__name__)


class DeviceDashboardAPI:
    """Device dashboard operations."""

    def __init__(self, client=None):
        self._client = client

    def get_device_counts(self=None, *args, **kwargs):
        """Fetch device status counts from API.

        Usage:
            api = APIClient()
            counts = api.dashboard.get_device_counts()
        """
        if not isinstance(self, DeviceDashboardAPI):
            from .api_client import APIClient
            return APIClient.get_default().dashboard.get_device_counts(*args, **kwargs)

        endpoints = {
            "TOTAL PRODUCTION DEVICES": GET_PRODUCTION_DEVICE_COUNT,
            "TOTAL DISPATCHED DEVICES": GET_DISPATCHED_DEVICE_COUNT,
            "TOTAL INSTALLED DEVICES": GET_INSTALLED_DEVICE_COUNT,
            "TOTAL DISCARDED DEVICES": GET_DISCARDED_DEVICE_COUNT,
        }
        counts = {}
        for title, endpoint in endpoints.items():
            data = self._client.get(endpoint)
            val = data.get("data") if data.get("data") is not None else data.get("count", 0)
            counts[title] = int(val) if val is not None else 0

        logger.info("Fetched device counts: %s", counts)
        return counts
