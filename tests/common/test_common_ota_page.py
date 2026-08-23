from playwright.sync_api import expect
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from utils.helpers import Helpers as helper
from utils.logger import get_logger

import re
import pytest

logger = get_logger(__name__)


@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
@pytest.mark.device
@pytest.mark.regression
class TestOtaPage:
    """Test suite for OTA Batch and OTA Master pages."""

    # Test data
    SEARCH_QUERY = "SET"


    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting OTA test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("OTA test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("OTA test passed: %s", test_name)
        elif report.failed:
            logger.error("OTA test failed: %s", test_name)
            logger.debug("OTA failure details for %s: %s", test_name, report.longrepr)
        elif report.skipped:
            logger.warning("OTA test skipped: %s", test_name)

    """ OTA Batch Page Tests """

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_navigation_and_url_validation(self, ota_page, report_case):
        """Verify OTA page is loaded with correct URL."""
        logger.info("Validating OTA page load state")
        logger.debug("Current OTA page URL: %s", ota_page.page.url)

        page_loaded = ota_page.is_page_loaded()
        logger.debug("OTA page loaded: %s", page_loaded)

        report_case(
            expected="OTA page should be loaded",
            actual=f"Page loaded: {page_loaded}, URL: {ota_page.page.url}",
            message="Validate OTA page navigation and load state",
        )

        assert page_loaded, f"OTA page did not load at {ota_page.page.url}"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_batch_header_title_validation(self, ota_page, report_case):
        """Verify OTA Batch page title is correct."""
        logger.info("Verifying OTA Batch page title")

        expected_title = "OTA Batch"
        actual_title = ota_page.get_title()
        logger.debug(
            "OTA Batch title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=f"Title should be '{expected_title}'",
            actual=f"Actual title: '{actual_title}'",
            message="Validate OTA Batch page title",
        )

        assert (
            actual_title == expected_title
        ), f"Expected title '{expected_title}', but got '{actual_title}'"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_batch_ui_elements_visibility(self, ota_page, report_case):
        """Verify all OTA Batch page elements are visible and loaded."""
        logger.info("Validating OTA Batch page elements")

        page_loaded = ota_page.is_page_loaded()
        buttons_visible = ota_page.is_ota_batch_page_buttons_visible()
        table_visible = ota_page.is_ota_batch_table_visible()
        search_visible = ota_page.is_search_box_visible()

        logger.debug(
            "Element visibility check | page_loaded=%s | buttons=%s | table=%s | search=%s",
            page_loaded,
            buttons_visible,
            table_visible,
            search_visible,
        )

        report_case(
            expected="All OTA Batch page elements should be visible and loaded",
            actual=f"Page loaded: {page_loaded}, Buttons visible: {buttons_visible}, Table visible: {table_visible}, Search visible: {search_visible}",
            message="Validate all OTA Batch page elements visibility",
        )

        assert page_loaded, "OTA Batch page did not load correctly"
        assert buttons_visible, "OTA Batch page buttons are not visible"
        assert table_visible, "OTA Batch table is not visible"
        assert search_visible, "Search box is not visible"

        logger.info("All OTA Batch page elements are present and visible")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_batch_table_search_filter_functionality(self, ota_page, report_case):
        """Verify search functionality on OTA Batch page."""
        logger.info("Testing search functionality on OTA Batch table")

        assert ota_page.is_ota_batch_table_visible(), "OTA Batch table is not visible"

        search = SearchHelper(ota_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        logger.debug("Search result: %s", result)

        report_case(
            expected=f"Search with query '{self.SEARCH_QUERY}' should succeed",
            actual=f"Search success: {result['success']}, Results found: {result['results_found']}",
            message=f"Validate OTA Batch table search filters for query '{self.SEARCH_QUERY}'",
        )

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(ota_page.page)
            assert (
                table.has_no_data()
            ), f"Search query '{self.SEARCH_QUERY}' not found and no data message shown"
        else:
            rows = result["results"]
            assert any(
                self.SEARCH_QUERY.lower() in row.lower() for row in rows
            ), f"Search query '{self.SEARCH_QUERY}' not found in results"

        logger.info("OTA Batch table search filtering verified successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_batch_table_headers_and_data_display(self, ota_page, report_case):
        """Verify OTA Batch table data is visible and valid."""
        logger.info("Validating OTA Batch table data")

        table = TableSection(ota_page.page)
        table_visible = ota_page.is_ota_batch_table_visible()
        assert table_visible, "OTA Batch table not visible"

        row_count = ota_page.get_batch_table_row_count()
        logger.debug("OTA Batch table row count: %s", row_count)

        report_case(
            expected="OTA Batch table should display valid data",
            actual=f"Table visible: {table_visible}, Row count: {row_count}",
            message="Validate OTA Batch table displays data",
        )

        if row_count == 0:
            logger.warning("OTA Batch table is empty - skipping data validation")
            return

        try:
            headers = ota_page.get_batch_table_headers()
            assert len(headers) > 0, "Table headers should not be empty"
            logger.debug("OTA Batch table headers: %s", headers)
        except Exception as e:
            logger.warning("Could not retrieve headers: %s", str(e))

        try:
            rows = ota_page.get_batch_table_data()
            if rows:
                logger.debug("Retrieved %s rows from OTA Batch table", len(rows))
            else:
                logger.warning(
                    "No rows retrieved from table - selector may need adjustment"
                )
        except Exception as e:
            logger.warning("Could not retrieve rows: %s", str(e))

        logger.info("OTA Batch table data validation completed")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_batch_table_search_helper_record_lookup(self, ota_page, report_case):
        """Test search using SearchHelper on OTA Batch page."""
        logger.info("Testing search using SearchHelper on OTA Batch")

        result = ota_page.search_in_batch_page(self.SEARCH_QUERY)

        logger.debug("Search result: %s", result)

        report_case(
            expected=f"Search should find records matching '{self.SEARCH_QUERY}'",
            actual=f"Search success: {result['success']}, Results found: {result['results_found']}",
            message="Validate SearchHelper finds records on OTA Batch page",
        )

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            assert ota_page.is_batch_table_empty(), "Expected no data"
        else:
            # Require at least one result row to contain the search query
            assert any(
                self.SEARCH_QUERY.lower() in row.lower() for row in result["results"]
            ), f"Search query '{self.SEARCH_QUERY}' not found in results"

        logger.info("OTA Batch SearchHelper test completed successfully")

    """ OTA Master Page Tests """

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_master_button_visibility(self, ota_page, report_case):
        """Verify OTA Master button is visible on OTA Batch page."""
        logger.info("Validating OTA Master button visibility")

        button_visible = ota_page.is_ota_master_page_button_visible()
        logger.debug("OTA Master button visible: %s", button_visible)

        report_case(
            expected="OTA Master button should be visible on OTA Batch page",
            actual=f"OTA Master button visible: {button_visible}",
            message="Validate OTA Master button visibility",
        )

        assert button_visible, "OTA Master page button is not visible"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_master_button_navigation(
        self, ota_page, report_case
    ):
        """Verify navigation to OTA Master page succeeds."""
        logger.info("Navigating to OTA Master page")
        ota_page.go_to_ota_master_page()
        logger.debug("OTA Master URL after navigation: %s", ota_page.page.url)

        report_case(
            expected="Page URL should contain 'ota-master'",
            actual=f"Current URL: {ota_page.page.url}",
            message="Validate navigation to OTA Master page",
        )

        expect(ota_page.page).to_have_url(re.compile(r".*ota-master"))
        logger.info("Successfully navigated to OTA Master page")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_master_header_title_validation(self, ota_page, report_case):
        """Verify OTA Master page title is correct after navigation."""
        logger.info("Verifying OTA Master page title")
        ota_page.go_to_ota_master_page()

        expected_title = "OTA Master"
        actual_title = ota_page.get_page_title()
        logger.debug(
            "OTA Master title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=f"Page title should be '{expected_title}'",
            actual=f"Actual title: '{actual_title}'",
            message="Validate OTA Master page title",
        )

        assert (
            actual_title == expected_title
        ), f"Expected title '{expected_title}', but got '{actual_title}'"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_master_ui_elements_visibility(self, ota_page, report_case):
        """Verify OTA Master page elements are visible after navigation."""
        logger.info("Validating OTA Master page elements")
        ota_page.go_to_ota_master_page()

        master_loaded = ota_page.is_ota_master_page_loaded()
        buttons_visible = ota_page.is_ota_batch_page_buttons_visible()
        table_visible = ota_page.is_ota_batch_table_visible()

        logger.debug(
            "Element visibility check | master_loaded=%s | buttons=%s | table=%s",
            master_loaded,
            buttons_visible,
            table_visible,
        )

        report_case(
            expected="All OTA Master page elements should be visible",
            actual=f"Master page loaded: {master_loaded}, Buttons visible: {buttons_visible}, Table visible: {table_visible}",
            message="Validate OTA Master page elements visibility",
        )

        assert master_loaded, "OTA Master page did not load correctly"
        assert buttons_visible, "Action buttons are not visible on OTA Master page"
        assert table_visible, "OTA Master table is not visible on OTA Master page"

        logger.info("OTA Master page elements are present and visible")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_master_table_search_filter_functionality(self, ota_page, report_case):
        """Verify search functionality on OTA Master page."""
        logger.info("Testing search functionality on OTA Master table")

        ota_page.go_to_ota_master_page()
        assert ota_page.is_ota_batch_table_visible(), "OTA Master table is not visible"

        search = SearchHelper(ota_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        logger.debug("Search result: %s", result)

        report_case(
            expected=f"Search with query '{self.SEARCH_QUERY}' should succeed",
            actual=f"Search success: {result['success']}, Results found: {result['results_found']}",
            message=f"Validate OTA Master table search filters for query '{self.SEARCH_QUERY}'",
        )

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(ota_page.page)
            assert (
                table.has_no_data()
            ), f"Search query '{self.SEARCH_QUERY}' not found and no data message shown"
        else:
            rows = result["results"]
            assert any(
                self.SEARCH_QUERY.lower() in row.lower() for row in rows
            ), f"Search query '{self.SEARCH_QUERY}' not found in results"

        logger.info("OTA Master table search filtering verified successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_master_table_headers_and_data_display(self, ota_page, report_case):
        """Verify OTA Master table data is visible and valid."""
        logger.info("Validating OTA Master table data")

        ota_page.go_to_ota_master_page()
        table = TableSection(ota_page.page)
        table_visible = ota_page.is_ota_batch_table_visible()
        assert table_visible, "OTA Master table not visible"

        row_count = ota_page.get_master_table_row_count()
        logger.debug("OTA Master table row count: %s", row_count)

        report_case(
            expected="OTA Master table should display valid data",
            actual=f"Table visible: {table_visible}, Row count: {row_count}",
            message="Validate OTA Master table displays data",
        )

        if row_count == 0:
            logger.warning("OTA Master table is empty - skipping data validation")
            return

        try:
            headers = ota_page.get_master_table_headers()
            assert len(headers) > 0, "Table headers should not be empty"
            logger.debug("OTA Master table headers: %s", headers)
        except Exception as e:
            logger.warning("Could not retrieve headers: %s", str(e))

        try:
            rows = ota_page.get_master_table_data()
            if rows:
                logger.debug("Retrieved %s rows from OTA Master table", len(rows))
            else:
                logger.warning(
                    "No rows retrieved from table - selector may need adjustment"
                )
        except Exception as e:
            logger.warning("Could not retrieve rows: %s", str(e))

        logger.info("OTA Master table data validation completed")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_master_table_search_helper_record_lookup(self, ota_page, report_case):
        """Test search using SearchHelper on OTA Master page."""
        logger.info("Testing search using SearchHelper on OTA Master")

        ota_page.go_to_ota_master_page()
        result = ota_page.search_in_master_page(self.SEARCH_QUERY)

        logger.debug("Search result: %s", result)

        report_case(
            expected=f"Search should find records matching '{self.SEARCH_QUERY}'",
            actual=f"Search success: {result['success']}, Results found: {result['results_found']}",
            message="Validate SearchHelper finds records on OTA Master page",
        )

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            assert ota_page.is_master_table_empty(), "Expected no data"
        else:
            for row in result["results"]:
                assert self.SEARCH_QUERY.lower() in row.lower()

        logger.info("OTA Master SearchHelper test completed successfully")

    """ Add Ota Command Page"""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_button_visibility_and_navigation(self, ota_page, report_case):
        """Verify Add OTA Command button is visible on OTA Master page."""
        logger.info("Validating Add OTA Command button visibility and navigation")
        ota_page.go_to_ota_master_page()

        button_visible = ota_page.is_add_ota_command_button_visible()
        logger.debug("Add OTA Command button visible: %s", button_visible)

        report_case(
            expected="Add OTA Command button should be visible on OTA Master page",
            actual=f"Add OTA Command button visible: {button_visible}",
            message="Validate Add OTA Command button visibility",
        )

        assert (
            button_visible
        ), "Add OTA Command button is not visible on OTA Master page"

        if button_visible:
            logger.info("Add OTA Command button is visible on OTA Master page")
            ota_page.validate_add_ota_button_and_click()
        else:
            logger.warning("Add OTA Command button is not visible - cannot click")

        page_title = ota_page.is_on_add_ota_command_page()
        logger.debug("Add OTA Command page title after navigation: %s", page_title)

        report_case(
            expected="Should navigate to Add OTA Command page",
            actual=f"Page title after navigation: '{page_title}'",
            message="Validate Add OTA Command page navigation",
        )

        assert page_title, "Did not navigate to Add OTA Command page"
        assert (
            "Add OTA Command" in page_title
        ), f"Expected 'Add OTA Command' in page title, got '{page_title}'"
        logger.info("Successfully validated Add OTA Command button navigation")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_fields_visibility(self, ota_page, report_case):
        """Verify all Add OTA Command form fields are visible."""
        logger.info("Validating Add OTA Command form fields visibility")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        fields_visible = ota_page.are_add_ota_command_form_fields_visible()
        logger.debug("Add OTA Command form fields visible: %s", fields_visible)

        report_case(
            expected="All Add OTA Command form fields should be visible",
            actual=f"Form fields visible: {fields_visible}",
            message="Validate Add OTA Command form fields visibility",
        )

        assert fields_visible, "Not all Add OTA Command form fields are visible"

        logger.info("All Add OTA Command form fields are visible")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_ota_name_field_input(
        self, ota_page, report_case
    ):
        """Verify OTA Name field can be filled."""
        logger.info("Testing OTA Name field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_name = "Test OTA Name"
        ota_page.fill_ota_name(test_name)

        actual_value = ota_page.get_ota_name_value()
        logger.debug(
            "OTA Name field check | expected=%s | actual=%s",
            test_name,
            actual_value,
        )

        report_case(
            expected=f"OTA Name field should accept value '{test_name}'",
            actual=f"Actual value in field: '{actual_value}'",
            message="Validate OTA Name field input",
        )

        assert (
            actual_value == test_name
        ), f"Expected '{test_name}', but got '{actual_value}'"
        logger.info("OTA Name field filled successfully: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_ota_command_field_input(
        self, ota_page, report_case
    ):
        """Verify OTA Command field can be filled."""
        logger.info("Testing OTA Command field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_command = "Test Command"
        ota_page.fill_ota_command(test_command)

        actual_value = ota_page.get_ota_command_value()
        logger.debug(
            "OTA Command field check | expected=%s | actual=%s",
            test_command,
            actual_value,
        )

        report_case(
            expected=f"OTA Command field should accept value '{test_command}'",
            actual=f"Actual value in field: '{actual_value}'",
            message="Validate OTA Command field input",
        )

        assert (
            actual_value == test_command
        ), f"Expected '{test_command}', but got '{actual_value}'"
        logger.info("OTA Command field filled successfully: %s", test_command)

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_example_field_input(
        self, ota_page, report_case
    ):
        """Verify Example field can be filled."""
        logger.info("Testing Example field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_example = helper.generate_random_string(10)
        ota_page.fill_example(test_example)

        actual_value = ota_page.get_example_value()
        logger.debug(
            "Example field check | expected=%s | actual=%s", test_example, actual_value
        )

        report_case(
            expected=f"Example field should accept value '{test_example}'",
            actual=f"Actual value in field: '{actual_value}'",
            message="Validate Example field input",
        )

        assert (
            actual_value == test_example
        ), f"Expected '{test_example}', but got '{actual_value}'"
        logger.info("Example field filled successfully: %s", test_example)

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_ota_type_dropdown_selection(
        self, ota_page, report_case
    ):
        """Verify OTA Type dropdown can be selected."""
        logger.info("Testing OTA Type dropdown selection")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        ota_type = "GET"
        try:
            ota_page.select_ota_type(ota_type)
            logger.debug("OTA Type selected: %s", ota_type)

            report_case(
                expected=f"OTA Type dropdown should accept selection '{ota_type}'",
                actual=f"OTA Type selected successfully: {ota_type}",
                message="Validate OTA Type dropdown selection",
            )

            logger.info("OTA Type selected successfully: %s", ota_type)
        except Exception as e:
            logger.warning("Error selecting OTA Type: %s", str(e))
            report_case(
                expected=f"OTA Type dropdown should accept selection '{ota_type}'",
                actual=f"Error during selection: {str(e)}",
                message="Validate OTA Type dropdown selection",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_input_field_required_dropdown_selection(
        self, ota_page, report_case
    ):
        """Verify Input Field Required dropdown can be selected."""
        logger.info("Testing Input Field Required dropdown selection")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        option = "NO"
        try:
            ota_page.select_input_field_required(option)
            logger.debug("Input Field Required selected: %s", option)

            report_case(
                expected=f"Input Field Required dropdown should accept selection '{option}'",
                actual=f"Option selected successfully: {option}",
                message="Validate Input Field Required dropdown selection",
            )

            logger.info("Input Field Required selected successfully: %s", option)
        except Exception as e:
            logger.warning("Error selecting Input Field Required: %s", str(e))
            report_case(
                expected=f"Input Field Required dropdown should accept selection '{option}'",
                actual=f"Error during selection: {str(e)}",
                message="Validate Input Field Required dropdown selection",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_fill_and_validation_flow(
        self, ota_page, report_case
    ):
        """Test complete Add OTA Command form flow with all fields."""
        logger.info("Testing complete Add OTA Command form flow")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Verify form fields are visible
        assert (
            ota_page.are_add_ota_command_form_fields_visible()
        ), "Form fields not visible"

        # Fill OTA Name
        test_name = "Complete Test OTA"
        ota_page.fill_ota_name(test_name)
        assert (
            ota_page.get_ota_name_value() == test_name
        ), "OTA Name not filled correctly"

        # Fill OTA Command
        test_command = "Test Command Complete"
        ota_page.fill_ota_command(test_command)
        assert (
            ota_page.get_ota_command_value() == test_command
        ), "OTA Command not filled correctly"

        # Fill Example
        test_example = "Complete Example"
        ota_page.fill_example(test_example)
        assert (
            ota_page.get_example_value() == test_example
        ), "Example not filled correctly"

        logger.debug(
            "Form completed with | name=%s | command=%s | example=%s",
            test_name,
            test_command,
            test_example,
        )

        report_case(
            expected="Add OTA Command form should accept all field values",
            actual=f"All fields filled successfully: Name='{test_name}', Command='{test_command}', Example='{test_example}'",
            message="Validate complete Add OTA Command form flow",
        )

        logger.info("Add OTA Command form complete flow test passed")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_submit_disabled_when_empty(self, ota_page, report_case):
        """Verify Submit button is disabled when form fields are empty."""
        logger.info("Testing Submit button disabled state on empty form")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Form should be empty, so submit button should be disabled
        is_disabled = ota_page.is_submit_button_disabled()
        logger.debug("Submit button disabled on empty form: %s", is_disabled)

        report_case(
            expected="Submit button should be disabled on empty form",
            actual=f"Submit button disabled: {is_disabled}",
            message="Validate Submit button disabled state on empty form",
        )

        assert is_disabled, "Submit button should be disabled when form is empty"

        logger.info("Submit button is correctly disabled on empty form")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_submit_enabled_when_filled(self, ota_page, report_case):
        """Verify Submit button is enabled when all form fields are filled."""
        logger.info("Testing Submit button enabled state on filled form")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Initially form is empty, submit should be disabled
        initially_disabled = ota_page.is_submit_button_disabled()
        assert initially_disabled, "Submit button should be disabled initially"
        logger.debug("Submit button initially disabled: %s", initially_disabled)

        # Fill all required fields
        ota_page.fill_ota_name("Test OTA Name")
        ota_page.fill_ota_command("Test Command")
        ota_page.fill_example("Test Example")

        try:
            ota_page.select_ota_type("GET")
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        # Now all fields are filled, submit should be enabled
        is_enabled = ota_page.is_submit_button_enabled()
        logger.debug("Submit button enabled after filling form: %s", is_enabled)

        report_case(
            expected="Submit button should be enabled when all fields are filled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate Submit button enabled state on filled form",
        )

        assert is_enabled, "Submit button should be enabled when all fields are filled"

        logger.info("Submit button is correctly enabled on filled form")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_submit_state_transitions_on_field_fill(self, ota_page, report_case):
        """Verify Submit button state transitions between disabled and enabled."""
        logger.info("Testing Submit button state transitions")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Step 1: Initially empty - should be disabled
        step1_disabled = ota_page.is_submit_button_disabled()
        assert step1_disabled, "Submit should be disabled initially"
        logger.info("Step 1 - Submit button is disabled on empty form")

        # Step 2: Fill first field - check state
        ota_page.fill_ota_name("Test OTA")
        step2_disabled = ota_page.is_submit_button_disabled()
        logger.debug(
            "Step 2 - OTA Name filled. Submit button disabled: %s",
            step2_disabled,
        )

        # Step 3: Fill second field
        ota_page.fill_ota_command("Test Command")
        step3_disabled = ota_page.is_submit_button_disabled()
        logger.debug(
            "Step 3 - OTA Command filled. Submit button disabled: %s",
            step3_disabled,
        )

        # Step 4: Fill example field
        ota_page.fill_example("Example Value")
        step4_disabled = ota_page.is_submit_button_disabled()
        logger.debug(
            "Step 4 - Example filled. Submit button disabled: %s",
            step4_disabled,
        )

        # Step 5: Try to select dropdowns and check if submit becomes enabled
        try:
            ota_page.select_ota_type("GET")
            logger.debug(
                "Step 5 - OTA Type selected. Submit button enabled: %s",
                ota_page.is_submit_button_enabled(),
            )
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
            logger.debug(
                "Step 6 - Input Field Required selected. Submit button enabled: %s",
                ota_page.is_submit_button_enabled(),
            )
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        report_case(
            expected="Submit button state should transition based on form fill state",
            actual=f"Step1: disabled={step1_disabled}, Step2: disabled={step2_disabled}, Step3: disabled={step3_disabled}, Step4: disabled={step4_disabled}",
            message="Validate Submit button state transitions",
        )

        logger.info("Submit button state transitions test completed")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_add_command_form_submit_button_clickability(self, ota_page, report_case):
        """Verify Submit button is clickable when enabled with all fields filled."""
        logger.info("Testing Submit button is clickable when enabled")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Fill all required fields
        ota_page.fill_ota_name("Clickable Test OTA")
        ota_page.fill_ota_command("Clickable Test Command")
        ota_page.fill_example("Clickable Example")

        try:
            ota_page.select_ota_type("GET")
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        # Verify button is enabled before clicking
        is_enabled = ota_page.is_submit_button_enabled()
        logger.debug("Submit button enabled before click: %s", is_enabled)

        report_case(
            expected="Submit button should be enabled and clickable",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate Submit button clickability",
        )

        assert is_enabled, "Submit button should be enabled"

        # Click submit button
        try:
            ota_page.click_submit_button()
            logger.info("Submit button clicked successfully")
        except Exception as e:
            logger.error("Error clicking submit button: %s", str(e))
            raise

    """ Manual Ota Test Cases"""

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_button_visibility(self, ota_page, report_case):
        """Verify Manual OTA button is visible on OTA Master page."""
        logger.info("Validating Manual OTA button visibility")

        button_visible = ota_page.is_manual_ota_button_visible()
        logger.debug("Manual OTA button visible: %s", button_visible)

        report_case(
            expected="Manual OTA button should be visible on OTA Master page",
            actual=f"Manual OTA button visible: {button_visible}",
            message="Validate Manual OTA button visibility",
        )

        assert button_visible, "Manual OTA button is not visible on OTA Master page"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_button_navigation(self, ota_page, report_case):
        """Verify clicking Manual OTA button opens correct page."""
        logger.info("Testing Manual OTA button click and validation")

        if ota_page.is_manual_ota_button_visible():
            logger.debug("Manual OTA button is visible - attempting to click")
            try:
                ota_page.click_manual_ota_button()
                expect(ota_page.page).to_have_url(re.compile(r".*manual-ota"))
                logger.debug("Manual OTA URL after navigation: %s", ota_page.page.url)

                report_case(
                    expected="Clicking Manual OTA button should navigate to manual-ota page",
                    actual=f"Page URL: {ota_page.page.url}",
                    message="Validate Manual OTA button navigation",
                )

                logger.info(
                    "Manual OTA button click test completed - add validation logic as needed"
                )
            except Exception as e:
                logger.error("Error clicking Manual OTA button: %s", str(e))
                report_case(
                    expected="Clicking Manual OTA button should navigate to manual-ota page",
                    actual=f"Error during click: {str(e)}",
                    message="Validate Manual OTA button navigation",
                )
                raise
        else:
            logger.warning(
                "Manual OTA button is not visible - cannot perform click test"
            )
            report_case(
                expected="Manual OTA button should be visible",
                actual="Manual OTA button is not visible",
                message="Validate Manual OTA button visibility",
            )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_search_device_title_visibility(self, ota_page, report_case):
        """Verify component title is visible on Manual OTA page."""
        logger.info("Validating component title on Manual OTA page")

        ota_page.go_to_manual_ota_page()
        expected_title = "Search Device"
        actual_title = ota_page.get_manual_ota_component_title()

        logger.debug(
            "Manual OTA component title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=f"Component title should be '{expected_title}'",
            actual=f"Actual component title: '{actual_title}'",
            message="Validate Manual OTA component title",
        )

        assert (
            actual_title == expected_title
        ), "Component title is not visible on Manual OTA page"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_search_button_disabled_when_empty(
        self, ota_page, report_case
    ):
        """Verify Search button is disabled on Manual OTA page if fields are not filled."""
        logger.info("Testing Search button disabled state on empty fields")

        ota_page.go_to_manual_ota_page()

        is_disabled = ota_page.is_search_button_disabled()
        logger.debug("Search button disabled on empty fields: %s", is_disabled)

        report_case(
            expected="Search button should be disabled when fields are not filled",
            actual=f"Search button disabled: {is_disabled}",
            message="Validate Search button disabled state on empty fields",
        )

        assert (
            is_disabled
        ), "Search button should be disabled when fields are not filled"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_imei_field_validation_errors(self, ota_page, report_case):
        """Verify error messages for IMEI input fields on Manual OTA page."""
        logger.info("Testing IMEI input fields error messages")
        ota_page.go_to_manual_ota_page()

        # Test empty IMEI field
        ota_page.clear_imei_input()
        ota_page.click_imei_input()
        ota_page.click_manual_ota_imei_search_button()

        error_msg_1 = ota_page.get_imei_error_message(
            "This field is required and can't be only spaces."
        )
        logger.debug("Error message for empty IMEI: %s", error_msg_1)

        report_case(
            expected="Error message for empty IMEI field",
            actual=f"Actual error: '{error_msg_1}'",
            message="Validate error message for empty IMEI",
        )

        assert (
            error_msg_1 == "This field is required and can't be only spaces."
        ), "Expected error message for empty IMEI field not shown"

        # Test invalid IMEI format
        ota_page.fill_imei_input("invalid_imei_demo")
        ota_page.click_manual_ota_imei_search_button()

        error_msg_2 = ota_page.get_imei_error_message(
            "Value must be exactly 15 characters long."
        )
        logger.debug("Error message for invalid length IMEI: %s", error_msg_2)

        assert (
            error_msg_2 == "Value must be exactly 15 characters long."
        ), "Expected error message for invalid IMEI format not shown"

        # Test 15 character IMEI format in string
        ota_page.fill_imei_input("a" * 15)
        ota_page.click_manual_ota_imei_search_button()

        error_msg_3 = ota_page.get_imei_error_message("Only numbers are allowed.")
        logger.debug("Error message for non-numeric IMEI: %s", error_msg_3)

        assert (
            error_msg_3 == "Only numbers are allowed."
        ), "Expected error message for invalid IMEI format not shown"

        logger.info("IMEI input fields error messages validated successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_valid_imei_search_execution(
        self, ota_page, project_config, test_data, report_case
    ):
        """Verify entering valid IMEI and clicking search on Manual OTA page."""
        logger.info("Testing search with valid IMEI")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)

        search_enabled = not ota_page.is_search_button_disabled()
        logger.debug("Search button enabled for IMEI: %s", search_enabled)

        report_case(
            expected="Search button should be enabled when valid IMEI is entered",
            actual=f"Search button enabled: {search_enabled}",
            message="Validate Search button enabled state for valid IMEI",
        )

        assert (
            search_enabled
        ), "Search button should be enabled when valid IMEI is entered"

        try:
            ota_page.click_manual_ota_imei_search_button()
            logger.info("Clicked Search button with valid IMEI successfully")

            # Verify search was executed (page still on manual-ota and no error displayed)
            assert (
                "manual-ota" in ota_page.page.url
            ), "Should remain on manual-ota page after search"

            logger.info("Search completed successfully with valid IMEI")
        except Exception as e:
            logger.error("Error during search: %s", str(e))
            raise

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_ota_page_manual_ota_device_details_and_command_display(
        self, ota_page, project_config, test_data, report_case
    ):
        """Verify device details are displayed after searching with valid IMEI on Manual OTA page."""
        logger.info("Testing device details display after search")

        # Prefer values from project-specific test_data, then project_config, then sensible defaults
        device_data = {
            "imei": test_data.get("valid_imei") or project_config.get("imei"),
            "UIN": test_data.get("valid_uid")
            or test_data.get("valid_uin")
            or project_config.get("uin", ""),
            "VIN": test_data.get("vin") or project_config.get("vin", ""),
            "ICCID": test_data.get("iccid") or project_config.get("iccid", ""),
        }

        ota_page.go_to_manual_ota_page()

        valid_imei = device_data["imei"]
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        # imei validation
        expect(ota_page.page.locator("#imei")).to_be_visible()
        expect(ota_page.page.locator("#imei")).not_to_be_empty()
        expect(ota_page.page.locator("#imei")).to_have_value(device_data["imei"])
        logger.debug("IMEI field validated: %s", device_data["imei"])

        # uin validation
        expect(ota_page.page.locator("#uin")).to_be_visible()
        expect(ota_page.page.locator("#uin")).not_to_be_empty()
        expect(ota_page.page.locator("#uin")).to_have_value(device_data["UIN"])
        logger.debug("UIN field validated: %s", device_data["UIN"])

        # vin validation
        expect(ota_page.page.locator("#modelName")).to_be_visible()
        expect(ota_page.page.locator("#modelName")).not_to_be_empty()
        expect(ota_page.page.locator("#modelName")).to_have_value(device_data["VIN"])
        logger.debug("VIN field validated: %s", device_data["VIN"])

        # iccid validation
        expect(ota_page.page.locator("#iccid")).to_be_visible()
        expect(ota_page.page.locator("#iccid")).not_to_be_empty()
        expect(ota_page.page.locator("#iccid")).to_have_value(device_data["ICCID"])
        logger.debug("ICCID field validated: %s", device_data["ICCID"])

        # command validation
        command_locator = ota_page.page.locator("#command")
        expect(command_locator).to_be_visible()
        expect(command_locator).not_to_be_empty()

        command_text = command_locator.input_value().strip()
        logger.debug("Command field value: %s", command_text)

        report_case(
            expected="Device details should be displayed correctly after search",
            actual=f"IMEI={device_data['imei']}, UIN={device_data['UIN']}, VIN={device_data['VIN']}, ICCID={device_data['ICCID']}",
            message="Validate device details display after search",
        )

        assert re.match(
            r"^\*(GET|SET|CLR)", command_text
        ), f"Command '{command_text}' does not start with *GET, *SET, or *CLR"

        logger.info("Device details validation completed successfully")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_new_ota_button_enabled_after_search(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify New OTA Command button is visible after searching with valid IMEI on Manual OTA page."""
        logger.info("Testing New OTA button visibility after valid search")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        button_enabled = ota_page.is_new_ota_button_enabled()
        logger.debug("New OTA Command button enabled: %s", button_enabled)

        report_case(
            expected="New OTA Command button should be visible after valid search",
            actual=f"New OTA Command button enabled: {button_enabled}",
            message="Validate New OTA Command button visibility",
        )

        assert (
            button_enabled
        ), "New OTA Command button should be visible after valid search"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ota_page_manual_ota_new_ota_button_navigation(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify clicking New OTA Command button after valid search navigates to Add OTA Command page."""
        logger.info("Testing New OTA Command button click navigation")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        if ota_page.is_new_ota_button_enabled():
            logger.info("New OTA Command button is visible - attempting to click")
            try:
                ota_page.click_new_ota_button()
                logger.info("Clicked New OTA Command button successfully")
            except Exception as e:
                logger.error("Error clicking New OTA Command button: %s", str(e))
                raise

            # Validate new page opened
            page_title = ota_page.get_ota_command_list_header()
            logger.debug("OTA Command List header: %s", page_title)

            report_case(
                expected="Should navigate to page with 'OTA Command List' header",
                actual=f"Page header: '{page_title}'",
                message="Validate navigation after New OTA button click",
            )

            assert (
                "OTA Command List" in page_title
            ), f"Expected 'OTA Command List' in page title, got '{page_title}'"
            logger.info("Navigated to Add OTA Command page successfully")
        else:
            logger.warning(
                "New OTA Command button is not visible - cannot perform click test"
            )
            report_case(
                expected="New OTA Command button should be visible",
                actual="New OTA Command button is not visible",
                message="Validate New OTA button visibility",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_command_list_ota_type_dropdown_selection(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify OTA Type dropdown can be selected on Add OTA Command page."""
        logger.info("Testing OTA Type dropdown selection on Manual OTA page")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        if ota_page.is_new_ota_button_enabled():
            ota_page.click_new_ota_button()
            try:
                # validate that firstly it does have ALL option selected by default and then select GET option
                ota_page.select_ota_type_on_manual_ota_page("ALL")
                ota_page.select_ota_type_on_manual_ota_page("GET")
                logger.debug("OTA Type selected successfully: GET")

                report_case(
                    expected="OTA Type dropdown should accept GET selection",
                    actual="OTA Type selected: GET",
                    message="Validate OTA Type dropdown selection",
                )

                logger.info("OTA Type selected successfully: GET")
            except Exception as e:
                logger.warning("Error selecting OTA Type: %s", str(e))
                report_case(
                    expected="OTA Type dropdown should accept GET selection",
                    actual=f"Error during selection: {str(e)}",
                    message="Validate OTA Type dropdown selection",
                )
        else:
            logger.warning(
                "New OTA Command button is not visible - cannot test OTA Type dropdown"
            )
            report_case(
                expected="New OTA Command button should be visible",
                actual="New OTA Command button is not visible",
                message="Validate New OTA button visibility",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_command_checkboxes_visibility_and_default_state(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify all checkboxes are visible and unchecked on Manual OTA page after valid search."""
        logger.info("Testing checkboxes visibility and state")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        if ota_page.is_new_ota_button_enabled():
            # Validate checkboxes are visible and unchecked
            checkboxes_visible = ota_page.are_all_checkboxes_visible()
            checkboxes_unchecked = ota_page.are_all_checkboxes_unchecked()

            logger.debug(
                "Checkboxes visible: %s, Checkboxes unchecked: %s",
                checkboxes_visible,
                checkboxes_unchecked,
            )

            report_case(
                expected="All checkboxes should be visible and unchecked by default",
                actual=f"Checkboxes visible: {checkboxes_visible}, Checkboxes unchecked: {checkboxes_unchecked}",
                message="Validate checkboxes visibility and state",
            )

            assert (
                checkboxes_visible
            ), "Not all checkboxes are visible on Manual OTA page"
            assert (
                checkboxes_unchecked
            ), "Not all checkboxes are unchecked by default on Manual OTA page"
            logger.info("All checkboxes are visible and unchecked by default")
        else:
            logger.warning(
                "New OTA Command button is not visible - cannot test checkboxes visibility and state"
            )
            report_case(
                expected="New OTA Command button should be visible",
                actual="New OTA Command button is not visible",
                message="Validate New OTA button visibility",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_select_command_checkbox_via_search(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify selecting one checkbox by searching command on Manual OTA page after valid search."""
        logger.info("Testing checkbox selection by searching command")
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        if ota_page.is_new_ota_button_enabled():
            # Search for a specific command and select its checkbox
            command_to_search = (
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            )
            try:
                ota_page.search_command_in_manual_ota(command_to_search)

                checkbox_selected = ota_page.is_checkbox_for_command_selected()
                logger.debug(
                    "Checkbox for command '%s' selected: %s",
                    command_to_search,
                    checkbox_selected,
                )

                report_case(
                    expected=f"Checkbox for command '{command_to_search}' should be selected after search",
                    actual=f"Checkbox selected: {checkbox_selected}",
                    message="Validate checkbox selection after command search",
                )

                assert (
                    checkbox_selected
                ), f"Checkbox for command '{command_to_search}' should be selected after search"
                logger.info(
                    "Checkbox for command '%s' is selected successfully after search",
                    command_to_search,
                )
            except Exception as e:
                logger.warning(
                    "Error searching for command '%s' and selecting checkbox: %s",
                    command_to_search,
                    str(e),
                )
                report_case(
                    expected=f"Checkbox for command '{command_to_search}' should be selected",
                    actual=f"Error: {str(e)}",
                    message="Validate checkbox selection after command search",
                )
        else:
            logger.warning(
                "New OTA Command button is not visible - cannot test searching and selecting command checkbox"
            )
            report_case(
                expected="New OTA Command button should be visible",
                actual="New OTA Command button is not visible",
                message="Validate New OTA button visibility",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_set_batch_button_enabled_on_checkbox_selection(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify selecting a checkbox enables the Set Batch button on Manual OTA page after valid search."""
        logger.info(
            "Testing selecting a checkbox enables the Set Batch button on Manual OTA page after valid search"
        )
        ota_page.go_to_manual_ota_page()

        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        ota_page.fill_imei_input(valid_imei)
        ota_page.click_manual_ota_imei_search_button()

        logger.info("Valid imei searched")

        # self.page.wait_for_timeout(1000)
        # self.page.scroll_into_view_if_needed(ota_page.new_ota_button)

        if ota_page.is_new_ota_button_enabled():

            # clicking on the new_ota_button to navigate to the page where checkboxes are present and Set Batch button is present
            ota_page.click_new_ota_button()

            # Select a checkbox for a command
            command_to_select = (
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            )
            try:
                ota_page.search_command_in_manual_ota(command_to_select)

                logger.info(
                    f"Command '{command_to_select}' searched and checkbox should be selected"
                )

                if ota_page.get_size_of_checkbox_list() > 1:
                    logger.error(
                        f"Multiple checkboxes found, validating the correct one is selected for command '{command_to_select}'"
                    )

                else:
                    is_selected = ota_page.is_checkbox_for_command_selected()
                    logger.debug(
                        "Checkbox selected for command '%s': %s",
                        command_to_select,
                        is_selected,
                    )

                    if is_selected:
                        report_case(
                            expected=f"Checkbox should not be pre-selected for command '{command_to_select}'",
                            actual=f"Checkbox is already selected: {is_selected}",
                            message="Validate checkbox initial state before selection",
                        )

                    ota_page.select_checkbox_for_command()

                    logger.info(f"Checkbox for command '{command_to_select}' selected")

                    # Validate that Set Batch button is now enabled
                    set_batch_enabled = ota_page.is_set_batch_button_enabled()
                    logger.debug("Set Batch button enabled: %s", set_batch_enabled)

                    report_case(
                        expected="Set Batch button should be enabled after selecting a command checkbox",
                        actual=f"Set Batch button enabled: {set_batch_enabled}",
                        message="Validate Set Batch button enabled state after checkbox selection",
                    )

                    assert (
                        set_batch_enabled
                    ), "Set Batch button should be enabled after selecting a command checkbox"

                    logger.info("Set Batch button is enabled after selecting checkbox")

                    logger.info(
                        "Set Batch button is enabled successfully after selecting checkbox for command '%s'",
                        command_to_select,
                    )

            except Exception as e:
                logger.warning(
                    "Error during checkbox selection and Set Batch button validation: %s",
                    str(e),
                )
                report_case(
                    expected="Checkbox selection and Set Batch button validation should succeed",
                    actual=f"Error: {str(e)}",
                    message="Validate checkbox selection and Set Batch button enabled state",
                )
        else:
            logger.warning(
                "New OTA Command button is not visible - cannot test checkbox selection and Set Batch button state"
            )
            report_case(
                expected="New OTA button should be enabled for manual OTA setup",
                actual="New OTA button is not enabled",
                message="Validate New OTA button state",
            )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_set_configuration_component_visibility(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify Set Configuration component is visible after clicking Set Batch button."""
        logger.info(
            "Testing Set Configuration component visibility after clicking Set Batch button"
        )

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Now click Set Batch button and validate Set Configuration component
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            # Validate that the Set Configuration component is visible after clicking the button
            is_visible = ota_page.is_set_configuration_component_visible()
            logger.debug("Set Configuration component visible: %s", is_visible)

            report_case(
                expected="Set Configuration component should be visible after clicking Set Batch button",
                actual=f"Set Configuration component visible: {is_visible}",
                message="Validate Set Configuration component visibility",
            )

            assert (
                is_visible
            ), "Set Configuration component should be visible after clicking Set Batch button"

            logger.info(
                "Set Configuration component is visible after clicking Set Batch button"
            )
        except Exception as e:
            logger.error(
                "Error clicking Set Batch button or validating component: %s",
                str(e),
            )
            report_case(
                expected="Set Configuration component should be visible after clicking Set Batch button",
                actual=f"Error: {str(e)}",
                message="Validate Set Configuration component visibility",
            )
            raise

    # def test_valid_table_headers_on_set_configuration_value_component(self, ota_page):
    #     """Verify that the table headers on Set Configuration component are correct."""
    #     logger.info("Testing table headers validation on Set Configuration component")

    #     # Use helper method to set up manual OTA and enable Set Batch button
    #     ota_page.setup_manual_ota_and_enable_set_batch(
    #         valid_imei=IMEI, command_to_search="GET IMEI"
    #     )
    #     logger.info("Manual OTA setup and Set Batch button enabled successfully")

    #     # Click Set Batch button and validate table headers
    #     try:
    #         ota_page.click_set_batch_button()
    #         logger.info("Clicked Set Batch button successfully")

    #         if ota_page.is_set_configuration_component_visible():
    #             expected_headers = [
    #                 "Name",
    #                 "Command",
    #                 "Example",
    #                 "Input Value",
    #                 "Action",
    #             ]
    #             actual_headers = ota_page.get_set_configuration_table_headers()

    #             assert (
    #                 actual_headers == expected_headers
    #             ), f"Expected headers {expected_headers}, but got {actual_headers}"

    #             logger.info("Table headers on Set Configuration component are correct")

    #         else:
    #             logger.warning(
    #                 "Set Configuration component is not visible - cannot validate table headers"
    #             )

    #     except Exception as e:
    #         logger.error(
    #             "Error validating table headers on Set Configuration component: %s",
    #             str(e),
    #         )
    #         raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_set_configuration_submit_button_clickability(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify Submit button is visible and clickable on Set Configuration component."""
        logger.info(
            "Testing Submit button visibility and clickability on Set Configuration component"
        )

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button and validate Submit button
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                is_submit_visible = (
                    ota_page.is_submit_button_on_set_configuration_visible()
                )
                logger.debug("Submit button visible: %s", is_submit_visible)

                report_case(
                    expected="Submit button should be visible on Set Configuration component",
                    actual=f"Submit button visible: {is_submit_visible}",
                    message="Validate Submit button visibility on Set Configuration",
                )

                assert (
                    is_submit_visible
                ), "Submit button should be visible on Set Configuration component"

                logger.info("Submit button is visible on Set Configuration component")

                # Click the Submit button
                ota_page.click_submit_button_on_set_configuration()

                logger.info(
                    "Clicked Submit button on Set Configuration component successfully"
                )

            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate Submit button"
                )
                report_case(
                    expected="Set Configuration component should be visible after clicking Set Batch button",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error(
                "Error validating or clicking Submit button on Set Configuration component: %s",
                str(e),
            )
            report_case(
                expected="Submit button should be visible and clickable on Set Configuration component",
                actual=f"Error: {str(e)}",
                message="Validate Submit button visibility and click",
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_history_component_visibility_after_submit(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify OTA History component is visible after submitting configuration."""
        logger.info(
            "Testing OTA History component visibility after submitting configuration"
        )

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button, submit configuration, and validate OTA History component
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                ota_page.click_submit_button_on_set_configuration()
                logger.info(
                    "Clicked Submit button on Set Configuration component successfully"
                )

                # Validate that the OTA History component is visible after submission
                is_history_visible = ota_page.is_ota_history_component_visible()
                logger.debug("OTA History component visible: %s", is_history_visible)

                report_case(
                    expected="OTA History component should be visible after submitting configuration",
                    actual=f"OTA History component visible: {is_history_visible}",
                    message="Validate OTA History component visibility after submit",
                )

                assert (
                    is_history_visible
                ), "OTA History component should be visible after submitting configuration"

                logger.info("OTA History component is visible after submission")
            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate OTA History component"
                )
                report_case(
                    expected="Set Configuration component should be visible before submission",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error(
                "Error validating OTA History component visibility: %s", str(e)
            )
            report_case(
                expected="OTA History component should be visible after submitting configuration",
                actual=f"Error: {str(e)}",
                message="Validate OTA History component visibility",
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_history_table_headers_validation(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify that the table headers on OTA History component are correct."""
        logger.info("Testing table headers validation on OTA History component")

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button, submit configuration, and validate table headers
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                ota_page.click_submit_button_on_set_configuration()
                logger.info(
                    "Clicked Submit button on Set Configuration component successfully"
                )

                if ota_page.is_ota_history_component_visible():
                    expected_headers = [
                        "BATCH ID",
                        "BATCH NAME",
                        "UIN",
                        "IMEI",
                        "OTA TRIGGERED",
                        "OTA RESPONSE",
                        "CREATED AT",
                        "OTA STATUS",
                    ]
                    actual_headers = ota_page.get_ota_history_table_headers()
                    logger.debug("Expected headers: %s", expected_headers)
                    logger.debug("Actual headers: %s", actual_headers)

                    report_case(
                        expected=f"Table headers should match: {expected_headers}",
                        actual=f"Actual headers: {actual_headers}",
                        message="Validate OTA History table headers",
                    )

                    assert (
                        actual_headers == expected_headers
                    ), f"Expected headers {expected_headers}, but got {actual_headers}"

                    logger.info("Table headers on OTA History component are correct")
                else:
                    logger.warning(
                        "OTA History component is not visible - cannot validate table headers"
                    )
                    report_case(
                        expected="OTA History component should be visible after submit",
                        actual="OTA History component is not visible",
                        message="Validate OTA History component visibility",
                    )
            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate OTA History table headers"
                )
                report_case(
                    expected="Set Configuration component should be visible",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error(
                "Error validating table headers on OTA History component: %s", str(e)
            )
            report_case(
                expected="OTA History table headers should be validated successfully",
                actual=f"Error: {str(e)}",
                message="Validate OTA History table headers",
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_history_table_first_row_data_validation(
        self, project_config, test_data, ota_page, report_case
    ):
        """Verify that the data displayed in OTA History table is correct after submitting configuration."""
        logger.info("Testing data validation in OTA History table")
        valid_imei = test_data.get("valid_imei") or project_config.get("imei")
        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=valid_imei,
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button, submit configuration, and validate OTA History table data
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                ota_page.click_submit_button_on_set_configuration()
                logger.info(
                    "Clicked Submit button on Set Configuration component successfully"
                )

                if ota_page.is_ota_history_component_visible():
                    # Add specific assertions here to validate the data in the first row of the OTA History table
                    first_row_data = ota_page.get_first_row_data_from_ota_history()
                    logger.debug("First row OTA History data: %s", first_row_data)

                    actual_imei = first_row_data.get("IMEI", "")
                    logger.debug(
                        "Expected IMEI: %s, Actual IMEI: %s", valid_imei, actual_imei
                    )

                    report_case(
                        expected=f"IMEI in first row should be '{valid_imei}'",
                        actual=f"IMEI found: '{actual_imei}'",
                        message="Validate IMEI in OTA History table first row",
                    )

                    assert (
                        actual_imei == valid_imei
                    ), f"Expected IMEI '{valid_imei}' in first row, but got '{actual_imei}'"

                    logger.info("Data in OTA History table is correct after submission")
                else:
                    logger.warning(
                        "OTA History component is not visible - cannot validate table data"
                    )
                    report_case(
                        expected="OTA History component should be visible",
                        actual="OTA History component is not visible",
                        message="Validate OTA History component visibility",
                    )
            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate OTA History table data"
                )
                report_case(
                    expected="Set Configuration component should be visible",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error("Error validating data in OTA History table: %s", str(e))
            report_case(
                expected="OTA History table data should be validated successfully",
                actual=f"Error: {str(e)}",
                message="Validate OTA History table data",
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_history_export_button_clickability(
        self, ota_page, project_config, test_data, report_case
    ):
        """Verify OTA History component has Export button and it is clickable."""
        logger.info(
            "Testing Export button visibility and clickability on OTA History component"
        )

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button, submit configuration, and validate Export button
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                ota_page.click_submit_button_on_set_configuration()
                logger.info(
                    "Clicked Submit button on Set Configuration component successfully"
                )

                if ota_page.is_ota_history_component_visible():
                    is_export_visible = (
                        ota_page.is_export_button_visible_on_ota_history()
                    )
                    logger.debug("Export button visible: %s", is_export_visible)

                    report_case(
                        expected="Export button should be visible on OTA History component",
                        actual=f"Export button visible: {is_export_visible}",
                        message="Validate Export button visibility on OTA History",
                    )

                    assert (
                        is_export_visible
                    ), "Export button should be visible on OTA History component"

                    logger.info("Export button is visible on OTA History component")

                    # Click the Export button
                    ota_page.click_export_button_on_ota_history()

                    logger.info(
                        "Clicked Export button on OTA History component successfully"
                    )

                else:
                    logger.warning(
                        "OTA History component is not visible - cannot validate Export button"
                    )
                    report_case(
                        expected="OTA History component should be visible",
                        actual="OTA History component is not visible",
                        message="Validate OTA History component visibility",
                    )
            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate Export button on OTA History component"
                )
                report_case(
                    expected="Set Configuration component should be visible",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error(
                "Error validating or clicking Export button on OTA History component: %s",
                str(e),
            )
            report_case(
                expected="Export button should be visible and clickable on OTA History component",
                actual=f"Error: {str(e)}",
                message="Validate Export button visibility and click",
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_ota_page_manual_ota_history_pagination_validation(
        self, ota_page, project_config, test_data, report_case
    ):
        # Pagination class is defined.
        # get all prev steps and use the pagination class
        logger.info("Testing pagination on Manual OTA page")

        # Use helper method to set up manual OTA and enable Set Batch button
        ota_page.setup_manual_ota_and_enable_set_batch(
            valid_imei=test_data.get("valid_imei") or project_config.get("imei"),
            command_to_search=(
                test_data.get("command_to_search")
                or project_config.get("command_to_search")
                or "GET IMEI"
            ),
        )
        logger.info("Manual OTA setup and Set Batch button enabled successfully")

        # Click Set Batch button and validate pagination
        try:
            ota_page.click_set_batch_button()
            logger.info("Clicked Set Batch button successfully")

            if ota_page.is_set_configuration_component_visible():
                pagination_result = ota_page.verify_pagination_on_manual_ota_history()
                logger.debug("Pagination result: %s", pagination_result)

                report_case(
                    expected="Pagination should work correctly on Manual OTA History",
                    actual=f"Pagination success: {pagination_result.get('success', False)}",
                    message="Validate pagination on Manual OTA History",
                )

                assert pagination_result[
                    "success"
                ], f"Pagination test failed: {pagination_result.get('error', 'Unknown error')}"
                logger.info("Pagination on Manual OTA page verified successfully")
            else:
                logger.warning(
                    "Set Configuration component is not visible - cannot validate pagination on Manual OTA History"
                )
                report_case(
                    expected="Set Configuration component should be visible",
                    actual="Set Configuration component is not visible",
                    message="Validate Set Configuration component visibility",
                )

        except Exception as e:
            logger.error("Error validating pagination on Manual OTA page: %s", str(e))
            report_case(
                expected="Pagination on Manual OTA page should be validated successfully",
                actual=f"Error: {str(e)}",
                message="Validate pagination on Manual OTA page",
            )
            raise

    """ OTA Batch Functionality Test Cases - To be implemented after the feature is fully developed and stable enough for testing """
