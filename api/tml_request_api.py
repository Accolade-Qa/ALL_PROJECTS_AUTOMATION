"""API operations used by ATCU ticket and status-log pages."""

from config import config
from utils.helpers import Helpers

from .api_service import APIService


GENERATE_TICKET_TOKEN = "/api/crm/generateToken"
GENERATE_TML_TICKET = "/api/crm/generateTickets"
GET_STATUS_UPDATE_LOGS = "/api/crm/getStatusUpdateLogs"
GET_DASHBOARD_COUNTS = "/api/crm/getDashCounts"
DEFAULT_DASHBOARD_FILTERS = (
    "state=&dealer=&toDate=&fromDate=&assignTo=&initiatedBy="
    "&ticketStatusFilter=&deviceType=&search=&id="
    "&ticketCompletedAtFromDate=&ticketCompletedAtToDate=&tatType="
)


class TmlRequestAPI(APIService):
    def __init__(self, client):
        super().__init__(client)
        self._ticket_token = None

    def build_ticket_url(self, endpoint):
        base_url = getattr(
            config,
            "TICKET_BASE_URL",
            "https://aepl-tcu4g-qa.accoladeelectronics.com:6109",
        )
        return base_url.rstrip("/") + endpoint

    def _ticket_request(self, method, endpoint, **kwargs):
        response = getattr(self._client.session, method)(
            self.build_ticket_url(endpoint),
            **kwargs,
        )
        if not response.ok:
            try:
                message = response.json().get("message")
            except ValueError:
                message = None
            details = f": {message}" if message else ""
            raise RuntimeError(
                f"TML request failed [{response.status_code}]{details}"
            )
        return response.json() if response.text else {}

    def get_token(self):
        if self._ticket_token:
            return self._ticket_token

        username = getattr(config, "TICKET_USERNAME", "")
        password = getattr(config, "TICKET_PASSWORD", "")
        if not username or not password:
            raise RuntimeError(
                "TML ticket credentials are not configured. Set "
                "TICKET_USERNAME and TICKET_PASSWORD in the environment."
            )

        response = self._ticket_request(
            "post",
            GENERATE_TICKET_TOKEN,
            data={"username": username, "password": password},
            timeout=20,
        )
        self._ticket_token = response.get("token")
        if not self._ticket_token:
            raise ValueError("TML token response did not contain a token")
        return self._ticket_token

    def _build_ticket_payload(self):
        state_name, state_code = Helpers.generate_random_indian_state_data()
        return [
            {
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
                "COMMERCIAL_ACTIVATION_START_DATE": Helpers.get_timestamp(
                    fmt="%Y-%m-%d"
                ),
                "COMMERCIAL_ACTIVATION_EXPIRY_DATE": Helpers.get_future_date(
                    2, fmt="%Y-%m-%d"
                ),
                "MFG_YEAR": "2024",
                "ACCOLADE_POSTING_DATE_TIME": Helpers.get_timestamp(
                    fmt="%Y-%m-%d"
                ),
                "INVOICE_DATE": Helpers.get_timestamp(fmt="%Y-%m-%d"),
                "INVOICE_NUMBER": "AEPL100000000",
                "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": "2",
            }
        ]

    def post_tml_request_log(self):
        payload = self._build_ticket_payload()
        response = self._ticket_request(
            "post",
            GENERATE_TML_TICKET,
            json=payload,
            headers={
                "token": self.get_token(),
                "Content-Type": "application/json",
            },
            timeout=25,
        )

        ticket_data = response.get("data", [])
        if isinstance(ticket_data, list):
            ticket_data = ticket_data[0] if ticket_data else {}
        if not isinstance(ticket_data, dict):
            ticket_data = {}

        ticket_number = (
            ticket_data.get("TICKET_NO")
            or ticket_data.get("ticketNo")
            or response.get("TICKET_NO", "")
        )
        vin = ticket_data.get("VIN_NO") or payload[0]["VIN_NO"]
        uin = ticket_data.get("UIN_NO") or payload[0]["UIN_NO"]
        iccid = ticket_data.get("ICCID") or payload[0]["ICCID"]
        return payload, vin, uin, iccid, ticket_number, ticket_data

    def get_status_update_logs(self, vin_no=None):
        endpoint = GET_STATUS_UPDATE_LOGS
        if vin_no:
            endpoint += f"?vinNo={vin_no}"
        return self._ticket_request(
            "get",
            endpoint,
            headers={"token": self.get_token()},
            timeout=25,
        )

    def get_dash_counts(self, params=None):
        params = params or DEFAULT_DASHBOARD_FILTERS
        return self._ticket_request(
            "get",
            f"{GET_DASHBOARD_COUNTS}?{params}",
            headers={"token": self.get_token()},
            timeout=25,
        )
