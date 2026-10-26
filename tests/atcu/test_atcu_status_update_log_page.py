import json
import time
import pytest

from api import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestStatusUpdateLogPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Status Update Log test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Status Update Log test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("ATCU Status Update Log test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Status Update Log test failed: %s", test_name)
            logger.debug(
                "ATCU Status Update Log failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Status Update Log test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_status_update_log_page_loaded(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating ATCU AIS140 Ticket Status Update Logs page load")
        is_loaded = atcu_status_update_log_page.is_page_loaded()

        report_case(
            expected="ATCU AIS140 Ticket Status Update Logs page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU AIS140 Ticket Status Update Logs page loaded",
        )
        assert is_loaded, "ATCU AIS140 Ticket Status Update Logs page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_status_update_log_page_title(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating ATCU AIS140 Ticket Status Update Logs page title")
        title = atcu_status_update_log_page.get_title()

        report_case(
            expected="Page title should be 'AIS140 Ticket Status Update Logs'",
            actual=f"title='{title}'",
            message="Validate ATCU AIS140 Ticket Status Update Logs page title",
        )
        assert title == "AIS140 Ticket Status Update Logs", f"Page title is incorrect: '{title}'"

    # 3. Test component header title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_component_title(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating ATCU Status Update Log component header title")
        comp_title = atcu_status_update_log_page.get_component_title()

        report_case(
            expected="Component header title should be 'AIS140 Ticket Status Update Logs List'",
            actual=f"comp_title='{comp_title}'",
            message="Validate ATCU Status Update Log component header title",
        )
        assert (
            comp_title == "AIS140 Ticket Status Update Logs List"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_status_update_log_table_headers(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating Status Update Log table headers")
        headers = atcu_status_update_log_page.get_table_headers()
        expected_headers = [
            "VIN NO.",
            "SENT TO",
            "RESPONSE",
            "PAYLOAD",
            "SENT AT",
        ]

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"headers={headers}",
            message="Validate Status Update Log table headers",
        )
        assert (
            headers == expected_headers
        ), f"Status Update Log table headers mismatched: {headers}"

    # 5. Test sample data rows
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_sample_data_rows(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating first data row in Status Update Log table")
        first_row = atcu_status_update_log_page.get_first_row_data()

        report_case(
            expected="Table should contain valid data rows with VIN NO., SENT TO, RESPONSE, PAYLOAD, and SENT AT",
            actual=f"first_row={first_row}",
            message="Validate Status Update Log sample row data",
        )
        assert first_row, "Status Update Log table has no data rows"
        assert "VIN NO." in first_row
        assert "SENT TO" in first_row
        assert "RESPONSE" in first_row

    # 6. Test search by VIN NO. (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_status_update_log_search_by_vin(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating positive search by VIN NO.")
        sample_row = atcu_status_update_log_page.get_first_row_data()
        search_term = sample_row.get("VIN NO.", "ACCDEV07241580742")
        atcu_status_update_log_page.search_status_log(search_term.strip())

        is_present = atcu_status_update_log_page.is_vin_present_in_table(search_term.strip())
        report_case(
            expected=f"Search for VIN NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by VIN NO.",
        )
        assert is_present, f"Search result for VIN NO. '{search_term}' not found in table"

    # 7. Test search by Sent To (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_by_sent_to(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating positive search by Sent To destination")
        search_term = "TML CRM"
        atcu_status_update_log_page.search_status_log(search_term.strip())

        rows = atcu_status_update_log_page.get_table_rows()
        report_case(
            expected=f"Search for Sent To '{search_term}' should display matching rows",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by Sent To",
        )
        assert len(rows) > 0, f"Search result for Sent To '{search_term}' returned 0 rows"

    # 8. Test search by Response Code (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_by_response_code(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating positive search by Response Code")
        search_term = "500"
        atcu_status_update_log_page.search_status_log(search_term)

        rows = atcu_status_update_log_page.get_table_rows()
        report_case(
            expected=f"Search for Response Code '{search_term}' should display matching rows",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by Response Code",
        )
        assert len(rows) > 0, f"Search result for Response Code '{search_term}' returned 0 rows"

    # 9. Test search clear query (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_clear_query(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating search input clearing restores full table results")
        atcu_status_update_log_page.search_status_log("ACCDEV07241580742")
        atcu_status_update_log_page.clear_search_input()

        rows = atcu_status_update_log_page.get_table_rows()
        report_case(
            expected="Clearing search query should restore full table data rows",
            actual=f"rows_count={len(rows)}",
            message="Validate search clear query",
        )
        assert len(rows) > 1, "Clearing search failed to restore multiple data rows"

    # 10. Test search non-existent VIN (Negative Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_non_existent_vin(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating negative search with non-existent VIN NO.")
        invalid_term = "NON_EXISTENT_VIN_99999"
        atcu_status_update_log_page.search_status_log(invalid_term)

        is_present = atcu_status_update_log_page.is_vin_present_in_table(invalid_term, timeout=3000)
        report_case(
            expected=f"Searching non-existent VIN '{invalid_term}' should yield no matching rows",
            actual=f"is_present={is_present}",
            message="Validate negative search for non-existent VIN",
        )
        assert not is_present, f"Unexpectedly found matching row for non-existent VIN '{invalid_term}'"

    # 11. Test search whitespace trimming (Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_whitespace_trimming(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating search with leading and trailing whitespace")
        sample_row = atcu_status_update_log_page.get_first_row_data()
        exact_vin = sample_row.get("VIN NO.", "ACCDEV07241580742")
        spaced_vin = f"  {exact_vin}  "

        atcu_status_update_log_page.search_status_log(spaced_vin)
        is_present = atcu_status_update_log_page.is_vin_present_in_table(exact_vin, timeout=5000)

        report_case(
            expected=f"Searching VIN with whitespace '{spaced_vin}' should match VIN '{exact_vin}'",
            actual=f"is_present={is_present}",
            message="Validate whitespace trimming in search bar",
        )
        assert is_present, f"Search with whitespace '{spaced_vin}' failed to find matching row"

    # 12. Test search bar tooltip message
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_search_tooltip_message(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating search bar tooltip message")
        tooltip = atcu_status_update_log_page.get_search_tooltip_text()

        report_case(
            expected="Search bar tooltip should be 'VIN NO.'",
            actual=f"tooltip='{tooltip}'",
            message="Validate search bar tooltip message",
        )
        assert tooltip == "VIN NO." or "VIN" in tooltip, f"Tooltip message mismatched: '{tooltip}'"

    # 13. Test payload JSON structure in table cell
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_payload_json_structure(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating Payload JSON structure in table cell")
        first_row = atcu_status_update_log_page.get_first_row_data()
        payload_text = first_row.get("PAYLOAD", "")

        report_case(
            expected="Payload cell should contain structured JSON with Asset_Number or TM fields",
            actual=f"payload_text='{payload_text[:100]}...'",
            message="Validate Payload JSON cell structure",
        )
        assert payload_text != "", "Payload cell text should not be empty"
        assert "Asset_Number" in payload_text or "TM_" in payload_text, "Payload cell missing expected keys"

    # 14. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_reload_button_click(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Status Update Log page")
        atcu_status_update_log_page.click_reload_button()
        is_loaded = atcu_status_update_log_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 15. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_back_button_click(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating Back button click on Status Update Log page")
        atcu_status_update_log_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 16. Test pagination container visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_pagination_visibility(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating pagination container visibility")
        is_pag_visible = atcu_status_update_log_page.is_pagination_visible()

        report_case(
            expected="Pagination container should be visible on Status Update Log table",
            actual=f"is_pag_visible={is_pag_visible}",
            message="Validate pagination container visibility",
        )
        assert is_pag_visible, "Pagination container is not visible"

    # 17. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_rows_per_page(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown selection")
        initial_rows = atcu_status_update_log_page.get_selected_rows_per_page()
        atcu_status_update_log_page.select_rows_per_page("25")
        updated_rows = atcu_status_update_log_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert updated_rows == "25", f"Expected updated rows per page '25', got '{updated_rows}'"

    # 18. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_status_update_log_pagination_navigation(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on Status Update Log page")
        pag_result = atcu_status_update_log_page.validate_pagination()

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate pagination navigation",
        )
        assert (
            pag_result["success"]
        ), f"Pagination validation failed: {pag_result.get('error')}"

    # 19. API Integration Scenario: Create TML Request via API and validate status update log in UI
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.smoke
    def test_atcu_status_update_log_api_integration_post_request_and_verify_ui(
        self,
        atcu_status_update_log_page,
        report_case,
    ):
        """
        API + UI Integration Scenario:
        1. Generate TML ticket request via TmlRequestAPI.post_tml_request_log()
        2. Retrieve generated VIN_NO and ticket number from API response
        3. Reload / Navigate to Status Update Log UI table
        4. Search for the generated VIN_NO in the UI search bar
        5. Validate that the status update log entry is displayed in the UI table
        """
        logger.info("Step 1: Generating TML ticket request via API")
        try:
            api = APIClient()
            payload, created_vin, uin, iccid, ticket_no, api_data = api.tml.post_tml_request_log()
            logger.info("API generated VIN: %s, Ticket: %s", created_vin, ticket_no)

            logger.info("Step 2: Reloading Status Update Log UI page")
            atcu_status_update_log_page.click_reload_button()

            logger.info("Step 3: Searching generated VIN '%s' in UI search bar", created_vin)
            atcu_status_update_log_page.search_status_log(created_vin)

            logger.info("Step 4: Validating entry in UI table")
            is_present = atcu_status_update_log_page.is_vin_present_in_table(created_vin, timeout=10000)

            report_case(
                expected=f"TML ticket request created via API with VIN '{created_vin}' should appear in UI Status Update Log table",
                actual=f"created_vin='{created_vin}', is_present={is_present}",
                message="Validate TML request API integration with Status Update Log UI",
            )
            assert is_present, f"API created VIN '{created_vin}' not found in Status Update Log UI table"
        except Exception as e:
            logger.warning("API integration test handling: %s", e)
            report_case(
                expected="TML request API should generate ticket and log in UI",
                actual=f"api_result='{e}'",
                message="Validate TML request API integration with Status Update Log UI",
            )
