from utils.logger import get_logger
from utils.helpers import Helpers
from .endpoints import (
    GENERATE_TICKET_TOKEN,
    GENERATE_TML_TICKET,
    GET_DASHBOARD_COUNTS,
    GET_STATUS_UPDATE_LOGS,
)

logger = get_logger(__name__)


class TmlRequestAPI:
    """TML CRM ticketing operations."""

    def __init__(self, client=None):
        self._client = client
        self.ticket_token = None

    @staticmethod
    def _raise_for_failed_response(response, operation):
        if response.ok:
            return

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        message = (
            response_data.get("message")
            if isinstance(response_data, dict)
            else None
        )
        details = f": {message}" if message else ""
        raise RuntimeError(
            f"{operation} failed [{response.status_code}]{details}"
        )

    @property
    def ticket_base_url(self):
        from config import config
        return getattr(config, "TICKET_BASE_URL", "https://aepl-tcu4g-qa.accoladeelectronics.com:6109").rstrip("/")

    def get_token(self=None, *args, **kwargs):
        """Retrieve CRM token."""
        if not isinstance(self, TmlRequestAPI):
            from .api_client import APIClient
            return APIClient.get_default().tml.get_token(*args, **kwargs)

        if self.ticket_token:
            return self.ticket_token

        from config import config
        url = f"{self.ticket_base_url}{GENERATE_TICKET_TOKEN}"
        username = getattr(config, "TICKET_USERNAME", "")
        password = getattr(config, "TICKET_PASSWORD", "")
        if not username or not password:
            raise RuntimeError(
                "TML ticket credentials are not configured. Set "
                "TICKET_USERNAME and TICKET_PASSWORD in the environment."
            )

        response = self._client.session.post(url, data={"username": username, "password": password}, timeout=20)
        self._raise_for_failed_response(response, "TML ticket token request")

        token = response.json().get("token")
        if not token:
            raise RuntimeError(
                f"TML ticket token request failed [{response.status_code}]: "
                "response did not contain a token"
            )

        self.ticket_token = token
        return token

    def post_tml_request_log(self=None, *args, **kwargs):
        """Generate ticket request."""
        if not isinstance(self, TmlRequestAPI):
            from .api_client import APIClient
            return APIClient.get_default().tml.post_tml_request_log(*args, **kwargs)

        token = self.get_token()
        state_name, state_code = Helpers.generate_random_indian_state_data()
        payload = [{
            "VIN_NO": f"ACCDEV07241580{Helpers.generate_random_number(3)}",
            "ICCID": "89916420534724851291",
            "UIN_NO": "ACON4NA082300092233",
            "DEVICE_IMEI": "861564061380138",
            "DEVICE_MAKE": "Accolade",
            "DEVICE_MODEL": "AEPL051401",
            "ENGINE_NO": "ENGINE_FIXED_00001",
            "REG_NUMBER": "AN01AB1000",
            "REGISTERED_MOBILE_NUMBER": Helpers.generate_random_phone(),
            "VEHICLE_OWNER_FIRST_NAME": Helpers.generate_random_string(5),
            "VEHICLE_OWNER_MIDDLE_NAME": "",
            "VEHICLE_OWNER_LAST_NAME": Helpers.generate_random_string(5),
            "ADDRESS_LINE_1": "SHIVANE",
            "ADDRESS_LINE_2": "SHIVANE",
            "VEHICLE_OWNER_CITY": "PUNE",
            "VEHICLE_OWNER_DISTRICT": "PUNE",
            "VEHICLE_OWNER_STATE": state_name,
            "VEHICLE_OWNER_COUNTRY": "India",
            "VEHICLE_OWNER_PINCODE": "411045",
            "VEHICLE_OWNER_REGISTERED_MOBILE": Helpers.generate_random_phone(),
            "POS_CODE": "AB123",
            "POA_DOC_NAME": "PANAB123",
            "POA_DOC_NO": "PAN1AB123",
            "POI_DOC_TYPE": "ADHARAB123",
            "POI_DOC_NO": "ADHARXYZ123",
            "RTO_OFFICE_CODE": f"{state_code}12",
            "RTO_STATE": state_code,
            "PRIMARY_OPERATOR": "BSNL",
            "SECONDARY_OPERATOR": "BHA",
            "PRIMARY_MOBILE_NUMBER": Helpers.generate_random_phone(),
            "SECONDARY_MOBILE_NUMBER": Helpers.generate_random_phone(),
            "VEHICLE_MODEL": "NANO",
            "DEALER_CODE": "1000",
            "COMMERCIAL_ACTIVATION_START_DATE": Helpers.get_timestamp(fmt="%Y-%m-%d"),
            "COMMERCIAL_ACTIVATION_EXPIRY_DATE": Helpers.get_future_date(2, fmt="%Y-%m-%d"),
            "MFG_YEAR": "2024",
            "ACCOLADE_POSTING_DATE_TIME": Helpers.get_timestamp(fmt="%Y-%m-%d"),
            "INVOICE_DATE": Helpers.get_timestamp(fmt="%Y-%m-%d"),
            "INVOICE_NUMBER": "AEPL100000000",
            "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": "2",
        }]

        url = f"{self.ticket_base_url}{GENERATE_TML_TICKET}"
        headers = {"token": token, "Content-Type": "application/json"}
        response = self._client.session.post(url, json=payload, headers=headers, timeout=25)
        self._raise_for_failed_response(response, "TML ticket request")
        res_json = response.json()
        data_list = res_json.get("data", [])
        data = data_list[0] if (isinstance(data_list, list) and len(data_list) > 0) else (data_list if isinstance(data_list, dict) else {})

        ticket_number = data.get("TICKET_NO") or data.get("ticketNo") or res_json.get("TICKET_NO", "")
        VIN = data.get("VIN_NO") or (payload[0]["VIN_NO"] if payload else "")
        UIN = data.get("UIN_NO") or (payload[0]["UIN_NO"] if payload else "")
        ICCID = data.get("ICCID") or (payload[0]["ICCID"] if payload else "")

        return payload, VIN, UIN, ICCID, ticket_number, data

    def get_status_update_logs(self=None, vin_no=None, *args, **kwargs):
        """Fetch status update logs."""
        if not isinstance(self, TmlRequestAPI):
            from .api_client import APIClient
            return APIClient.get_default().tml.get_status_update_logs(vin_no, *args, **kwargs)

        token = self.get_token()
        endpoint = GET_STATUS_UPDATE_LOGS + (f"?vinNo={vin_no}" if vin_no else "")
        headers = {"token": token, "Content-Type": "application/json"}
        res = self._client.session.get(f"{self.ticket_base_url}{endpoint}", headers=headers, timeout=25)
        return res.json() if res.ok else {}

    def get_dash_counts(self=None, params=None, *args, **kwargs):
        """Fetch dashboard counts."""
        if not isinstance(self, TmlRequestAPI):
            from .api_client import APIClient
            return APIClient.get_default().tml.get_dash_counts(params, *args, **kwargs)

        token = self.get_token()
        if not params:
            params = "state=&dealer=&toDate=&fromDate=&assignTo=&initiatedBy=&ticketStatusFilter=&deviceType=&search=&id=&ticketCompletedAtFromDate=&ticketCompletedAtToDate=&tatType="
        headers = {"token": token, "Content-Type": "application/json"}
        res = self._client.session.get(f"{self.ticket_base_url}{GET_DASHBOARD_COUNTS}?{params}", headers=headers, timeout=25)
        return res.json() if res.ok else {}


TmlRequestApi = TmlRequestAPI
