from pathlib import Path
from utils.logger import get_logger
from test_data.lct.device_data import DeviceData
from .endpoints import GET_SIM_BATCH_DETAILS_BY_CSV, GET_SIM_BATCH_DETAILS_BY_ICCID

logger = get_logger(__name__)


class SIMBatchAPI:
    """SIM batch operations."""

    def __init__(self, client=None):
        self._client = client

    def get_sim_batch_details_by_csv(self=None, file_path=None, *args, **kwargs):
        """Upload Excel/CSV file to fetch SIM batch details."""
        if not isinstance(self, SIMBatchAPI):
            from .api_client import APIClient
            return APIClient.get_default().sim_batch.get_sim_batch_details_by_csv(file_path, *args, **kwargs)

        if isinstance(file_path, str):
            pass
        elif not file_path or hasattr(file_path, "request"):
            file_path = "./test_data/Sensorise_SIM_data_Details.xlsx"

        resolved = Path(file_path)
        if not resolved.exists():
            resolved = Path(__file__).resolve().parent.parent / "test_data" / "Sensorise_SIM_data_Details.xlsx"

        with open(resolved, "rb") as f:
            file_content = f.read()

        files = {
            "file": (
                resolved.name,
                file_content,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }
        res = self._client.post(GET_SIM_BATCH_DETAILS_BY_CSV, files=files)
        return res.get("duplicateRows", []), res.get("simDetails", {}), res.get("errors", [])

    def get_sim_batch_by_manual_upload(self=None, iccid=None, *args, **kwargs):
        """Fetch SIM details by ICCID."""
        if not isinstance(self, SIMBatchAPI):
            from .api_client import APIClient
            return APIClient.get_default().sim_batch.get_sim_batch_by_manual_upload(iccid, *args, **kwargs)

        if not iccid or hasattr(iccid, "request"):
            devices = DeviceData().get_device_data()
            iccid = devices.get("device_3")[1]

        res = self._client.post(GET_SIM_BATCH_DETAILS_BY_ICCID, json=[iccid])
        return res.get("data", {})
