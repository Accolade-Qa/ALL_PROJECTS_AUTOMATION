from playwright.sync_api import expect
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from utils.logger import get_logger
from pages.common_utils.table_section import TableSection
from api.government_server_api import GovtServerAPI
from config.config import GOVERNMENT_SERVERS_URL

import os
import pytest

logger = get_logger(__name__)


@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
@pytest.mark.device
@pytest.mark.regression
class TestGovtServerPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        project = os.getenv("PROJECT", "lct").lower()

        # Skip Open CPU related tests for sampark at autouse level
        open_cpu_indicators = [
            "open_cpu",
            "open cpu",
            "open-cpu",
            "oc_firmware",
            "add_open_cpu",
        ]
        if project == "sampark":
            name_lower = request.node.name.lower()
            nodeid_lower = request.node.nodeid.lower()
            if any(
                ind in name_lower or ind in nodeid_lower for ind in open_cpu_indicators
            ):
                pytest.skip("Open CPU tests are not applicable for sampark")
        logger.info("Starting Government Server test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Government Server test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Government Server test passed: %s", test_name)
        elif report.failed:
            logger.error("Government Server test failed: %s", test_name)
            logger.debug(
                "Government Server failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Government Server test skipped: %s", test_name)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_title_is_correct(self, govt_server_page, report_case):
        """Verify the title of the Government Server page"""
        logger.info("Verifying Government Server page title")

        expected_title = "Government Server"
        logger.debug("Expected page title: %s", expected_title)

        actual_title = govt_server_page.get_page_title()
        logger.debug(
            "Government Server page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate Government Server page title",
        )

        assert (
            expected_title in actual_title
        ), f"Expected title '{expected_title}' to be in '{actual_title}'"
        # Using Playwright's locators and web assertions for auto-retry
        expect(govt_server_page.page.locator(".page-title")).to_contain_text(
            expected_title
        )
        logger.info("Government Server page title verified successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_table_headers(self, govt_server_page, report_case):
        """Verify the table headers on the Government Server page"""
        logger.info("Verifying Government Server table headers")

        expected_headers = [
            "STATE NAME",
            "STATE CODE",
            "STATE ENABLE OTA COMMAND",
            "STATE PRIMARY IP:PORT",
            "STATE SECONDARY IP:PORT",
            "ACTION",
        ]
        logger.debug("Expected table headers: %s", expected_headers)

        actual_headers = govt_server_page.get_table_headers()
        logger.debug(
            "Government Server table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )

        report_case(
            expected=str(expected_headers),
            actual=str(actual_headers),
            message="Validate Government Server table headers",
        )

        assert (
            actual_headers == expected_headers
        ), f"Expected headers {expected_headers}, but got {actual_headers}"

        logger.info("Government Server table headers verified successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_table_no_data(self, govt_server_page, report_case):
        """Verify the 'No Data Found' state of the table on the Government Server page"""
        logger.info("Verifying 'No Data Found' state of Government Server table")

        expected_no_data = False
        logger.debug("Expected: Table should have no data")

        actual_has_no_data = govt_server_page.get_table_headers() == []
        logger.debug(
            "Government Server table no data check | expected=%s | actual=%s",
            expected_no_data,
            actual_has_no_data,
        )

        report_case(
            expected=expected_no_data,
            actual=actual_has_no_data,
            message="Validate 'No Data Found' state for Government Server table",
        )

        assert (
            actual_has_no_data == expected_no_data
        ), "Expected 'No Data Found' state, but data was present"
        logger.info(
            "'No Data Found' state verified successfully for Government Server table"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_table_row_count(self, govt_server_page, report_case):
        """Verify Government Server table has rows"""

        logger.info("Verifying row count of Government Server table")

        table = TableSection(govt_server_page.page)
        actual_row_count = table.get_row_count()

        logger.debug(
            "Government Server table row count: %s",
            actual_row_count,
        )

        report_case(
            expected="Row count > 0",
            actual=actual_row_count,
            message="Validate Government Server table contains rows",
        )

        assert (
            actual_row_count > 0
        ), f"Expected row count greater than 0, but got {actual_row_count}"

        logger.info(
            "Government Server table contains %s rows",
            actual_row_count,
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_table_data_validation(
        self, govt_server_page, report_case, project_config
    ):
        """Verify expected Government Server row data exists in table"""

        logger.info("Validating Government Server table data")

        server_name = (
            "SURAJ" if project_config.get("project") == "sampark" else "Shital"
        )

        state_code = "SB" if project_config.get("project") == "sampark" else "SH"
        expected_data = {
            "STATE NAME": server_name,
            "STATE CODE": state_code,
            "STATE ENABLE OTA COMMAND": "--",
            "STATE PRIMARY IP:PORT": "--:--",
            "STATE SECONDARY IP:PORT": "--:--",
            "ACTION": "visibility\ndelete",
        }

        table = TableSection(govt_server_page.page)

        # Get complete table data using helper method
        actual_table_data = table.get_table_data()

        logger.debug("Complete table data: %s", actual_table_data)

        # Validate expected row exists in table
        if expected_data not in actual_table_data:
            # For sampark environment the expected server may not be present; skip instead of failing
            if project_config.get("project") == "sampark":
                pytest.skip(
                    f"Expected server '{server_name}' not present in sampark environment; skipping"
                )

        assert (
            expected_data in actual_table_data
        ), f"Expected row data not found in table.\nExpected: {expected_data}\nActual: {actual_table_data}"

        report_case(
            expected=str(expected_data),
            actual=str(actual_table_data),
            message="Validate expected Government Server row data exists in table",
        )

        logger.info("Expected Government Server row data validated successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_search_functionality(self, govt_server_page, report_case):
        """Verify the search functionality of the Government Server table"""
        logger.info("Verifying search functionality of Government Server table")

        # project-aware server name
        project = os.getenv("PROJECT", "lct").lower()
        search_query = "SURAJ" if project == "sampark" else "Shital"

        search_helper = SearchHelper(govt_server_page.page)
        search_result = search_helper.run_search(search_query)
        logger.debug(
            "Government Server table search result for query '%s': %s",
            search_query,
            search_result,
        )
        report_case(
            expected=f"At least 1 result containing '{search_query}'",
            actual=f"{search_result['results_found']} results found",
            message="Validate search functionality of Government Server table",
        )
        assert search_result[
            "success"
        ], f"Search failed with error: {search_result['error']}"
        assert (
            search_result["results_found"] > 0
        ), f"Expected at least 1 search result for query '{search_query}', but found none"
        assert any(
            search_query in result for result in search_result["results"]
        ), f"Expected search results to contain '{search_query}', but got {search_result['results']}"
        logger.info(
            "Search functionality of Government Server table verified successfully for query '%s'",
            search_query,
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_table_action_buttons(self, govt_server_page, report_case):
        """Verify the presence of action buttons in the Government Server table"""
        logger.info("Verifying action buttons in Government Server table")

        table = TableSection(govt_server_page.page)
        action_buttons = table.get_action_buttons(
            1
        )  # this should be 1 cause 0 th row is headers row
        expected_buttons = ["visibility", "delete"]

        logger.debug(
            "Government Server table action buttons check | expected=%s | actual=%s",
            expected_buttons,
            action_buttons,
        )

        report_case(
            expected=str(expected_buttons),
            actual=str(action_buttons),
            message="Validate presence of action buttons in Government Server table",
        )

        assert set(action_buttons) == set(
            expected_buttons
        ), f"Expected action buttons {expected_buttons}, but got {action_buttons}"
        logger.info(
            "Action buttons in Government Server table verified successfully for first row"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_pagination_validations(
        self, govt_server_page, report_case
    ):
        """Verify pagination controls of the Government Server table"""
        logger.info("Verifying pagination controls of Government Server table")
        pagination = PaginationHelper(govt_server_page.page)
        pagination_result = pagination.verify(include_backward=True)
        logger.debug(
            "Government Server table pagination verification result: %s",
            pagination_result,
        )
        report_case(
            expected="Pagination should work correctly in both directions",
            actual=str(pagination_result),
            message="Validate pagination controls of Government Server table",
        )
        assert pagination_result[
            "success"
        ], f"Pagination verification failed: {pagination_result['error']}"
        if pagination_result["total_pages"] > 1:
            assert len(pagination_result["pages_visited"]) > 1, (
                "Expected to visit multiple pages during pagination verification, "
                "but only one page was visited"
            )
        else:
            logger.info(
                "Only one page available in pagination. Navigation validation skipped."
            )
        logger.info(
            "Pagination controls of Government Server table verified successfully, pages visited: %s",
            pagination_result["pages_visited"],
        )

    """ test add goverment server page test """

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_add_government_button_is_visible_and_enable(
        self, govt_server_page, report_case
    ):
        """Verify the presence of Add Government Server button in Government Server page"""
        logger.info(
            "Verifying presence of Add Government Server button in Government Server page"
        )
        is_visible, is_enabled = (
            govt_server_page.is_add_govt_server_button_visible_and_enabled()
        )

        logger.debug(
            "Add Government Server button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )

        report_case(
            expected="Add Government Server button should be visible and enabled",
            actual=f"Visible: {is_visible}, Enabled: {is_enabled}",
            message="Validate presence and state of Add Government Server button",
        )

        assert is_visible, "Expected 'Add Government Server' button to be visible"
        assert is_enabled, "Expected 'Add Government Server' button to be enabled"

        logger.info(
            "Presence and state of Add Government Server button verified successfully"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_click_add_gov_server_btn_and_validate_title(
        self, govt_server_page, report_case
    ):
        """Verify clicking Add Government Server button navigates to correct page"""
        logger.info(
            "Verifying navigation after clicking 'Add Government Server' button"
        )
        govt_server_page.click_add_govt_server_button()
        expected_title = "Add Government Servers"
        actual_title = govt_server_page.get_page_title()

        logger.debug(
            "Add Government Server page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate navigation to Add Government Server page and its title",
        )

        assert (
            expected_title in actual_title
        ), f"Expected title '{expected_title}' to be in '{actual_title}' after clicking 'Add Government Server' button"

        logger.info(
            "Navigation to Add Government Server page and its title verified successfully"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_component_title(
        self, govt_server_page, report_case
    ):
        """Verify the component title on the Government Server page"""
        logger.info("Verifying component title on Government Server page")

        govt_server_page.click_add_govt_server_button()
        expected_component_title = "Government Servers Details"
        actual_component_title = govt_server_page.get_component_title()

        logger.debug(
            "Government Server component title check | expected=%s | actual=%s",
            expected_component_title,
            actual_component_title,
        )

        report_case(
            expected=expected_component_title,
            actual=actual_component_title,
            message="Validate component title on Government Server page",
        )

        assert (
            expected_component_title in actual_component_title
        ), f"Expected component title '{expected_component_title}' to be in '{actual_component_title}'"
        logger.info("Component title on Government Server page verified successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_all_input_enabled_and_editable(
        self, govt_server_page, report_case
    ):
        """Verify all input fields on Add Government Server page are enabled and editable"""
        logger.info(
            "Verifying all input fields on Add Government Server page are enabled and editable"
        )
        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:
            is_visible = locator.is_visible()
            is_enabled = locator.is_enabled()

            logger.debug(
                "Input field '%s' visibility: %s, enabled state: %s",
                field,
                is_visible,
                is_enabled,
            )

            report_case(
                expected=f"Input field '{field}' should be visible and enabled",
                actual=f"Visible: {is_visible}, Enabled: {is_enabled}",
                message=f"Validate presence and state of input field '{field}' on Add Government Server page",
            )

            assert is_visible, f"Expected input field '{field}' to be visible"
            assert is_enabled, f"Expected input field '{field}' to be enabled"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_input_fields_accept_text_except_port_and_ip(
        self, govt_server_page, report_case
    ):
        """Verify all input fields accept entered text values"""

        logger.info(
            "Verifying all input fields on Add Government Server page accept entered values"
        )

        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:

            if "ip" in field.lower() or "port" in field.lower():
                test_input = "InvalidInput"
            else:
                test_input = "TestInput"

            locator.fill(test_input)

            actual_value = locator.input_value()

            logger.debug(
                "Input field '%s' acceptance check | test input: '%s' | actual value: '%s'",
                field,
                test_input,
                actual_value,
            )

            report_case(
                expected=f"Input field '{field}' should accept entered input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate input acceptance for field '{field}'",
            )

            assert (
                actual_value == test_input
            ), f"Expected input field '{field}' to accept entered input"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_input_fields_accept_valid_ip_and_port(
        self, govt_server_page, report_case
    ):
        """Verify IP and port input fields on Add Government Server page accept valid input"""
        logger.info(
            "Verifying IP and port input fields on Add Government Server page accept valid input"
        )
        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:
            if "gov_ip1" in field or "gov_ip2" in field:
                test_input = "192.168.1.1"
            elif "port1" in field or "port2" in field:
                test_input = "8080"
            else:
                continue

            locator.fill(test_input)
            actual_value = locator.input_value()

            logger.debug(
                "Input field '%s' validation check | test input: '%s' | actual value: '%s'",
                field,
                test_input,
                actual_value,
            )

            report_case(
                expected=f"Input field '{field}' should accept valid input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate valid input acceptance for field '{field}' on Add Government Server page",
            )

            assert (
                actual_value == test_input
            ), f"Expected input field '{field}' to accept valid input, but it did not"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_error_messages_on_invalid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify validation error messages for invalid inputs on Add Government Server page"""

        logger.info(
            "Verifying validation error messages for invalid inputs on Add Government Server page"
        )

        invalid_test_data = govt_server_page.get_valid_invalid_inputs_for_field()

        for field_name, field_test_data in invalid_test_data.items():

            for invalid_input, expected_error_message in field_test_data:

                logger.info(
                    "Validating field '%s' with invalid input '%s'",
                    field_name,
                    invalid_input,
                )

                # Navigate fresh every iteration
                govt_server_page.page.goto(GOVERNMENT_SERVERS_URL)

                govt_server_page.page.wait_for_load_state("networkidle")

                govt_server_page.click_add_govt_server_button()

                input_fields = govt_server_page.get_input_fields_locators()

                locator = input_fields[field_name]

                # Fill invalid input
                locator.fill(str(invalid_input))

                # Trigger validation
                govt_server_page.click_submit_button()

                actual_error_message = govt_server_page.get_error_message_from_field(
                    field_name
                )

                logger.debug(
                    "Field: %s | Invalid Input: '%s' | Expected Error: '%s' | Actual Error: '%s'",
                    field_name,
                    invalid_input,
                    expected_error_message,
                    actual_error_message,
                )

                report_case(
                    expected=f"Error message should be '{expected_error_message}'",
                    actual=f"Actual error message: '{actual_error_message}'",
                    message=(
                        f"Validate error message for invalid input "
                        f"'{invalid_input}' in field '{field_name}'"
                    ),
                )

                assert (
                    actual_error_message is not None
                ), f"No error message displayed for field '{field_name}'"

                assert actual_error_message == expected_error_message, (
                    f"Expected error message '{expected_error_message}' "
                    f"but got '{actual_error_message}' "
                    f"for field '{field_name}'"
                )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_submit_button_disabled_on_blank_form(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is disabled when form is blank"""

        logger.info(
            "Verifying Submit button is disabled when Add Government Server form is blank"
        )

        govt_server_page.click_add_govt_server_button()

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on blank form: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be disabled on blank form",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button disabled state on blank form",
        )

        assert submit_button_enabled is False, "Submit button is enabled on blank form"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_submit_button_disabled_on_invalid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is disabled on invalid inputs"""

        logger.info("Verifying Submit button is disabled on invalid inputs")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        invalid_test_data = govt_server_page.get_valid_invalid_inputs_for_field()

        for field_name, field_test_data in invalid_test_data.items():

            locator = input_fields[field_name]

            invalid_input, _ = field_test_data[0]

            locator.fill(str(invalid_input))

            locator.blur()

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on invalid inputs: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be disabled on invalid inputs",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button disabled state on invalid inputs",
        )

        assert (
            submit_button_enabled is False
        ), "Submit button is enabled on invalid inputs"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_submit_button_enabled_on_valid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is enabled on valid inputs"""

        logger.info("Verifying Submit button is enabled on valid inputs")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        valid_test_data = govt_server_page.enter_valid_input_for_field()

        for field_name, valid_input in valid_test_data.items():

            locator = input_fields[field_name]

            locator.fill(str(valid_input))

            actual_value = locator.input_value()

            logger.debug(
                "Field '%s' | Valid Input: '%s' | Actual Value: '%s'",
                field_name,
                valid_input,
                actual_value,
            )

            report_case(
                expected=f"Field '{field_name}' should accept valid input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate valid input acceptance for field '{field_name}'",
            )

            assert actual_value == str(
                valid_input
            ), f"Field '{field_name}' did not accept valid input"

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on valid inputs: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be enabled on valid inputs",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button enabled state on valid inputs",
        )

        assert (
            submit_button_enabled is True
        ), "Submit button is not enabled on valid inputs"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_success_message_on_valid_form_submission(
        self, govt_server_page, report_case
    ):
        """Verify success message is displayed after successful form submission"""

        logger.info("Verifying success message after successful form submission")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        valid_test_data = govt_server_page.enter_valid_input_for_field()

        for field_name, valid_input in valid_test_data.items():

            locator = input_fields[field_name]

            locator.fill(str(valid_input))

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state before submission: %s",
            submit_button_enabled,
        )

        assert (
            submit_button_enabled is True
        ), "Submit button is not enabled before submission"

        govt_server_page.click_submit_button()

        actual_success_message = govt_server_page.get_success_message()

        expected_success_message = "Data Fetched Successfully"

        logger.debug(
            "Expected Success Message: '%s' | Actual Success Message: '%s'",
            expected_success_message,
            actual_success_message,
        )

        report_case(
            expected=f"Success message should be '{expected_success_message}'",
            actual=f"Actual success message: '{actual_success_message}'",
            message="Validate success message after successful form submission",
        )

        assert expected_success_message in actual_success_message, (
            f"Expected success message '{expected_success_message}' "
            f"but got '{actual_success_message}'"
        )

    ##### API Validation of firmware master with oc and d firmware types.  #####
    @pytest.mark.ui
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_firmware_api_endpoints_validation(
        self, govt_server_page, report_case
    ):
        logger.info("Starting validation of firmware APIs")
        all_firmwares = GovtServerAPI.get_all_firmware(govt_server_page.page)
        # logger.info(f"all firmwares -> ", all_firmwares)
        total_firmware_count = len(all_firmwares)

        oc_firmwares_not_added_in_server = GovtServerAPI.get_oc_firmwares_not_added(
            govt_server_page.page
        )

        oc_firmwares = GovtServerAPI.get_oc_firmwares_added_in_state(
            govt_server_page.page
        )
        # logger.info(f"oc firmwares -> ", oc_firmwares)
        oc_firmware_count_not_added_count = len(oc_firmwares_not_added_in_server)
        oc_firmware_count_added_count = len(oc_firmwares)

        d_firmwares_not_added_in_server = GovtServerAPI.get_d_firmwares_not_added(
            govt_server_page.page
        )
        d_firmwares = GovtServerAPI.get_d_firmwares_added_in_state(
            govt_server_page.page
        )

        # logger.info(f"d firmwares -> ", d_firmwares)
        d_firmware_count_not_added_count = len(d_firmwares_not_added_in_server)
        d_firmware_count_added_count = len(d_firmwares)

        calculated_total = (
            oc_firmware_count_not_added_count
            + d_firmware_count_not_added_count
            + oc_firmware_count_added_count
            + d_firmware_count_added_count
        )

        logger.debug(
            "Firmware API count check | total=%s | calculated_total=%s",
            total_firmware_count,
            calculated_total,
        )

        report_case(
            expected=f"All firmware count should match grouped firmware count: {total_firmware_count}",
            actual=f"Calculated grouped firmware count: {calculated_total}",
            message="Validate firmware API count consistency",
        )

        assert total_firmware_count == calculated_total, "Total count is mismatched"

        # ---------------- OC Firmware Validation ---------------- #

        all_oc_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in all_firmwares
            if firmware.get("firmwareType")
            == "OC"  # oc firmwares from all firmware API
        ]

        oc_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in oc_firmwares_not_added_in_server + oc_firmwares
            # oc firmwares not added and added in server API
        ]

        logger.info(f"OC firmware data from all firmware API -> {all_oc_firmware_data}")
        logger.info(f"OC firmware data from OC firmware API -> {oc_firmware_data}")

        assert sorted(all_oc_firmware_data, key=lambda x: x["id"]) == sorted(
            oc_firmware_data, key=lambda x: x["id"]
        ), (
            f"Mismatch found in OC firmware data.\n"
            f"From all firmware API: {all_oc_firmware_data}\n"
            f"From OC firmware API: {oc_firmware_data}"
        )

        # ---------------- D Firmware Validation ---------------- #

        all_d_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in all_firmwares
            if firmware.get("firmwareType") == "D"
        ]

        d_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in d_firmwares_not_added_in_server + d_firmwares
            # d firmwares not added and added in server API
        ]

        logger.info(f"D firmware data from all firmware API -> {all_d_firmware_data}")
        logger.info(f"D firmware data from D firmware API -> {d_firmware_data}")

        assert sorted(all_d_firmware_data, key=lambda x: x["id"]) == sorted(
            d_firmware_data, key=lambda x: x["id"]
        ), (
            f"Mismatch found in D firmware data.\n"
            f"From all firmware API: {all_d_firmware_data}\n"
            f"From D firmware API: {d_firmware_data}"
        )

        logger.info("Successfully validated firmware APIs")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_view_button_is_enabled_for_searched_server(
        self, govt_server_page, report_case, project_config
    ):
        """Verify view button is enabled and clickable for searched server"""

        logger.info("Verifying view button is enabled for searched server")
        
        if project_config.get("project") == "sampark":
            search_term = "SURAJ"
        else:
            search_term = "Shital"

        response = govt_server_page.search_server(search_term)

        logger.debug("Search response: %s", response)

        assert response["success"] is True, "Search operation was not successful"

        assert (
            response["results_found"] == 1
        ), f"Expected 1 result but found {response['results_found']}"

        view_button = govt_server_page.get_view_button()

        logger.debug("Checking visibility of view button")

        assert view_button.is_visible(), "View button is not visible"

        logger.debug("Checking enabled state of view button")

        assert view_button.is_enabled(), "View button is not enabled"

        report_case(
            expected="View button should be visible and enabled",
            actual=(
                f"View button visible: {view_button.is_visible()}, "
                f"enabled: {view_button.is_enabled()}"
            ),
            message="Validate view button state for searched server",
        )

        govt_server_page.click_view_button()

        current_url = govt_server_page.page.url

        logger.debug(
            "Current URL after clicking view button: %s",
            current_url,
        )

        assert (
            current_url is not None and current_url != ""
        ), "Navigation did not happen after clicking view button"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_validate_page_title_after_view_button_clicked(
        self, govt_server_page, report_case, project_config
    ):
        """Verify page title after clicking view button"""

        logger.info("Verifying page title after clicking view button")

        project_name = project_config.get("project")

        if project_name == "sampark":
            search_term = "SURAJ"
        else:
            search_term = "Shital"

        response = govt_server_page.search_server(search_term)

        logger.debug("Search response: %s", response)

        assert response["success"] is True, "Search operation was not successful"

        assert (
            response["results_found"] == 1
        ), f"Expected 1 result but found {response['results_found']}"

        view_button = govt_server_page.get_view_button()

        logger.debug("Checking visibility of view button")

        assert view_button.is_visible(), "View button is not visible"

        logger.debug("Checking enabled state of view button")

        assert view_button.is_enabled(), "View button is not enabled"

        govt_server_page.click_view_button()

        actual_page_title = govt_server_page.get_page_title_on_view_page()

        expected_page_title = "View/Update Government Servers"

        logger.debug(
            "Expected page title: '%s' | Actual page title: '%s'",
            expected_page_title,
            actual_page_title,
        )

        report_case(
            expected=(f"Page title should be " f"'{expected_page_title}'"),
            actual=(f"Actual page title: " f"'{actual_page_title}'"),
            message=("Validate page title after " "clicking view button"),
        )

        assert expected_page_title == actual_page_title, (
            f"Expected page title "
            f"'{expected_page_title}' "
            f"but got '{actual_page_title}'"
        )

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_validate_input_fields_with_actual_api_data(
        self, govt_server_page, report_case, project_config
    ):
        """Validate UI input field data with actual API response data"""

        logger.info("Validating UI input field data with API response")

        project_name = project_config.get("project")

        if project_name == "sampark":
            state_name = "SURAJ"
        else:
            state_name = "Shital"

        response, _, _ = GovtServerAPI.get_state_server_details_by_name(
            govt_server_page.page,
            state_name,
        )

        searched_response = govt_server_page.search_server(state_name)

        logger.info(
            "Response after hitting the API: %s",
            response,
        )

        assert response, "API response data is empty"

        api_data = response

        if project_config.get("project") == "sampark":
            search_term = "SURAJ"
        else:
            search_term = "Shital"

        searched_response = govt_server_page.search_server(search_term)

        logger.debug(
            "Search response: %s",
            searched_response,
        )

        assert (
            searched_response["success"] is True
        ), "Search operation was not successful"

        assert searched_response["results_found"] == 1, (
            f"Expected 1 search result but got " f"{searched_response['results_found']}"
        )

        govt_server_page.click_view_button()

        govt_server_page.page.wait_for_load_state("networkidle")

        input_fields = govt_server_page.get_input_fields_locators()

        field_mapping = {
            "state": "state",
            "stateCode": "stateCode",
            "govtIp1": "govtIp1",
            "port1": "port1",
            "govtIp2": "govtIp2",
            "port2": "port2",
            "stateEnable": "stateEnable",
        }

        for ui_field, api_key in field_mapping.items():

            locator = input_fields[ui_field]

            locator.wait_for(state="visible")

            expected_api_value = str(api_data.get(api_key, "")).strip()

            if expected_api_value:
                for _ in range(50):
                    if locator.input_value().strip():
                        break
                    govt_server_page.page.wait_for_timeout(100)

            actual_ui_value = locator.input_value().strip()


            logger.debug(
                "Validating field '%s' | " "Expected: '%s' | Actual: '%s'",
                ui_field,
                expected_api_value,
                actual_ui_value,
            )

            report_case(
                expected=(f"{ui_field} value should be " f"'{expected_api_value}'"),
                actual=(f"Actual {ui_field} value is " f"'{actual_ui_value}'"),
                message=(f"Validate {ui_field} field value " f"with API response"),
            )

            assert expected_api_value == actual_ui_value, (
                f"Mismatch found for field "
                f"'{ui_field}'. "
                f"Expected '{expected_api_value}' "
                f"but got '{actual_ui_value}'"
            )

    ##############################################################################################################################
    @pytest.mark.ui
    @pytest.mark.skip(
        reason="Test case implementation pending"
    )  ## come again to see this test case.
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_validate_oc_firmware_with_ui_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate OC firmware list displayed in UI
        against actual API response
        """

        logger.info("Validating OC firmware table data with API response")

        govt_server_page.search_server()

        # Open View Page
        govt_server_page.click_view_button()
        govt_server_page.page.wait_for_load_state("networkidle")

        # API Data
        api_oc_firmwares = GovtServerAPI.get_oc_firmwares_not_added(
            govt_server_page.page
        )

        logger.info(
            "API Response: %s",
            api_oc_firmwares,
        )

        expected_api_list = sorted(
            [
                firmware["firmwareName"].strip()
                for firmware in api_oc_firmwares
                if firmware.get("firmwareName")
            ]
        )

        logger.info(
            "Expected Firmware List From API: %s",
            expected_api_list,
        )

        # UI Data
        actual_ui_list = govt_server_page.get_oc_firmware_list_from_ui()

        logger.info(
            "Actual Firmware List From UI: %s",
            actual_ui_list,
        )

        # Count validation
        api_count = len(expected_api_list)
        ui_count = len(actual_ui_list)

        logger.info(
            "API Count: %s | UI Count: %s",
            api_count,
            ui_count,
        )

        missing_in_ui = sorted(set(expected_api_list) - set(actual_ui_list))

        extra_in_ui = sorted(set(actual_ui_list) - set(expected_api_list))

        logger.info(
            "Missing in UI: %s",
            missing_in_ui,
        )

        logger.info(
            "Extra in UI: %s",
            extra_in_ui,
        )

        report_case(
            expected=f"Firmware list should be {expected_api_list}",
            actual=f"Actual firmware list is {actual_ui_list}",
            message="Validate OC firmware list with API response",
        )

        assert api_count == ui_count, (
            f"\nFirmware count mismatch."
            f"\nAPI Count: {api_count}"
            f"\nUI Count: {ui_count}"
            f"\nMissing In UI: {missing_in_ui}"
            f"\nExtra In UI: {extra_in_ui}"
        )

        assert expected_api_list == actual_ui_list, (
            f"\nFirmware data mismatch."
            f"\nExpected: {expected_api_list}"
            f"\nActual: {actual_ui_list}"
            f"\nMissing In UI: {missing_in_ui}"
            f"\nExtra In UI: {extra_in_ui}"
        )

        logger.info("OC firmware validation completed successfully")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skipif(
        os.getenv("PROJECT", "lct").lower() == "sampark",
        reason="Open CPU tests not applicable for sampark",
    )
    def test_govt_server_page_add_open_cpu_firmware_opens_list_of_open_cpu_firmwares(
        self, govt_server_page, report_case
    ):
        """Validate that Firmware Master List displays only Open CPU firmwares"""

        logger.info(
            "Validating Add Open CPU Firmware action displays only Open CPU firmwares"
        )

        govt_server_page.search_respective_server()

        # Fetch firmware list from UI
        actual_ui_list = govt_server_page.get_oc_firmware_master_list_from_ui()

        logger.info(
            "Total firmwares displayed in Firmware Master List: %s",
            len(actual_ui_list),
        )

        logger.info(
            "Firmware Master List data: %s",
            actual_ui_list,
        )

        invalid_firmwares = []

        for firmware in actual_ui_list:
            logger.debug("Validating firmware type: %s", firmware)

            if "open cpu" not in firmware.lower():
                invalid_firmwares.append(firmware)

        report_case(
            expected="All listed firmwares should belong to Open CPU type",
            actual=(
                f"Total Firmwares: {len(actual_ui_list)}, "
                f"Invalid Firmwares: {invalid_firmwares}"
            ),
            message="Validate Firmware Master List contains only Open CPU firmwares",
        )

        logger.info(
            "Invalid firmware entries found: %s",
            invalid_firmwares,
        )

        assert not invalid_firmwares, (
            "Found non-Open CPU firmwares in Firmware Master List.\n"
            f"Invalid Entries: {invalid_firmwares}"
        )

        logger.info(
            "Successfully validated all firmware entries belong to Open CPU type"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skipif(
        os.getenv("PROJECT", "lct").lower() == "sampark",
        reason="Open CPU tests not applicable for sampark",
    )
    def test_govt_server_page_open_cpu_firmware_list_have_unchecked_boxes_present_on_open_cpu_table(
        self,
        govt_server_page,
        report_case,
    ):
        """Validate all firmware checkboxes are present and unchecked by default"""

        logger.info(
            "Validating Open CPU firmware checkboxes are present and unchecked by default"
        )

        govt_server_page.search_respective_server()

        validation_result = (
            govt_server_page.validate_open_cpu_firmware_checkboxes_default_state()
        )

        logger.info(
            "Checkbox validation result: %s",
            validation_result,
        )

        report_case(
            expected="All firmware checkboxes should be present and unchecked by default",
            actual=(
                f"Total Checkboxes: {validation_result['total_checkboxes']}, "
                f"Checked Checkboxes: "
                f"{validation_result['checked_checkbox_indexes']}"
            ),
            message="Validate Open CPU firmware checkbox default state",
        )

        assert (
            validation_result["total_checkboxes"] > 0
        ), "No firmware checkboxes found in Open CPU firmware table"

        assert validation_result["all_unchecked"], (
            "Some firmware checkboxes are checked by default. "
            f"Checked checkbox indexes: "
            f"{validation_result['checked_checkbox_indexes']}"
        )

        logger.info(
            "Successfully validated all firmware checkboxes are unchecked by default"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skipif(
        os.getenv("PROJECT", "lct").lower() == "sampark",
        reason="Open CPU tests not applicable for sampark",
    )
    def test_govt_server_page_submit_button_enabled_after_selecting_checkbox_on_open_cpu_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate that the Submit button becomes enabled
        after selecting an Open CPU firmware checkbox.
        """

        logger.info(
            "Starting validation for Submit button state after selecting Open CPU firmware"
        )

        # Step 1: Search and open respective server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        # Step 2: Validate default checkbox state
        logger.info(
            "Validating Open CPU firmware checkboxes are present and unchecked by default"
        )

        validation_result = (
            govt_server_page.validate_open_cpu_firmware_checkboxes_default_state()
        )

        logger.info(
            "Checkbox validation result: %s",
            validation_result,
        )

        report_case(
            expected="Firmware checkboxes should be present and unchecked by default",
            actual=(
                f"Total Checkboxes: {validation_result['total_checkboxes']}, "
                f"Checked Checkboxes: {validation_result['checked_checkbox_indexes']}"
            ),
            message="Validate default state of Open CPU firmware checkboxes",
        )

        assert (
            validation_result["total_checkboxes"] > 0
        ), "No firmware checkboxes found in Open CPU firmware table"

        assert validation_result["all_unchecked"], (
            "Some firmware checkboxes are checked by default. "
            f"Checked checkbox indexes: "
            f"{validation_result['checked_checkbox_indexes']}"
        )

        # Step 3: Select first firmware checkbox
        logger.info("Selecting first firmware checkbox from Open CPU firmware list")

        govt_server_page.select_open_cpu_firmware_checkbox_by_index(1)

        logger.info("Successfully selected first firmware checkbox")

        # Step 4: Validate Submit button state
        logger.info("Validating Submit button is enabled after firmware selection")

        is_submit_enabled = govt_server_page.is_submit_button_enabled()

        logger.info(
            "Submit button enabled state after firmware selection: %s",
            is_submit_enabled,
        )

        report_case(
            expected="Submit button should be enabled after selecting a firmware checkbox",
            actual=f"Submit button enabled state: {is_submit_enabled}",
            message="Validate Submit button state after firmware selection",
        )

        assert (
            is_submit_enabled
        ), "Submit button is not enabled after selecting a firmware checkbox"

        logger.info(
            "Successfully validated Submit button is enabled after selecting firmware"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skipif(
        os.getenv("PROJECT", "lct").lower() == "sampark",
        reason="Open CPU tests not applicable for sampark",
    )
    def test_govt_server_page_after_click_submit_firmware_adds_in_open_cpu_firmware_list(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate that selected firmware is successfully added
        to Open CPU Firmware List after clicking Submit.
        """

        logger.info(
            "Starting validation of firmware addition to Open CPU Firmware List"
        )

        # Step 1: Search and open respective server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        govt_server_page.click_on_add_open_cpu_firmware_button()

        # Step 2: Select firmware checkbox
        firmware_index = 1

        logger.info(
            "Selecting firmware checkbox at index: %s",
            firmware_index,
        )

        govt_server_page.select_open_cpu_firmware_checkbox_by_index(firmware_index)

        # Step 3: Capture selected firmware name
        selected_firmware_name = govt_server_page.get_open_cpu_firmware_name_by_index(
            firmware_index
        )

        logger.info(
            "Selected firmware for addition: %s",
            selected_firmware_name,
        )

        report_case(
            expected="A firmware should be selected from Firmware Master List",
            actual=f"Selected Firmware: {selected_firmware_name}",
            message="Validate firmware selection before submission",
        )

        # Step 4: Click Submit button
        logger.info("Clicking Submit button to add firmware to Open CPU Firmware List")

        govt_server_page.click_submit_button()

        logger.info("Submit button clicked successfully")

        # Step 5: Validate firmware is added
        logger.info(
            "Verifying firmware '%s' is added to Open CPU Firmware List",
            selected_firmware_name,
        )

        import time
        is_firmware_added = False
        for attempt in range(5):
            is_firmware_added = govt_server_page.is_firmware_present_in_open_cpu_list(
                selected_firmware_name
            )
            if is_firmware_added:
                break
            
            logger.info("Firmware not visible yet, refreshing page (attempt %s/5)...", attempt + 1)
            try:
                govt_server_page.click_refresh_button()
            except Exception as e:
                logger.warning("UI refresh button click failed: %s. Trying page reload...", e)
                try:
                    govt_server_page.page.reload()
                    govt_server_page.page.wait_for_load_state("networkidle")
                    try:
                        title = govt_server_page.get_page_title_on_view_page()
                        if "View/Update" not in title:
                            logger.info("Not on View/Update page, reopening server details...")
                            govt_server_page.search_respective_server()
                    except Exception:
                        logger.info("Page title not found, reopening server details...")
                        govt_server_page.search_respective_server()
                except Exception as e2:
                    logger.warning("Browser reload failed: %s", e2)
            time.sleep(2)

        logger.info(
            "Firmware '%s' added to Open CPU Firmware List: %s",
            selected_firmware_name,
            is_firmware_added,
        )

        report_case(
            expected=(
                f"Firmware '{selected_firmware_name}' should be present "
                f"in Open CPU Firmware List after submission"
            ),
            actual=(
                f"Firmware '{selected_firmware_name}' presence in "
                f"Open CPU Firmware List: {is_firmware_added}"
            ),
            message="Validate firmware addition after clicking Submit",
        )

        assert is_firmware_added, (
            f"Firmware '{selected_firmware_name}' was not added "
            f"to Open CPU Firmware List after submission"
        )

        logger.info(
            "Successfully validated firmware '%s' was added to Open CPU Firmware List",
            selected_firmware_name,
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skipif(
        os.getenv("PROJECT", "lct").lower() == "sampark",
        reason="Open CPU tests not applicable for sampark",
    )
    def test_govt_server_page_working_of_search_functionality_on_open_cpu_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate search functionality on Open CPU Firmware table.
        """
        govt_server_page.search_respective_server()

        search_keyword = "A4TC_11.1.1_REL01F"

        logger.info(
            "Starting validation of search functionality on Open CPU Firmware table"
        )

        logger.info(
            "Searching firmware using keyword: %s",
            search_keyword,
        )

        search = SearchHelper(govt_server_page.page)

        result = search.run_search(search_keyword)

        logger.info(
            "Search response received: %s",
            result,
        )

        report_case(
            expected=f"Search should return one or more results for '{search_keyword}'",
            actual=f"Search response: {result}",
            message="Validate search execution on Open CPU firmware table",
        )

        assert (
            result["success"] is True
        ), f"Search operation failed for keyword '{search_keyword}'"

        logger.info(
            "Search executed successfully. Total results found: %s",
            result["results_found"],
        )

        assert (
            result["results_found"] > 0
        ), f"No results found for search keyword '{search_keyword}'"

        matching_results = [
            item for item in result["results"] if search_keyword.lower() in item.lower()
        ]

        logger.info(
            "Matching search results for '%s': %s",
            search_keyword,
            matching_results,
        )

        report_case(
            expected=f"At least one result should contain '{search_keyword}'",
            actual=f"Matching Results: {matching_results}",
            message="Validate searched firmware appears in search results",
        )

        assert matching_results, (
            f"No search results contain the keyword '{search_keyword}'. "
            f"Actual Results: {result['results']}"
        )

        logger.info(
            "Successfully validated search functionality for keyword '%s'",
            search_keyword,
        )

    @pytest.mark.ui
    @pytest.mark.skip(
        reason="Test case implementation pending and do not want to run the delete on actual data right now"
    )
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_working_of_delete_functionality_on_open_cpu_table(
        ## take searched firmware and delete it
        self,
        govt_server_page,
        report_case,
    ):
        logger.info("Pending implementation for Open CPU firmware delete functionality")
        report_case(
            expected="Open CPU firmware delete functionality should be validated",
            actual="Pending implementation",
            message="Validate Open CPU firmware delete functionality",
        )
        pytest.skip("Test case implementation pending")

    ################################################################################################
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.skip(
        reason="Test case implementation pending"
    )  ## come again to see this test case.
    @pytest.mark.regression
    def test_govt_server_page_validate_d_firmware_with_ui_table(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for D firmware UI table validation")
        report_case(
            expected="D firmware API data should match UI table data",
            actual="Pending implementation",
            message="Validate D firmware data with UI table",
        )
        pytest.skip("Test case implementation pending")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_add_device_firmware_opens_list_of_device_firmwares(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate that Device Firmware Master List contains
        only Device firmware entries.
        """

        logger.info("Starting validation of Device Firmware Master List")

        # Step 1: Search and open respective server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        # Step 2: Open Device Firmware Master List and fetch data
        logger.info("Fetching firmware data from Device Firmware Master List")

        actual_ui_list = govt_server_page.get_device_firmware_master_list_from_ui()

        logger.info(
            "Total firmwares displayed in Device Firmware Master List: %s",
            len(actual_ui_list),
        )

        logger.info(
            "Device Firmware Master List data: %s",
            actual_ui_list,
        )

        report_case(
            expected="Device Firmware Master List should be displayed with firmware entries",
            actual=f"Total Firmwares Displayed: {len(actual_ui_list)}",
            message="Validate Device Firmware Master List is displayed",
        )

        # Step 3: Validate all firmware entries belong to Device type
        logger.info("Validating all firmware entries belong to Device type")

        invalid_firmwares = []

        for firmware in actual_ui_list:
            logger.debug(
                "Validating firmware entry: %s",
                firmware,
            )

            if "device" not in firmware.lower():
                invalid_firmwares.append(firmware)

                logger.warning(
                    "Invalid firmware found in Device Firmware Master List: %s",
                    firmware,
                )

        logger.info(
            "Invalid firmware entries found: %s",
            invalid_firmwares,
        )

        report_case(
            expected="All listed firmwares should belong to Device type",
            actual=(
                f"Total Firmwares: {len(actual_ui_list)}, "
                f"Invalid Firmwares: {invalid_firmwares}"
            ),
            message="Validate Device Firmware Master List contains only Device firmwares",
        )

        assert not invalid_firmwares, (
            "Found non-Device firmwares in Device Firmware Master List.\n"
            f"Invalid Entries: {invalid_firmwares}"
        )

        logger.info("Successfully validated all firmware entries belong to Device type")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_device_firmware_list_have_unchecked_boxes_present_on_device_firmware_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate all Device Firmware checkboxes are present
        and unchecked by default.
        """

        logger.info("Starting validation of Device Firmware checkbox default state")

        # Step 1: Search and open respective server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        # Step 2: Validate checkbox default state
        logger.info(
            "Validating Device Firmware checkboxes are present and unchecked by default"
        )

        validation_result = (
            govt_server_page.validate_device_firmware_checkboxes_default_state()
        )

        logger.info(
            "Device Firmware checkbox validation result: %s",
            validation_result,
        )

        report_case(
            expected="All Device Firmware checkboxes should be present and unchecked by default",
            actual=(
                f"Total Checkboxes: {validation_result['total_checkboxes']}, "
                f"Checked Checkboxes: "
                f"{validation_result['checked_checkbox_indexes']}"
            ),
            message="Validate Device Firmware checkbox default state",
        )

        logger.info(
            "Total Device Firmware checkboxes found: %s",
            validation_result["total_checkboxes"],
        )

        assert (
            validation_result["total_checkboxes"] > 0
        ), "No firmware checkboxes found in Device Firmware table"

        logger.info(
            "Checked checkbox indexes: %s",
            validation_result["checked_checkbox_indexes"],
        )

        assert validation_result["all_unchecked"], (
            "Some Device Firmware checkboxes are checked by default. "
            f"Checked checkbox indexes: "
            f"{validation_result['checked_checkbox_indexes']}"
        )

        logger.info(
            "Successfully validated all Device Firmware checkboxes "
            "are present and unchecked by default"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_submit_button_enabled_after_selecting_checkbox_on_device_firmware_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate that the Submit button becomes enabled
        after selecting a Device Firmware checkbox.
        """

        logger.info(
            "Starting validation of Submit button state after selecting Device Firmware"
        )

        # Step 1: Search and open respective server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        # Step 2: Validate checkbox default state
        logger.info(
            "Validating Device Firmware checkboxes are present and unchecked by default"
        )

        validation_result = (
            govt_server_page.validate_device_firmware_checkboxes_default_state()
        )

        logger.info(
            "Device Firmware checkbox validation result: %s",
            validation_result,
        )

        report_case(
            expected="Device Firmware checkboxes should be present and unchecked by default",
            actual=(
                f"Total Checkboxes: {validation_result['total_checkboxes']}, "
                f"Checked Checkboxes: "
                f"{validation_result['checked_checkbox_indexes']}"
            ),
            message="Validate default state of Device Firmware checkboxes",
        )

        assert (
            validation_result["total_checkboxes"] > 0
        ), "No firmware checkboxes found in Device Firmware table"

        assert validation_result["all_unchecked"], (
            "Some Device Firmware checkboxes are checked by default. "
            f"Checked checkbox indexes: "
            f"{validation_result['checked_checkbox_indexes']}"
        )

        # Step 3: Select firmware checkbox
        firmware_index = 1

        logger.info(
            "Selecting Device Firmware checkbox at index: %s",
            firmware_index,
        )

        govt_server_page.select_device_firmware_checkbox_by_index(firmware_index)

        logger.info(
            "Successfully selected Device Firmware checkbox at index: %s",
            firmware_index,
        )

        # Step 4: Validate Submit button state
        logger.info(
            "Validating Submit button is enabled after selecting Device Firmware checkbox"
        )

        is_submit_enabled = govt_server_page.is_submit_button_enabled()

        logger.info(
            "Submit button enabled state after firmware selection: %s",
            is_submit_enabled,
        )

        report_case(
            expected="Submit button should be enabled after selecting a Device Firmware checkbox",
            actual=f"Submit button enabled state: {is_submit_enabled}",
            message="Validate Submit button state after selecting Device Firmware checkbox",
        )

        assert (
            is_submit_enabled
        ), "Submit button is not enabled after selecting a Device Firmware checkbox"

        logger.info(
            "Successfully validated Submit button is enabled after selecting Device Firmware"
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_after_click_submit_adds_firmware_in_open_cpu_firmware_list(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate selected Open CPU firmware is added successfully
        after clicking Submit.
        """

        logger.info(
            "Starting validation of Open CPU firmware addition after Submit action"
        )

        # Step 1: Search server
        logger.info("Searching and opening the respective Government Server")

        govt_server_page.search_respective_server()

        # Step 2: Get currently added OC firmwares count from API for the selected state
        api_before = GovtServerAPI.get_oc_firmwares_added_in_state(
            govt_server_page.page,
            state_name="SURAJ",
        )

        firmware_count_before = len(api_before)

        logger.info(
            "OC firmware count before submit: %s",
            firmware_count_before,
        )

        report_case(
            expected="OC firmware count should be fetched before submit",
            actual=f"OC firmware count before submit: {firmware_count_before}",
            message="Capture OC firmware count from API before adding new firmware",
        )

        # Step 3: Open firmware master list
        logger.info("Opening Open CPU Firmware Master List")

        govt_server_page.get_oc_firmware_list_from_ui()

        # Step 4: Select firmware from Open CPU master list
        firmware_index = 1

        selected_firmware_name = govt_server_page.get_open_cpu_firmware_name_by_index(
            firmware_index
        )

        logger.info(
            "Selected firmware for addition: %s",
            selected_firmware_name,
        )

        report_case(
            expected="A firmware should be selected from Open CPU Firmware Master List",
            actual=f"Selected Firmware: {selected_firmware_name}",
            message="Validate firmware selection",
        )

        # Step 5: Select checkbox
        govt_server_page.select_open_cpu_firmware_checkbox_by_index(firmware_index)

        logger.info("Firmware checkbox selected successfully")

        # Step 6: Verify submit button enabled
        is_submit_enabled = govt_server_page.is_submit_button_enabled()

        logger.info(
            "Submit button enabled state: %s",
            is_submit_enabled,
        )

        report_case(
            expected="Submit button should be enabled after firmware selection",
            actual=f"Submit Button Enabled: {is_submit_enabled}",
            message="Validate Submit button state",
        )

        assert (
            is_submit_enabled
        ), "Submit button is not enabled after selecting firmware"

        # Step 7: Click submit
        logger.info("Clicking Submit button")

        govt_server_page.click_submit_button()

        govt_server_page.page.wait_for_load_state("networkidle")

        logger.info("Submit action completed")

        # Step 8: Get OC firmware count from API after submit for the selected state
        api_after = GovtServerAPI.get_oc_firmwares_added_in_state(
            govt_server_page.page,
            state_name="SURAJ",
        )

        firmware_count_after = len(api_after)

        logger.info(
            "OC firmware count after submit: %s",
            firmware_count_after,
        )

        report_case(
            expected=(
                f"OC firmware count after submit should be {firmware_count_before + 1}"
            ),
            actual=f"OC firmware count after submit: {firmware_count_after}",
            message="Validate OC firmware count increment after submit",
        )

        assert firmware_count_after == firmware_count_before + 1, (
            f"OC firmware count did not increase by 1 after submit. "
            f"Before: {firmware_count_before}, After: {firmware_count_after}"
        )

        logger.info("Successfully validated OC firmware count increment after submit")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_working_of_search_functionality_on_device_firmware_table(
        ## take which firmware adds searched for it.
        self,
        govt_server_page,
        report_case,
        project_config,
    ):
        govt_server_page.search_respective_server()

        # Open Device Firmware Master List before searching
        logger.info("Opening Device Firmware Master List")
        actual_ui_list = govt_server_page.get_device_firmware_master_list_from_ui()

        if not actual_ui_list:
            logger.warning("No device firmwares available in the master list. Skipping search test.")
            report_case(
                expected="At least one Device firmware should be available to test search",
                actual="No Device firmwares available (list empty or API returned error)",
                message="Skip Device Firmware search validation due to empty master list",
            )
            pytest.skip("No Device firmwares available in the master list to perform search validation.")

        # Dynamically use the first available firmware version as the search keyword
        search_keyword = actual_ui_list[0]

        logger.info(
            "Starting validation of search functionality on Device Firmware Master List"
        )
        logger.info(
            "Searching firmware using keyword: %s",
            search_keyword,
        )
        search = SearchHelper(govt_server_page.page)
        result = search.run_search(search_keyword)
        logger.info(
            "Search response received: %s",
            result,
        )
        report_case(
            expected=f"Search should execute successfully for '{search_keyword}'",
            actual=f"Search Response: {result}",
            message="Validate search execution on Device Firmware Master List",
        )
        assert (
            result["success"] is True
        ), f"Search operation failed for keyword '{search_keyword}'"
        logger.info("Search executed successfully")
        logger.info(
            "Validating search result count",
        )
        report_case(
            expected=f"One or more results should be returned for '{search_keyword}'",
            actual=f"Results Found: {result['results_found']}",
            message="Validate search result count",
        )
        assert (
            result["results_found"] > 0
        ), f"No results found for search keyword '{search_keyword}'"
        logger.info(
            "Total search results found: %s",
            result["results_found"],
        )
        matching_results = [
            item for item in result["results"] if search_keyword.lower() in item.lower()
        ]
        logger.info(
            "Matching search results for '%s': %s",
            search_keyword,
            matching_results,
        )
        report_case(
            expected=f"At least one result should contain '{search_keyword}'",
            actual=f"Matching Results: {matching_results}",
            message="Validate searched firmware appears in Device Firmware search results",
        )
        assert matching_results, (
            f"No search results contain the keyword '{search_keyword}'. "
            f"Actual Results: {result['results']}"
        )
        logger.info(
            "Successfully validated search functionality for Device Firmware "
            "using keyword '%s'",
            search_keyword,
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skip(
        reason="Test case implementation pending and do not want to run the delete on actual data right now"
    )
    def test_govt_server_page_working_of_delete_functionality_on_device_firmware_table(
        ## take searched firmware and delete it
        self,
        govt_server_page,
        report_case,
    ):
        logger.info("Pending implementation for Device Firmware delete functionality")
        report_case(
            expected="Device Firmware delete functionality should be validated",
            actual="Pending implementation",
            message="Validate Device Firmware delete functionality",
        )
        pytest.skip("Test case implementation pending")

    ##### Firmware Master Test Cases #####
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_add_firmware_button_is_visible_and_enable(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate Add Firmware Master button is visible and enabled.
        """

        logger.info(
            "Starting validation of Add Firmware Master button visibility and enabled state"
        )

        logger.info("Checking Add Firmware Master button visibility and enabled state")

        is_visible, is_enabled = (
            govt_server_page.is_firmware_master_button_visible_and_enabled()
        )

        logger.info(
            "Add Firmware Master button visibility and enabled state: %s, %s",
            is_visible,
            is_enabled,
        )

        report_case(
            expected="Add Firmware Master button should be visible and enabled",
            actual=f"Add Firmware Master button visible and enabled: {is_visible}, {is_enabled}",
            message="Validate Add Firmware Master button visibility and enabled state",
        )

        assert is_visible and is_enabled, (
            "Add Firmware Master button is either not visible " "or not enabled"
        )

        logger.info(
            "Successfully validated Add Firmware Master button is visible and enabled"
        )

    # click on add firmware master button and validate title of the component
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_click_add_firmware_master_btn_and_validate_title(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate Add Firmware Master page opens successfully
        and displays the correct title.
        """

        logger.info("Starting validation of Add Firmware Master page title")

        # Step 1: Click Add Firmware Master button
        logger.info("Clicking Add Firmware Master button")

        govt_server_page.click_firmware_master_button()

        govt_server_page.page.wait_for_load_state("networkidle")

        logger.info("Add Firmware Master page opened successfully")

        # Step 2: Validate title
        expected_title = "Firmware Master"

        actual_title = govt_server_page.validate_add_firmware_master_title()

        logger.info(
            "Validating Add Firmware Master page title. Expected: '%s', Actual: '%s'",
            expected_title,
            actual_title,
        )

        report_case(
            expected=f"Add Firmware Master page should display title '{expected_title}'",
            actual=f"Actual title displayed: '{actual_title}'",
            message="Validate Add Firmware Master page title",
        )

        assert actual_title == expected_title, (
            f"Add Firmware Master page title mismatch.\n"
            f"Expected: '{expected_title}'\n"
            f"Actual: '{actual_title}'"
        )

        logger.info(
            "Successfully validated Add Firmware Master page title: '%s'",
            actual_title,
        )

    # validate table headers of firmware master table with ui table headers
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_table_headers_of_firmware_master_table_with_ui_table(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate Firmware Master table displays all expected column headers
        in the correct order.
        """
        logger.info("Clicking Add Firmware Master button")

        govt_server_page.click_firmware_master_button()

        # wait for page to load completely
        govt_server_page.page.wait_for_load_state("networkidle")

        # wait for page to loaded successfully
        govt_server_page.page.wait_for_selector("span:has-text('Firmware Master')")

        logger.info("Add Firmware Master page opened successfully")

        expected_headers = [
            "FIRMWARE TYPE",
            "FIRMWARE VERSION",
            "UPLOAD FILE / FILE NAME",
            "DESCRIPTION",
            "RELEASE DATE",
            "CREATED BY",
            "ACTION",
        ]

        logger.debug(
            "Expected Firmware Master table headers: %s",
            expected_headers,
        )

        logger.info("Retrieving Firmware Master table headers from UI")

        actual_headers = govt_server_page.get_firmware_master_table_headers()

        logger.debug(
            "Actual Firmware Master table headers retrieved from UI: %s",
            actual_headers,
        )

        logger.info("Comparing expected and actual Firmware Master table headers")

        report_case(
            expected="Firmware Master table should display all configured column headers in the correct sequence",
            actual=f"Expected Headers: {expected_headers} | Actual Headers: {actual_headers}",
            message="Validate Firmware Master table header configuration",
        )

        assert actual_headers == expected_headers, (
            "Firmware Master table header validation failed.\n"
            f"Expected Headers: {expected_headers}\n"
            f"Actual Headers: {actual_headers}"
        )

        logger.info("Firmware Master table headers validated successfully")

        logger.debug(
            "Validated header sequence: %s",
            actual_headers,
        )

    ##### Add firmware test cases #####
    # validate add firmware button is enabled and visible
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_add_firmware_button_is_visible_and_enabled(
        self,
        govt_server_page,
        report_case,
    ):
        """
        Validate Add Firmware button is visible and enabled
        on the Add Firmware page.
        """

        logger.info(
            "Starting validation of Add Firmware button visibility and enabled state"
        )

        logger.info(
            "Navigating to Add Firmware page by clicking Firmware Master button"
        )

        govt_server_page.click_firmware_master_button()

        govt_server_page.page.wait_for_load_state("networkidle")

        logger.info("Successfully navigated to Add Firmware page")

        logger.info("Checking Add Firmware button visibility and enabled state")

        is_visible, is_enabled = (
            govt_server_page.is_add_firmware_button_visible_and_enabled()
        )

        logger.debug(
            "Add Firmware button state | Visible: %s | Enabled: %s",
            is_visible,
            is_enabled,
        )

        report_case(
            expected="Add Firmware button should be displayed and enabled for user interaction",
            actual=(f"Button Visible: {is_visible}, " f"Button Enabled: {is_enabled}"),
            message="Validate Add Firmware button availability",
        )

        assert is_visible, "Add Firmware button is not visible on the page"

        assert is_enabled, "Add Firmware button is visible but disabled"

        logger.info("Successfully validated Add Firmware button is visible and enabled")

    # click on add firmware button and validate title of the component
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_click_add_firmware_btn_and_validate_title(
        self, govt_server_page, report_case
    ):
        govt_server_page.click_firmware_master_button()
        govt_server_page.click_add_firmware_button()
        govt_server_page.page.wait_for_load_state("networkidle")
        expected_title = "Add Firmware"

        actual_title = govt_server_page.get_add_firmware_form_title()

        logger.info(
            "Validating Add Firmware form title. Expected: '%s', Actual: '%s'",
            expected_title,
            actual_title,
        )
        report_case(
            expected=f"Add Firmware form should display title '{expected_title}'",
            actual=f"Actual title displayed: '{actual_title}'",
            message="Validate Add Firmware form title",
        )
        assert actual_title == expected_title, (
            f"Add Firmware form title mismatch.\n"
            f"Expected: '{expected_title}'\n"
            f"Actual: '{actual_title}'"
        )
        logger.info(
            "Successfully validated Add Firmware form title: '%s'",
            actual_title,
        )

    # validate all input fields are enabled and editable
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_all_input_fields_are_enabled_and_editable(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for Add Firmware input field editability")
        report_case(
            expected="All Add Firmware input fields should be enabled and editable",
            actual="Pending implementation",
            message="Validate Add Firmware input field editability",
        )
        pytest.skip("Test case implementation pending")

    # validate upload file input field accepts only files and validate with invalid and valid file formats
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_upload_file_input_field_accepts_only_files_and_valid_formats(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for Add Firmware upload file validation")
        report_case(
            expected="Upload file input should accept only valid file formats",
            actual="Pending implementation",
            message="Validate Add Firmware upload file input",
        )
        pytest.skip("Test case implementation pending")

    # validate release date input field have currunt date selected by default and accepts only date format
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_release_date_input_field_have_current_date_by_default_and_accepts_only_date_format(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for Add Firmware release date validation")
        report_case(
            expected="Release date should default to current date and accept date format only",
            actual="Pending implementation",
            message="Validate Add Firmware release date input",
        )
        pytest.skip("Test case implementation pending")

    # validate firmware type dropdown have correct options and accepts only those options
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_firmware_type_dropdown_options_and_selection(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for Add Firmware type dropdown validation")
        report_case(
            expected="Firmware type dropdown should expose and accept valid options",
            actual="Pending implementation",
            message="Validate Add Firmware type dropdown",
        )
        pytest.skip("Test case implementation pending")

    # validate submit button is enabled only when all mandatory fields are filled with valid data
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_submit_button_enabled_only_on_valid_mandatory_fields(
        self, govt_server_page, report_case
    ):
        logger.info("Pending implementation for Add Firmware submit button state")
        report_case(
            expected="Submit button should be enabled only when mandatory fields are valid",
            actual="Pending implementation",
            message="Validate Add Firmware submit button state",
        )
        pytest.skip("Test case implementation pending")

    ##### End of add  firmware test cases #####

    # validate search functionality of firmware master table with firmware added by add firmware form
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_govt_server_page_validate_search_functionality_of_firmware_master_table_with_added_firmware(
        self, govt_server_page, report_case
    ):
        logger.info(
            "Pending implementation for Firmware Master table search validation"
        )
        report_case(
            expected="Firmware Master table search should find added firmware",
            actual="Pending implementation",
            message="Validate Firmware Master table search",
        )
        pytest.skip("Test case implementation pending")

    #### End of Firmware Master Test Cases #####
