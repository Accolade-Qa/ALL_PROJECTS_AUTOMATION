"""API operations used by the device dashboard page."""

from .api_service import APIService


DEVICE_COUNTS = {
    "TOTAL PRODUCTION DEVICES": (
        "/device/getProductionDeviceCount?selectedDeviceModelId=&selectedCustomerId="
    ),
    "TOTAL DISPATCHED DEVICES": (
        "/device/getDispatchDeviceCount?selectedDeviceModelId=&selectedCustomerId="
    ),
    "TOTAL INSTALLED DEVICES": (
        "/device/getInstalledDeviceCount?selectedDeviceModelId=&selectedCustomerId="
    ),
    "TOTAL DISCARDED DEVICES": (
        "/device/getDiscardedDeviceCount?selectedDeviceModelId=&selectedCustomerId="
    ),
}


class DeviceDashboardAPI(APIService):
    def get_device_counts(self):
        counts = {}
        for title, endpoint in DEVICE_COUNTS.items():
            response = self._client.get(endpoint)
            value = response.get("data")
            if value is None:
                value = response.get("count", 0)
            counts[title] = int(value or 0)
        return counts
