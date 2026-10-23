from urllib.parse import quote
from utils.logger import get_logger
from ..endpoints import GET_ATCU_OTA_BATCH_KPI, GET_ATCU_OTA_BATCH_LIST

logger = get_logger(__name__)


class AtcuOtaPageAPI:
    """ATCU OTA operations."""

    def __init__(self, client=None):
        self._client = client

    def get_ota_batch_list(self=None, page_no=1, size=10, search="", *args, **kwargs):
        """Fetch OTA batch list."""
        if not isinstance(self, AtcuOtaPageAPI):
            from ..api_client import APIClient
            return APIClient.get_default().ota.get_ota_batch_list(page_no, size, search, *args, **kwargs)

        endpoint = GET_ATCU_OTA_BATCH_LIST.format(page_no=page_no, size=size)
        result = self._client.get(endpoint)
        batches = result.get("data", {}).get("batchDeviceData", [])
        batch_ids = [b["_id"] for b in batches if isinstance(b, dict) and b.get("_id")]
        return result, batch_ids

    def get_ota_batch_kpi(self=None, batch_ref_id=None, *args, **kwargs):
        """Fetch OTA batch KPI."""
        if not isinstance(self, AtcuOtaPageAPI):
            from ..api_client import APIClient
            return APIClient.get_default().ota.get_ota_batch_kpi(batch_ref_id, *args, **kwargs)

        for a in args:
            if isinstance(a, (int, str)) and not hasattr(a, "request"):
                batch_ref_id = a
                break
        batch_ref_id = kwargs.get("batch_ref_id", batch_ref_id)
        endpoint = GET_ATCU_OTA_BATCH_KPI.format(
            page_no=kwargs.get("pageNo", 1),
            size=kwargs.get("size", 100),
            search=quote(kwargs.get("search", ""), safe=""),
            batch_ref_id=quote(str(batch_ref_id or ""), safe=""),
            kpi_selected=quote(kwargs.get("kpi_selected", "All"), safe=""),
        )
        return self._client.get(endpoint)
