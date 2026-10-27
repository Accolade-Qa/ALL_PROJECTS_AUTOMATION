"""API operations used by the SIM batch details page."""

from pathlib import Path

from test_data.lct.device_data import DeviceData

from .api_service import APIService


GET_SIM_BATCH_DETAILS_BY_CSV = "/sensoriseSimData/getSimDetailsByIccidUsingCsv"
GET_SIM_BATCH_DETAILS_BY_ICCID = "/sensoriseSimData/getSimDetailsByIccid"


class SIMBatchAPI(APIService):
    def get_sim_batch_details_by_csv(self, file_path=None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parent.parent
                / "test_data"
                / "Sensorise_SIM_data_Details.xlsx"
            )

        file_path = Path(file_path)
        if not file_path.exists():
            file_path = (
                Path(__file__).resolve().parent.parent
                / "test_data"
                / "Sensorise_SIM_data_Details.xlsx"
            )

        with file_path.open("rb") as file:
            files = {
                "file": (
                    file_path.name,
                    file.read(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            }

        response = self._client.post(GET_SIM_BATCH_DETAILS_BY_CSV, files=files)
        return (
            response.get("duplicateRows", []),
            response.get("simDetails", {}),
            response.get("errors", []),
        )

    def get_sim_batch_by_manual_upload(self, iccid=None):
        if iccid is None:
            device = DeviceData().get_device_data().get("device_3")
            if not device:
                raise ValueError("Device test data does not contain device_3")
            iccid = device[1]

        response = self._client.post(
            GET_SIM_BATCH_DETAILS_BY_ICCID,
            json=[iccid],
        )
        return response.get("data", {})
