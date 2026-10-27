import pytest
from pages.common_utils import TableSection
from pages.common_utils import SearchHelper
from pages.common_utils import PaginationHelper
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
# @pytest.mark.repeat(3) used to run on repeat all tests i.e. 9 tests * 3 = 27 total tests,, another use --count=3 in terminal while running.
class TestAeplResponseLogPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting AEPL Response Log test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "AEPL Response Log test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("AEPL Response Log test passed: %s", test_name)
        elif report.failed:
            logger.error("AEPL Response Log test failed: %s", test_name)
            logger.debug(
                "AEPL Response Log failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("AEPL Response Log test skipped: %s", test_name)

    @staticmethod
    def _get_first_row_payload(aepl_response_log_page):
        aepl_response_log_page.page.reload(wait_until="networkidle")
        row = TableSection(aepl_response_log_page.page).get_row_data(0)
        payload = aepl_response_log_page._normalize_payload_value(row["PAYLOAD"])

        assert isinstance(payload, dict), "UI payload is not a dictionary"
        for column, key in (
            ("VIN NO.", "VIN_NO"),
            ("ICCID NO.", "ICCID"),
            ("UIN NO.", "UIN_NO"),
        ):
            assert key in payload, f"UI payload is missing {key}"
            assert str(row[column]).strip() == str(payload[key]).strip(), (
                f"{column} does not match {key} in the UI payload"
            )

        return row, payload

    # test that the page is loaded successfully
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_loaded(
        self,
        aepl_response_log_page,
        report_case,
    ):
        logger.info("Validating AEPL Response Log page load")

        is_loaded = aepl_response_log_page.is_page_loaded()

        report_case(
            expected="AEPL Response Log page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="AEPL Response Log page load validation",
        )

        assert is_loaded, "AEPL Response Log page is not loaded"

    # test that the page title is correct when page is loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_title(
        self,
        aepl_response_log_page,
        report_case,
    ):
        logger.info("Validating AEPL Response Log page title")

        title = aepl_response_log_page.get_title()

        report_case(
            expected="AEPL Response Log page title should be correct",
            actual=f"page_title={title}",
            message="AEPL Response Log page title validation",
        )

        assert (
            title == "AIS140 Ticket AEPL Response Logs"
        ), f"AEPL Response Log page title is incorrect: {title}"

    # Do first request with valid payload
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.api
    @pytest.mark.smoke
    def test_aepl_response_log_page_api_payload_integrity(
        self, aepl_response_log_page, tml_api, report_case
    ):
        logger.info("Validating AEPL Response Log request-response pairs")
        payload, VIN, UIN, ICCID, ticket_number, data = (
            aepl_response_log_page.get_valid_request_response_by_api(tml_api)
        )
        report_case(
            expected="Valid request-response pairs should be fetched from AEPL Response Log API",
            actual=f"payload={payload}, VIN={VIN}, UIN={UIN}, ICCID={ICCID}, ticket_number={ticket_number}, data={data}",
            message="AEPL Response Log request-response validation",
        )

        assert (
            payload is not None
        ), "Failed to fetch valid request-response pairs from AEPL Response Log API"
        assert VIN is not None, "VIN is None in the valid request-response pairs"
        assert UIN is not None, "UIN is None in the valid request-response pairs"
        assert ICCID is not None, "ICCID is None in the valid request-response pairs"
        assert (
            ticket_number is not None
        ), "Ticket number is None in the valid request-response pairs"
        assert isinstance(
            payload, list
        ), "Payload is not a dictionary in the valid request-response pairs"
        assert isinstance(
            ticket_number, str
        ), "Ticket number is not a string in the valid request-response pairs"
        assert isinstance(
            data, dict
        ), "Data is not a list in the valid request-response pairs"

    # Validate the identifiers in the response-log row against its payload.
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_valid_payload_ui_validation(
        self, aepl_response_log_page, report_case
    ):
        logger.info("Validating AEPL Response Log payload against its table row")
        row, payload_data = self._get_first_row_payload(aepl_response_log_page)
        logger.info("UI response log row fetched: %s", row)
        report_case(
            expected="VIN, ICCID and UIN in the UI row should match its payload",
            actual=f"UI row={row}, payload={payload_data}",
            message="AEPL Response Log UI payload validation",
        )
        logger.info("AEPL Response Log payload validation completed successfully")

    # Test the column data:
    # sent to - ['Generate Tickets API', 'Institutional Sale']
    # response - 200
    # VIN, UIN, ICCID validation
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_table_data_payload_validation(
        self, aepl_response_log_page, report_case
    ):
        logger.info("Validating AEPL Response Log table data against its payload")
        ui_data, payload_data = self._get_first_row_payload(aepl_response_log_page)
        report_case(
            expected="AEPL Response Log table identifiers should match the row payload",
            actual=f"UI row={ui_data}, payload={payload_data}",
            message="AEPL Response Log UI table data validation",
        )
        logger.info("AEPL Response Log table data validation completed successfully")

    # Validate the Search functionality on the response log page with the valid payload and validate the response on the ui with the response from the api
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.critical
    def test_aepl_response_log_page_search_functionality(
        self, aepl_response_log_page, report_case
    ):
        # take help of helper search from pages/common_utils/search.py
        logger.info("Validating search functionality on the AEPL Response Log page")

        search_helper = SearchHelper(aepl_response_log_page.page)

        result = search_helper.run_search("ACCDEV20222589462")

        if result["success"]:
            logger.info(
                "Search executed successfully with results found: %d",
                result["results_found"],
            )
            report_case(
                expected="Search should return results",
                actual=f"Results found: {result['results_found']}",
                message="AEPL Response Log search functionality validation",
            )

        if not result["success"]:
            logger.error("Search failed with error: %s", result["error"])
            report_case(
                expected="Search should execute successfully",
                actual=f"Error: {result['error']}",
                message="AEPL Response Log search functionality validation",
            )
            assert False, f"Search failed with error: {result['error']}"

        if result["error"]:
            logger.error("Search encountered an error: %s", result["error"])
            report_case(
                expected="Search should not encounter errors",
                actual=f"Error: {result['error']}",
                message="AEPL Response Log search functionality validation",
            )
            assert False, f"Search encountered an error: {result['error']}"

    # Validate the table headers on response log page
    @pytest.mark.regression
    @pytest.mark.ui
    def test_aepl_response_log_page_table_headers_validation(
        self, aepl_response_log_page, report_case
    ):
        logger.info("Validating table headers on the AEPL Response Log page")

        expected_headers = [
            "VIN NO.",
            "ICCID NO.",
            "UIN NO.",
            "SENT TO",
            "RESPONSE",
            "PAYLOAD",
            "SENT AT",
        ]

        actual_headers = TableSection(aepl_response_log_page.page).get_headers()

        logger.info("Actual table headers fetched: %s", actual_headers)

        report_case(
            expected="Table headers should match expected headers",
            actual=f"Actual headers: {actual_headers}",
            message="AEPL Response Log table headers validation",
        )

        assert (
            actual_headers == expected_headers
        ), f"Table headers mismatch. Expected: {expected_headers}, Actual: {actual_headers}"

    # Validate the first row's payload and response metadata.
    @pytest.mark.regression
    @pytest.mark.ui
    def test_aepl_response_log_page_first_row_payload_validation(
        self, aepl_response_log_page, report_case
    ):
        logger.info(
            "Validating first-row identifiers against its AEPL Response Log payload"
        )
        row, payload_data = self._get_first_row_payload(aepl_response_log_page)
        logger.info("UI response log row fetched: %s", row)
        report_case(
            expected="First-row identifiers should match the payload in that row",
            actual=f"UI row={row}, payload={payload_data}",
            message="AEPL Response Log UI payload validation",
        )

        assert (
            row["SENT TO"] == "Generate Tickets API"
            or row["SENT TO"] == "Institutional Sale"
        ), "Unexpected SENT TO value in the UI response log row"

        assert (
            row["SENT AT"] is not None and len(row["SENT AT"]) > 0
        ), "SENT AT value is empty or None in the UI payload"

        logger.info(
            "AEPL Response Log first row table data validation completed successfully"
        )

    # Validate the pagination on the response log page with the valid payload and validate the response on the ui with the response from the api
    @pytest.mark.regression
    @pytest.mark.ui
    def test_aepl_response_log_page_pagination_functionality(
        self, aepl_response_log_page, report_case
    ):
        logger.info("Validating pagination functionality on the AEPL Response Log page")

        table_section = TableSection(aepl_response_log_page.page)

        # Get the initial row count
        initial_row_count = table_section.get_row_count()
        logger.info("Initial row count: %d", initial_row_count)

        pagination = PaginationHelper(aepl_response_log_page.page)

        result = pagination.verify()

        if result["success"]:
            logger.info(
                "Pagination executed successfully with pages visited: %s",
                result["pages_visited"],
            )
            report_case(
                expected="Pagination should execute successfully",
                actual=f"Pages visited: {result['pages_visited']}",
                message="AEPL Response Log pagination functionality validation",
            )

        if result["error"]:
            logger.error("Pagination encountered an error: %s", result["error"])
            report_case(
                expected="Pagination should not encounter errors",
                actual=f"Error: {result['error']}",
                message="AEPL Response Log pagination functionality validation",
            )
            assert False, f"Pagination encountered an error: {result['error']}"

        if result["total_pages"] > 0:
            logger.info(
                "Pagination count on response page should be greater than 0, total pages %s",
                result["total_pages"],
            )
            report_case(
                expected="Pagination count on response page should be greater than 0",
                actual=f"Total pages: {result['total_pages']}",
                message="AEPL Response Log pagination functionality validation",
            )
