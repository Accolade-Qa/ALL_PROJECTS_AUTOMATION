import ast
import json
import time

from pages.atcu.atcu_tml_request_log_page import AtcuTmlRequestLogPage
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from pages.common_utils.pagination import PaginationHelper
from utils.logger import get_logger
from pages.common_base_page import BasePage

logger = get_logger(__name__)


class AtcuAeplResponseLogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.request_log = AtcuTmlRequestLogPage(page)
        logger.debug("Initialized AtcuAeplResponseLogPage")

    @staticmethod
    def _normalize_payload_value(payload):
        if isinstance(payload, str):
            value = payload.strip()
            if not value:
                return payload

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    return payload

        return payload

    def get_title(self):
        title = self.page.locator(".page-title").text_content()
        logger.debug("AEPL Response Log page title retrieved: %s", title)
        return title

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.debug("AEPL Response Log page loaded successfully.")
            return True
        except Exception as e:
            logger.error("AEPL Response Log page failed to load: %s", e)
            return False

    def search_logs(self, item_to_search):
        logger.info("Searching AEPL Response Log for '%s'", item_to_search)

        search = SearchHelper(self.page)
        result = search.run_search(item_to_search)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            result["success"],
            result["results_found"],
        )

        return result

    def get_table_headers(self):
        logger.info("Fetching AEPL Response Log table headers")

        table = TableSection(self.page)
        headers = table.get_headers()

        logger.debug("Retrieved table headers: %s", headers)

        return headers

    def validate_pagination(self):
        logger.info("Validating pagination on AEPL Response Log page")

        pagination = PaginationHelper(self.page)
        result = pagination.verify()

        logger.debug(
            "Pagination validation completed. Success=%s, Pages Visited=%s, Total Pages=%s",
            result["success"],
            result["pages_visited"],
            result["total_pages"],
        )

        return result

    def get_valid_request_response_by_api(self, api):
        logger.info("Fetching valid request-response pairs from AEPL Response Log API")

        payload, VIN, UIN, ICCID, ticket_number, data = (
            self.request_log.get_tml_request_payload_by_api(api)
        )

        return payload, VIN, UIN, ICCID, ticket_number, data

    def get_table_data_first_row(self):
        logger.info("Fetching first row data from AEPL Response Log table")

        table = TableSection(self.page)
        first_row_data = table.get_row_data(0)
        if isinstance(first_row_data, dict):
            first_row_data["PAYLOAD"] = self._normalize_payload_value(
                first_row_data.get("PAYLOAD")
            )
        logger.debug("Retrieved first row data: %s", first_row_data)
        return first_row_data
