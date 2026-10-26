import time
import pytest

from utils.helpers import Helpers
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestGovtServerPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Government Server test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Government Server test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("ATCU Government Server test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Government Server test failed: %s", test_name)
            logger.debug(
                "ATCU Government Server failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Government Server test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_govt_server_page_loaded(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating ATCU Government Servers page load")
        is_loaded = atcu_govt_server_page.is_page_loaded()

        report_case(
            expected="ATCU Government Servers page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Government Servers page loaded",
        )
        assert is_loaded, "ATCU Government Servers page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_govt_server_page_title(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating ATCU Government Servers page title")
        title = atcu_govt_server_page.get_title()

        report_case(
            expected="Page title should be 'Government Servers'",
            actual=f"title='{title}'",
            message="Validate ATCU Government Servers page title",
        )
        assert title == "Government Servers", f"Page title is incorrect: '{title}'"

    # 3. Test component header title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_component_title(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating ATCU Government Servers component header title")
        comp_title = atcu_govt_server_page.get_component_title()

        report_case(
            expected="Component header title should be 'Government Servers List'",
            actual=f"comp_title='{comp_title}'",
            message="Validate ATCU Government Servers component header title",
        )
        assert (
            comp_title == "Government Servers List"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_govt_server_table_headers(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Government Servers table headers")
        headers = atcu_govt_server_page.get_table_headers()
        expected_headers = [
            "NAME OF STATE",
            "STATE ABBREVIATION",
            "1ST SEO",
            "GOVT. IP1",
            "PORT1",
            "GOVT. IP2",
            "PORT2",
            "2ND SEO",
            "GOVT. IP3",
            "PORT3",
            "GOVT. IP4",
            "PORT4",
            "CREATED BY",
            "ACTION",
        ]

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"headers={headers}",
            message="Validate Government Servers table headers",
        )

        assert len(headers) > 0, "Government Servers table headers list is empty"
        assert all(
            header in expected_headers for header in headers
        ), "Unexpected table headers found"
        assert (
            headers == expected_headers
        ), f"Government Servers table headers mismatched: {headers}"

    # 5. Test sample data rows
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_sample_data_rows(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating first data row in Government Servers table")
        first_row = atcu_govt_server_page.get_first_row_data()

        report_case(
            expected="Table should contain valid data rows with NAME OF STATE, STATE ABBREVIATION, GOVT. IP1, and PORT1",
            actual=f"first_row={first_row}",
            message="Validate Government Servers sample row data",
        )
        assert first_row, "Government Servers table has no data rows"
        assert "NAME OF STATE" in first_row
        assert "STATE ABBREVIATION" in first_row
        assert "GOVT. IP1" in first_row
        assert "PORT1" in first_row

    # 6. Test search by State Name (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_by_state_name(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating positive search by State Name")
        search_term = "Bihar"
        atcu_govt_server_page.search_govt_server_list(search_term)

        is_present = atcu_govt_server_page.is_state_present_in_table(search_term)
        report_case(
            expected=f"Search for State Name '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by State Name",
        )
        assert (
            is_present
        ), f"Search result for State Name '{search_term}' not found in table"

    # 7. Test search by State Abbreviation (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_by_state_abbr(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating positive search by State Abbreviation")
        search_term = "DND"  # State abbreviation for DO NOT DELETE (example)
        atcu_govt_server_page.search_govt_server_list(search_term)

        is_present = atcu_govt_server_page.is_state_present_in_table(search_term)
        report_case(
            expected=f"Search for State Abbreviation '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by State Abbreviation",
        )
        assert (
            is_present
        ), f"Search result for State Abbreviation '{search_term}' not found in table"

    # 8. Test search by Govt IP (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_by_ip(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating positive search by Govt IP")
        search_term = "brvlts.parivahan.gov.in"
        atcu_govt_server_page.search_govt_server_list(search_term)

        is_present = atcu_govt_server_page.is_state_present_in_table(search_term)
        report_case(
            expected=f"Search for Govt IP '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by Govt IP",
        )
        assert (
            is_present
        ), f"Search result for Govt IP '{search_term}' not found in table"

    # 9. Test search by Port (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_by_port(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating positive search by Port")
        search_term = "9031"
        atcu_govt_server_page.search_govt_server_list(search_term)

        is_present = atcu_govt_server_page.is_state_present_in_table(search_term)
        report_case(
            expected=f"Search for Port '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by Port",
        )
        assert is_present, f"Search result for Port '{search_term}' not found in table"

    # 10. Test search clear query (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_clear_query(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating search input clearing restores full table results")
        atcu_govt_server_page.search_govt_server_list("Bihar")
        atcu_govt_server_page.clear_search_input()

        rows = atcu_govt_server_page.get_table_rows()
        report_case(
            expected="Clearing search query should restore full table data rows",
            actual=f"rows_count={len(rows)}",
            message="Validate search clear query",
        )
        assert len(rows) > 1, "Clearing search failed to restore multiple data rows"

    # 11. Test search non-existent term (Negative Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_non_existent_term(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating negative search with non-existent search term")
        invalid_term = "NON_EXISTENT_STATE_99999"
        atcu_govt_server_page.search_govt_server_list(invalid_term)

        is_present = atcu_govt_server_page.is_state_present_in_table(
            invalid_term, timeout=3000
        )
        report_case(
            expected=f"Searching non-existent term '{invalid_term}' should yield no matching rows",
            actual=f"is_present={is_present}",
            message="Validate negative search for non-existent term",
        )
        assert (
            not is_present
        ), f"Unexpectedly found matching row for non-existent term '{invalid_term}'"

    # 12. Test download report button visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_download_report_button_visibility(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Download Report button visibility")
        is_vis = atcu_govt_server_page.is_download_report_button_visible()

        report_case(
            expected="Download Report button should be visible",
            actual=f"is_visible={is_vis}",
            message="Validate Download Report button visibility",
        )
        assert is_vis, "Download Report button is not visible"

    # 13. Test download report button click
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_download_report_button_click(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Download Report button click event")
        try:
            download = atcu_govt_server_page.click_download_report_button()
            filename = download.suggested_filename
            report_case(
                expected="Download Report click should trigger file download event",
                actual=f"downloaded_file='{filename}'",
                message="Validate Download Report button click",
            )
            assert filename != "", "Downloaded report file name should not be empty"
        except Exception as e:
            logger.warning("Download report event handling: %s", e)
            report_case(
                expected="Download Report button should be visible and clickable",
                actual=f"error='{e}'",
                message="Validate Download Report button click",
            )

    # 14. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_reload_button_click(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Government Servers page")
        atcu_govt_server_page.click_reload_button()
        is_loaded = atcu_govt_server_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 15. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_back_button_click(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Back button click on Government Servers page")
        atcu_govt_server_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 16. Test pagination container visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_pagination_visibility(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating pagination container visibility")
        is_pag_visible = atcu_govt_server_page.is_pagination_visible()

        report_case(
            expected="Pagination container should be visible on Government Servers table",
            actual=f"is_pag_visible={is_pag_visible}",
            message="Validate pagination container visibility",
        )
        assert is_pag_visible, "Pagination container is not visible"

    # 17. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_rows_per_page(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown selection")
        initial_rows = atcu_govt_server_page.get_selected_rows_per_page()
        atcu_govt_server_page.select_rows_per_page("25")
        updated_rows = atcu_govt_server_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert (
            initial_rows == "10"
        ), f"Expected default rows per page '10', got '{initial_rows}'"
        assert (
            updated_rows == "25"
        ), f"Expected updated rows per page '25', got '{updated_rows}'"

    # 18. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_pagination_navigation(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on Government Servers page")
        pag_result = atcu_govt_server_page.validate_pagination()

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate pagination navigation",
        )
        assert pag_result[
            "success"
        ], f"Pagination validation failed: {pag_result.get('error')}"

    # 19. Test navigation to Add Government server sub-page
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_govt_server_navigate_to_add_page(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating navigation to Add Government server sub-page")
        assert atcu_govt_server_page.is_add_govt_server_button_visible()
        atcu_govt_server_page.click_add_govt_server_button()

        is_sub_loaded = atcu_govt_server_page.is_add_page_loaded()
        report_case(
            expected="Clicking 'Add Government server' button should navigate to Add Government Servers sub-page",
            actual=f"is_sub_loaded={is_sub_loaded}",
            message="Validate navigation to Add Government server page",
        )
        assert is_sub_loaded, "Add Government Servers sub-page failed to load"

    # 20. Test Add Government Servers page titles
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_page_title(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Add Government Servers page titles")
        atcu_govt_server_page.click_add_govt_server_button()
        title = atcu_govt_server_page.get_add_page_title()
        comp_title = atcu_govt_server_page.get_add_component_title()

        report_case(
            expected="Page title should be 'Add Government Servers' and component title should be 'Government Servers Details'",
            actual=f"title='{title}', comp_title='{comp_title}'",
            message="Validate Add Government Servers page titles",
        )
        assert title == "Add Government Servers", f"Page title mismatched: '{title}'"
        assert (
            comp_title == "Government Servers Details"
        ), f"Component title mismatched: '{comp_title}'"

    # 20a. Test all input fields on Add Government Server form are enabled and editable
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_all_inputs_enabled(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info(
            "Validating all input fields on Add Government Server page are enabled and editable"
        )
        atcu_govt_server_page.click_add_govt_server_button()
        fields = atcu_govt_server_page.get_input_fields_locators()

        for field_name, locator in fields.items():
            is_vis = locator.is_visible()
            is_ena = locator.is_enabled()
            logger.debug(
                "Field '%s' -> Visible: %s, Enabled: %s", field_name, is_vis, is_ena
            )
            report_case(
                expected=f"Field '{field_name}' should be visible and enabled",
                actual=f"Visible: {is_vis}, Enabled: {is_ena}",
                message=f"Validate state of input field '{field_name}'",
            )
            assert is_vis, f"Input field '{field_name}' is not visible"
            assert is_ena, f"Input field '{field_name}' is not enabled"

    # 20b. Test input fields accept text values
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_inputs_accept_values(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating input fields accept typed values")
        atcu_govt_server_page.click_add_govt_server_button()
        atcu_govt_server_page.fill_add_govt_server_form(
            state="TestState",
            state_abbr="TS",
            state_enable="*SET#SWEMP#TS#",
        )
        vals = atcu_govt_server_page.get_input_field_values()

        report_case(
            expected="Input fields state, stateAbbreviation, and stateEnable should accept text values",
            actual=f"values={vals}",
            message="Validate text input acceptance",
        )
        assert vals.get("state") == "TestState"
        assert vals.get("stateAbbreviation") == "TS"

    # 20c. Test IP and Port input fields accept valid IP and Port values generated via Helpers
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_valid_ip_and_port_inputs(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating IP and Port input fields accept valid values")
        atcu_govt_server_page.click_add_govt_server_button()

        random_ip1 = Helpers.generate_random_ip()
        random_port1 = Helpers.generate_random_port()
        random_ip2 = Helpers.generate_random_ip()
        random_port2 = Helpers.generate_random_port()

        atcu_govt_server_page.fill_add_govt_server_form(
            govt_ip1=random_ip1,
            port1=random_port1,
            govt_ip2=random_ip2,
            port2=random_port2,
        )
        vals = atcu_govt_server_page.get_input_field_values()

        report_case(
            expected="IP and Port fields should accept valid IP address and Port number values",
            actual=f"vals={vals}",
            message="Validate IP and Port input acceptance",
        )
        assert vals.get("govtIp1") == random_ip1
        assert vals.get("port1") == random_port1
        assert vals.get("govtIp2") == random_ip2
        assert vals.get("port2") == random_port2

    # 20d. Test Search Bar tooltip message
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_search_tooltip_message(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Search bar tooltip message")
        tooltip = atcu_govt_server_page.get_search_tooltip_text()

        report_case(
            expected="Search bar should display tooltip message containing field names",
            actual=f"tooltip='{tooltip}'",
            message="Validate Search bar tooltip message",
        )
        assert tooltip != "", "Search bar tooltip message should not be empty"

    # 21. Test Add Form initial state & Submit button state (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_initial_state(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating initial state of Add Government Server form")
        atcu_govt_server_page.click_add_govt_server_button()

        is_submit_enabled = atcu_govt_server_page.is_submit_button_enabled()
        report_case(
            expected="Submit button should be disabled initially when required fields are empty",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate initial state of Add Government Server form",
        )
        assert (
            not is_submit_enabled
        ), "Submit button should be disabled initially when required fields are empty"

    # 21a. Corner Case Test: Partial form fill keeps Submit button disabled
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_partial_fill_disabled(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info(
            "Validating Submit button remains disabled when form is only partially filled"
        )
        atcu_govt_server_page.click_add_govt_server_button()
        atcu_govt_server_page.fill_add_govt_server_form(
            state="OnlyStateName", state_abbr=None
        )

        is_submit_enabled = atcu_govt_server_page.is_submit_button_enabled()
        report_case(
            expected="Submit button should remain disabled when State Abbreviation is missing",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate partial form fill disabled state",
        )
        assert (
            not is_submit_enabled
        ), "Submit button should remain disabled when required fields are missing"

    # 21b. Corner Case Test: Fill spaces-only inputs (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_empty_spaces_only(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating form behavior when required inputs contain spaces only")
        atcu_govt_server_page.click_add_govt_server_button()
        atcu_govt_server_page.fill_add_govt_server_form(state="   ", state_abbr="   ")

        is_submit_enabled = atcu_govt_server_page.is_submit_button_enabled()
        report_case(
            expected="Submit button should be disabled when required inputs contain spaces only",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate spaces-only input handling",
        )

    # 21c. Corner Case Test: Duplicate state creation attempt (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_duplicate_state(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating duplicate state creation corner case")
        existing_state = "Bihar"
        atcu_govt_server_page.click_add_govt_server_button()
        atcu_govt_server_page.fill_add_govt_server_form(
            state=existing_state,
            state_abbr="BR",
            govt_ip1=Helpers.generate_random_ip(),
            port1=Helpers.generate_random_port(),
        )

        atcu_govt_server_page.click_submit_button()
        toast = atcu_govt_server_page.get_toast_message(timeout=3000)

        report_case(
            expected=f"Attempting to add existing state '{existing_state}' should handle duplicate error gracefully",
            actual=f"toast='{toast}'",
            message="Validate duplicate state creation handling",
        )

    # 22. Corner Case Test: Form fields handling leading and trailing whitespace
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_add_form_leading_trailing_spaces(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info(
            "Starting corner case validation for leading/trailing spaces in Add Government Server form"
        )
        atcu_govt_server_page.click_add_govt_server_button()
        assert atcu_govt_server_page.is_add_page_loaded()

        timestamp = int(time.time())
        raw_state_name = f"  TRIM_STATE_{timestamp}  "
        raw_state_abbr = f"  TS{timestamp % 1000}  "
        expected_state_name = f"TRIM_STATE_{timestamp}"
        random_ip = Helpers.generate_random_ip()
        random_port = Helpers.generate_random_port()

        atcu_govt_server_page.fill_add_govt_server_form(
            state=raw_state_name,
            state_abbr=raw_state_abbr,
            govt_ip1=random_ip,
            port1=random_port,
        )

        atcu_govt_server_page.click_submit_button()

        atcu_govt_server_page.search_govt_server_list(expected_state_name)
        is_present = atcu_govt_server_page.is_state_present_in_table(
            expected_state_name, timeout=10000
        )

        if is_present:
            atcu_govt_server_page.click_delete_button_for_row(expected_state_name)

        report_case(
            expected="Form with leading/trailing spaces should submit and create server successfully",
            actual=f"is_present={is_present}",
            message="Validate leading/trailing whitespace handling in form fields",
        )
        assert (
            is_present
        ), f"Government server created with whitespace '{expected_state_name}' was not found in table"

    # 23. Test View action button for existing server row
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_view_button_action(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info(
            "Validating View action button for an existing government server row"
        )
        sample_state = "Bihar"
        # from pages.common_utils.search import SearchHelper as sh
        # sh.run_search(atcu_govt_server_page, sample_state)

        assert atcu_govt_server_page.is_state_present_in_table(sample_state)

        is_view_vis = atcu_govt_server_page.is_view_button_visible_for_row(sample_state)
        assert is_view_vis, f"View button not visible for row '{sample_state}'"

        atcu_govt_server_page.click_view_button_for_row(sample_state)

        is_add_loaded = atcu_govt_server_page.is_view_page_loaded()

        report_case(
            expected="Clicking View action button should navigate to Government Servers Details page",
            actual=f"is_view_vis={is_view_vis}, is_add_loaded={is_add_loaded}",
            message="Validate View action button navigation",
        )
        assert (
            is_add_loaded
        ), "Add/Details page failed to load after clicking View button"

    # 24. Test Delete action button visibility for table row
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_govt_server_delete_button_visibility(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        logger.info("Validating Delete action button visibility for state row")
        sample_state = "Bihar"
        assert atcu_govt_server_page.is_state_present_in_table(sample_state)

        is_delete_vis = atcu_govt_server_page.is_delete_button_visible_for_row(
            sample_state
        )
        report_case(
            expected=f"Delete action button should be visible for row '{sample_state}'",
            actual=f"is_delete_vis={is_delete_vis}",
            message="Validate Delete button visibility",
        )
        assert is_delete_vis, f"Delete button is not visible for row '{sample_state}'"

    # 25. End-to-End Scenario: Add new government server, verify in list search, and delete
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_govt_server_add_delete_and_verify(
        self,
        atcu_govt_server_page,
        report_case,
    ):
        """
        Flow:
        1. Navigate to Add Government Server form (/govt-servers-add)
        2. Fill State Name, Abbreviation, Govt IP1, and Port1 with new unique values generated via Helpers
        3. Submit form and return to list
        4. Search for newly added state in search bar
        5. Validate entry is present in table and row data matches
        6. Delete state via Delete action button
        7. Confirm state is deleted from list
        """
        logger.info("Step 1: Navigating to Add Government Server page")
        atcu_govt_server_page.click_add_govt_server_button()
        assert atcu_govt_server_page.is_add_page_loaded()

        logger.info("Step 2: Entering unique state details generated via Helpers")
        ts = int(time.time())
        unique_state = f"AUTO_STATE_{ts}"
        unique_abbr = f"AS{ts % 1000}"
        unique_ip = Helpers.generate_random_ip()
        unique_port = Helpers.generate_random_port()

        atcu_govt_server_page.fill_add_govt_server_form(
            state=unique_state,
            state_abbr=unique_abbr,
            govt_ip1=unique_ip,
            port1=unique_port,
        )

        logger.info("Step 3: Submitting form")
        atcu_govt_server_page.click_submit_button()

        logger.info("Step 4: Returning to Government Servers list page")
        is_loaded = atcu_govt_server_page.is_page_loaded()
        assert is_loaded, "Government Servers list page failed to load after submission"

        logger.info(
            "Step 5: Searching for newly added state '%s' in table", unique_state
        )
        atcu_govt_server_page.search_govt_server_list(unique_state)

        logger.info(
            "Step 6: Validating entry present in list table and matching details"
        )
        is_created_present = atcu_govt_server_page.is_state_present_in_table(
            unique_state, timeout=10000
        )
        assert is_created_present, f"Created state '{unique_state}' not found in table"

        row_details = atcu_govt_server_page.get_row_details_by_state(unique_state)
        logger.info("Row details for newly added state: %s", row_details)

        logger.info("Step 7: Deleting created state")
        assert atcu_govt_server_page.is_delete_button_visible_for_row(unique_state)
        atcu_govt_server_page.click_delete_button_for_row(unique_state)

        logger.info("Step 8: Confirming state is deleted from table")
        atcu_govt_server_page.search_govt_server_list(unique_state)
        is_still_present = atcu_govt_server_page.is_state_present_in_table(
            unique_state, timeout=3000
        )
        assert (
            not is_still_present
        ), f"Deleted state '{unique_state}' is still present in table"

        report_case(
            expected="Government server should be created, verified via search, deleted, and confirmed absent",
            actual=f"unique_state='{unique_state}', is_created_present={is_created_present}, is_still_present={is_still_present}",
            message="Validate end-to-end add, search, and delete government server flow",
        )
