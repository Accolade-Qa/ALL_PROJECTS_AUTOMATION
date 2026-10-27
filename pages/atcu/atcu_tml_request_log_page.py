from utils.helpers import Helpers
from pages.common_base_page import BasePage
from api.tml_request_api import GENERATE_TML_TICKET
from pages.common_utils import SearchHelper, TableSection, PaginationHelper
import asyncio
import threading
import aiohttp


from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuTmlRequestLogPage(BasePage):
    """
    this page should mainly for validating the ticket request,
    and validate the data exactly on the ui.
    """

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized AtcuTmlRequestLogPage")

    def get_title(self):
        return super().get_title()

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.debug("TML Request Log page loaded successfully.")
            return True
        except Exception as e:
            logger.error("TML Request Log page failed to load: %s", e)
            return False

    def search_logs(self, item_to_search):
        logger.info("Searching TML Request Log for '%s'", item_to_search)

        search = SearchHelper(self.page)
        result = search.run_search(item_to_search)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            result["success"],
            result["results_found"],
        )

        return result

    def get_table_headers(self):
        logger.info("Fetching TML Request Log table headers")

        table = TableSection(self.page)
        headers = table.get_headers()

        logger.debug("Retrieved table headers: %s", headers)

        return headers

    def validate_pagination(self):
        logger.info("Validating pagination on TML Request Log page")

        pagination = PaginationHelper(self.page)
        result = pagination.verify()

        logger.debug(
            "Pagination validation completed. Success=%s, Pages Visited=%s, Total Pages=%s",
            result["success"],
            result["pages_visited"],
            result["total_pages"],
        )

        return result

    def get_tml_request_payload_by_ui(self) -> list[str]:
        """
        Returns all payload values from the TML Request Log table.
        """

        logger.info("Fetching payload values from the TML Request Log table")

        table = TableSection(self.page)
        table_data = table.get_table_data()

        payloads = [row.get("PAYLOAD", "").strip() for row in table_data]

        logger.debug("Retrieved %s payload(s): %s", len(payloads), payloads)

        return payloads

    def get_tml_request_payload_by_api(self, tml_api):
        """
        Returns the payload values from the TML Request Log API.
        """

        logger.info("Fetching payload values from the TML Request Log API")

        payload, VIN, UIN, ICCID, ticket_number, data = (
            tml_api.post_tml_request_log()
        )

        logger.debug(
            "Retrieved payload from API: %s, VIN: %s, UIN: %s, ICCID: %s, Ticket Number: %s, Data: %s",
            payload,
            VIN,
            UIN,
            ICCID,
            ticket_number,
            data,
        )

        return payload, VIN, UIN, ICCID, ticket_number, data

    def validate_fota_batch_addition(self):

        vehicle_owner_states = {
            "Haryana",
            "Assam",
            "Andhra Pradesh",
            "Jammu & Kashmir",
            "Punjab",
            "Nagaland",
            "Gujarat",
            "Daman and Diu",
            "Dadra and Nagar Haveli",
            "Jharkhand",
        }

        try:
            payload = self.get_tml_request_payload_by_ui()[0]

            state_name = payload.get("VEHICLE_OWNER_STATE", "").strip()
            ticket_number = payload.get("TICKET_NUMBER", "").strip()

            logger.info("Vehicle owner state : %s", state_name)

            if state_name not in vehicle_owner_states:
                logger.info(
                    "Vehicle owner state '%s' is not eligible for Auto FOTA.",
                    state_name,
                )

                return {
                    "success": True,
                    "conditions_met": False,
                    "batch_added": False,
                    "error": None,
                }

            batch_added = self.check_fota_batch_on_ui(
                ticket_number=ticket_number,
                state_name=state_name,
            )

            return {
                "success": batch_added,
                "conditions_met": True,
                "batch_added": batch_added,
                "error": None if batch_added else "FOTA batch not found.",
            }

        except Exception as e:
            logger.exception("Failed to validate FOTA batch")

            return {
                "success": False,
                "conditions_met": False,
                "batch_added": False,
                "error": str(e),
            }

    def check_fota_batch_on_ui(
        self,
        project_config,
        ticket_number: str,
        state_name: str,
    ) -> bool:
        """
        Verifies that the Auto FOTA batch has been created for the
        given ticket number and vehicle owner state.

        Returns:
            bool: True if batch name and description match, otherwise False.
        """

        logger.info(
            "Validating Auto FOTA batch for Ticket=%s, State=%s",
            ticket_number,
            state_name,
        )

        try:
            # Navigate to FOTA Batch page
            self.page.goto(project_config["fota_batch_url"])

            self.page.wait_for_load_state("networkidle")

            # Refresh so that newly created batch is visible
            self.page.reload()

            self.page.wait_for_load_state("networkidle")

            table = TableSection(self.page)
            table_data = table.get_table_data()

            if not table_data:
                logger.error("No FOTA batches found on UI.")
                return False

            # Latest batch should be at the top
            latest_batch = table_data[0]

            actual_batch_name = latest_batch.get("BATCH NAME", "").strip()
            actual_description = latest_batch.get("DESCRIPTION", "").strip()

            expected_batch_name = f"Auto FOTA for {ticket_number}"

            expected_description = (
                f"Auto FOTA for {ticket_number} for state {state_name}"
            )

            logger.info("Expected Batch Name : %s", expected_batch_name)
            logger.info("Actual Batch Name   : %s", actual_batch_name)

            logger.info("Expected Description : %s", expected_description)
            logger.info("Actual Description   : %s", actual_description)

            if actual_batch_name != expected_batch_name:
                logger.error(
                    "Batch name mismatch. Expected '%s', got '%s'",
                    expected_batch_name,
                    actual_batch_name,
                )
                return False

            if actual_description != expected_description:
                logger.error(
                    "Batch description mismatch. Expected '%s', got '%s'",
                    expected_description,
                    actual_description,
                )
                return False

            logger.info("Auto FOTA batch validation completed successfully.")

            return True

        except Exception as e:
            logger.exception("Failed while validating Auto FOTA batch.")
            logger.error(str(e))
            return False

    def create_multiple_tickets_concurrently(self, tml_api):
        """Generate multiple TML tickets simultaneously and validate uniqueness."""

        payloads = []

        # Number of concurrent requests
        request_count = 10

        for _ in range(request_count):
            state_name = Helpers.generate_random_state_name()
            state_code = Helpers.generate_random_state_abbreviation()

            payloads.append(
                {
                    "VIN_NO": f"MAT00007241580{Helpers.generate_random_number(3)}",
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
                    "ACCOLADE_POSTING_DATE_TIME": Helpers.get_timestamp(fmt="%Y-%m-%d"),
                    "INVOICE_DATE": Helpers.get_timestamp(fmt="%Y-%m-%d"),
                    "INVOICE_NUMBER": "AEPL100000000",
                    "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": "2",
                }
            )

        token = tml_api.get_token()
        endpoint = tml_api.build_ticket_url(GENERATE_TML_TICKET)

        headers = {
            "Content-Type": "application/json",
            "token": token,
        }

        async def send_request(session, payload):
            vin = payload["VIN_NO"]

            try:
                async with session.post(
                    endpoint,
                    json=[payload],
                    headers=headers,
                ) as response:

                    http_status = response.status

                    try:
                        response_json = await response.json(content_type=None)
                    except Exception:
                        return {
                            "vin": vin,
                            "http_status": http_status,
                            "ticket_number": None,
                            "record_status": None,
                            "validation_errors": ["Non JSON Response"],
                            "response": {},
                        }

                    ticket_number = None
                    record_status = None
                    validation_errors = []

                    data = response_json.get("data", [])

                    if isinstance(data, list) and data:
                        record = data[0]
                        ticket_number = record.get("TICKET_NO")
                        record_status = record.get("status")
                        validation_errors = record.get("VALIDATION_ERROR", [])

                    return {
                        "vin": vin,
                        "http_status": http_status,
                        "ticket_number": ticket_number,
                        "record_status": record_status,
                        "validation_errors": validation_errors,
                        "response": response_json,
                    }

            except Exception as exc:
                return {
                    "vin": vin,
                    "http_status": None,
                    "ticket_number": None,
                    "record_status": None,
                    "validation_errors": [str(exc)],
                    "response": {},
                }

        async def execute():
            connector = aiohttp.TCPConnector(limit=10, ssl=False)
            timeout = aiohttp.ClientTimeout(total=60)

            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
            ) as session:

                tasks = []

                for payload in payloads:
                    tasks.append(asyncio.create_task(send_request(session, payload)))
                    await asyncio.sleep(0.001)

                return await asyncio.gather(*tasks)

        result_holder = {}

        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result_holder["value"] = loop.run_until_complete(execute())
            finally:
                loop.close()
                asyncio.set_event_loop(None)

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            results = asyncio.run(execute())
        else:
            thread = threading.Thread(target=run_in_thread)
            thread.start()
            thread.join()
            results = result_holder.get("value")

        tickets = []
        failed_requests = []

        for result in results:
            if result["ticket_number"]:
                tickets.append(result["ticket_number"])
            else:
                failed_requests.append(result)

        duplicates = list({ticket for ticket in tickets if tickets.count(ticket) > 1})

        logger.info(
            "Concurrent Ticket Generation Summary | "
            "Total=%s Generated=%s Failed=%s Duplicates=%s",
            len(results),
            len(tickets),
            len(failed_requests),
            len(duplicates),
        )

        return {
            "results": results,
            "tickets": tickets,
            "failed_requests": failed_requests,
            "duplicates": duplicates,
        }

    def get_table_data(self):
        """
        Returns all rows of the TML Request Log table as a list of dictionaries.
        Each dictionary represents a row with column headers as keys.
        """

        logger.info("Fetching all rows from the TML Request Log table")

        table = TableSection(self.page)
        table_data = table.get_table_data()

        logger.debug("Retrieved %s row(s) from the table", len(table_data))

        first_row = table_data[0] if table_data else {}
        sent_by_in_key = first_row.get("SENT_BY", "").strip() if first_row else None
        logger.info("First row SENT_BY value: %s", sent_by_in_key)

        institutional_sale_from_payload = first_row.get("PAYLOAD", "")
        if isinstance(institutional_sale_from_payload, str):
            try:
                import json

                payload_dict = json.loads(institutional_sale_from_payload)
                institutional_sale_from_payload = payload_dict.get(
                    "InstitutionalSales", ""
                ).strip()
            except json.JSONDecodeError:
                logger.error(
                    "Failed to decode PAYLOAD JSON for the first row: %s",
                    institutional_sale_from_payload,
                )
                institutional_sale_from_payload = None

        if not sent_by_in_key:
            if institutional_sale_from_payload:
                sent_by_in_key = (
                    "Institutional Sales"
                    if institutional_sale_from_payload.upper() == "Y"
                    else "Generate Tickets API"
                )
            else:
                sent_by_in_key = "Generate Tickets API"

        logger.info("First row INSTITUTIONAL_SALE_FROM value: %s", institutional_sale_from_payload)

        return sent_by_in_key, institutional_sale_from_payload