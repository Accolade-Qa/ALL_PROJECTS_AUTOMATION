"""API operations used by the ATCU OTA batch page."""

from urllib.parse import quote

from ..api_service import APIService


GET_ATCU_OTA_BATCH_LIST = "/api/ota/fetchOtaBatchList?pageNo={page_no}&size={size}"
GET_ATCU_OTA_BATCH_KPI = (
    "/api/ota/fetchOtaBatchKpi?pageNo={page_no}&size={size}"
    "&batchRefId={batch_ref_id}&kpiSelected={kpi_selected}"
)


class AtcuOtaPageAPI(APIService):
    def get_ota_batch_list(self, page_no=1, size=10):
        endpoint = GET_ATCU_OTA_BATCH_LIST.format(page_no=page_no, size=size)
        result = self._client.get(endpoint)
        batches = result.get("data", {}).get("batchDeviceData", [])
        batch_ids = [
            batch["_id"]
            for batch in batches
            if isinstance(batch, dict) and batch.get("_id")
        ]
        return result, batch_ids

    def get_ota_batch_kpi(
        self,
        batch_ref_id=None,
        page_no=1,
        size=100,
        search="",
        kpi_selected="All",
    ):
        endpoint = GET_ATCU_OTA_BATCH_KPI.format(
            page_no=page_no,
            size=size,
            search=quote(search, safe=""),
            batch_ref_id=quote(str(batch_ref_id or ""), safe=""),
            kpi_selected=quote(kpi_selected, safe=""),
        )
        return self._client.get(endpoint)
