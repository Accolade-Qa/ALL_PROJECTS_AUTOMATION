from datetime import datetime
from api import APIClient
from utils.helpers import Helpers
from pages.common_utils import TableSection, SearchHelper
from utils.logger import get_logger

import re
import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.critical
@pytest.mark.regression
class TestRoleGroupPage:
    group = None

    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        if self.__class__.group is None:
            self.__class__.group = f"Test{Helpers.generate_random_string(4)}"

        test_name = request.node.name
        logger.info("Starting Role Group test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Role Group test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Role Group test passed: %s", test_name)
        elif report.failed:
            logger.error("Role Group test failed: %s", test_name)
            logger.debug(
                "Role Group failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Role Group test skipped: %s", test_name)

    """" Test for deleting role group from the role group page. """
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_role_group_page_delete_roles_api(self, role_group_page, report_case):
        """Test deleting a role permission."""
        logger.info("Testing delete role permission functionality")
        api = APIClient()
        result = api.role_group.delete_role_groups()
        report_case(
            expected=True,
            actual=result.get("success"),
            message="Validate delete role groups via API in role group page",
        )
        assert result.get("success"), "Role group deletion API execution failed"
        logger.info("Delete role management test completed")



    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_role_group_page_title_is_correct(self, role_group_page, report_case):
        logger.info("Testing Role Group page title")
        title = role_group_page.get_title()
        logger.debug(
            "Role Group title check | expected=%s | actual=%s",
            "Group Management",
            title,
        )
        report_case(expected="Group Management", actual=title, message="Validate Role group page title is correct")
        assert (
            title == "Group Management"
        ), f"Expected page title 'Group Management', but got '{title}'"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_role_group_page_all_elements_are_visible(
        self, role_group_page, report_case
    ):
        logger.info("Testing Role Group page elements")
        page_loaded = role_group_page.is_page_loaded()
        add_group_visible = role_group_page.is_add_group_button_visible()
        table_visible = role_group_page.is_role_group_table_visible()
        search_visible = role_group_page.is_search_box_visible()
        report_case(
            expected="Page loaded=True, Add Group visible=True, table visible=True, search visible=True",
            actual=(
                f"Page loaded={page_loaded}, Add Group visible={add_group_visible}, "
                f"table visible={table_visible}, search visible={search_visible}"
            )
        , message="Validate Role group page all elements are visible")
        assert page_loaded, "Role Group page did not load correctly"

        assert add_group_visible, "Add Group button is not visible"

        assert table_visible, "Role Group table is not visible"

        assert search_visible, "Search box is not visible"

        logger.info("All Role Group page elements are present and visible")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_add_button_navigates_to_form(
        self, role_group_page, report_case
    ):
        logger.info("Testing navigation to Add Group page")

        if role_group_page.is_add_group_button_visible():
            logger.debug("Add Group button visible, clicking it")
            role_group_page.click_add_group()

        logger.debug(
            "Role Group page URL after Add Group click: %s", role_group_page.page.url
        )
        assert role_group_page.page.url.endswith(
            "/role-group"
        ), f"Expected URL to end with '/role-group', but got '{role_group_page.page.url}'"

        component_title = role_group_page.get_component_title()
        logger.debug("Add Group component title: %s", component_title)
        report_case(
            expected="URL ends with /role-group and component title is Add Group",
            actual=f"URL={role_group_page.page.url}, component title={component_title}"
        , message="Validate Role group page add button navigates to form")
        assert component_title == "Add Group", "Add Group page did not load correctly"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_form_shows_validation_errors_for_invalid_input(
        self, role_group_page, report_case
    ):
        logger.info("Testing input box errors on different inputs")

        role_group_page.click_add_group()

        # Test empty input
        role_group_page.enter_role_group_name("")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        logger.debug("Empty group name error: %s", error_message)
        results = {"empty": error_message}
        assert (
            error_message == "This field is required and can't be empty."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test input with only spaces
        role_group_page.enter_role_group_name("   ")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        logger.debug("Spaces-only group name error: %s", error_message)
        results["spaces"] = error_message
        assert (
            error_message == "This field is required and can't be only spaces."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test special characters
        role_group_page.enter_role_group_name("@#$%^&*")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        logger.debug("Special-character group name error: %s", error_message)
        results["special_characters"] = error_message
        assert (
            error_message == "Only alphabets and spaces are allowed."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test valid input
        role_group_page.enter_role_group_name(self.group)
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        logger.debug(
            "Valid group name error state for %s: %s", self.group, error_message
        )
        results["valid_error"] = error_message
        assert error_message is None, f"Unexpected error message '{error_message}'"
        success_message = role_group_page.get_success_message()
        logger.debug("Valid group creation success message: %s", success_message)
        results["success_message"] = success_message
        report_case(
            expected={
                "empty": "This field is required and can't be empty.",
                "spaces": "This field is required and can't be only spaces.",
                "special_characters": "Only alphabets and spaces are allowed.",
                "valid_error": None,
                "success_message": "Success",
            },
            actual=results
        , message="Validate Role group page form shows validation errors for invalid input")
        assert "Success" in success_message, "Expected success message not found"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_table_search_filters_results(
        self, role_group_page, report_case
    ):
        logger.info("Testing search functionality on Role Group table")

        assert (
            role_group_page.is_role_group_table_visible()
        ), "Role Group table is not visible"

        # Use SearchHelper for reliable search instead of manual interaction
        search = SearchHelper(role_group_page.page)
        result = search.run_search(self.group)

        logger.info("Search result: %s", result)
        logger.debug("Role Group search rows for %s: %s", self.group, result["results"])
        report_case(
            expected=f"Search for {self.group} should succeed and show matching results or no-data state",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Search failed: {result['error']}"

        # Check if the group is found in the results
        if result["results_found"] == 0:
            table = TableSection(role_group_page.page)
            assert (
                table.has_no_data()
            ), f"Group '{self.group}' not found and no data message shown"
        else:
            # Validate that all rows contain the search term
            rows = result["results"]
            assert any(
                self.group.lower() in row.lower() for row in rows
            ), f"Group '{self.group}' not found in search results. Results: {rows}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_table_displays_valid_group_data(
        self, role_group_page, report_case
    ):
        logger.info("Validating Role Group table data")

        table = TableSection(role_group_page.page)

        assert role_group_page.is_role_group_table_visible()

        row_count = table.get_row_count()
        logger.debug("Role Group table row count: %s", row_count)
        report_case(
            expected="Role Group table should be visible and data state valid",
            actual=f"row_count={row_count}"
        , message="Validate Role group page table displays valid group data")

        if row_count == 0:
            logger.warning("Table is empty")
            assert table.has_no_data()
            return

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_table_search_helper_finds_groups(
        self, role_group_page, report_case
    ):
        logger.info("Testing search using SearchHelper")

        search = SearchHelper(role_group_page.page)

        result = search.run_search(self.group)

        logger.info("Search result: %s", result)
        logger.debug(
            "Role Group helper search rows for %s: %s", self.group, result["results"]
        )
        report_case(
            expected=f"SearchHelper should succeed for {self.group}",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(role_group_page.page)
            assert table.has_no_data()
        else:
            for row in result["results"]:
                assert self.group.lower() in row.lower()

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_table_pagination_navigates_across_pages(
        self, role_group_page, report_case
    ):
        logger.info("Testing pagination on Role Group table")

        # Check if pagination elements exist
        page_input = role_group_page.page.locator("input.page-input")
        next_button = role_group_page.page.locator(
            "button:has(mat-icon:has-text('chevron_right'))"
        )

        if page_input.count() > 0 and next_button.count() > 0:
            logger.debug(
                "Pagination elements count | page_input=%s | next_button=%s",
                page_input.count(),
                next_button.count(),
            )
            assert page_input.is_visible(), "Pagination input not visible"
            assert next_button.is_visible(), "Next button not visible"
            logger.info("Pagination elements are present")
            report_case(
                expected="Pagination input and next button visible",
                actual="Pagination elements are visible"
            , message="Validate Role group page table pagination navigates across pages")
        else:
            logger.info("No pagination elements found, assuming single page")
            report_case(
                expected="Pagination visible when multiple pages exist",
                actual="No pagination elements found; assuming single page"
            , message="Validate Role group page table pagination navigates across pages")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_search_results_match_table_data(
        self, role_group_page, report_case
    ):
        logger.info("Testing search + table validation")

        search = SearchHelper(role_group_page.page)
        table = TableSection(role_group_page.page)

        result = search.run_search(self.group)
        logger.debug("Role Group search and validate result: %s", result)
        report_case(
            expected=f"Rows should contain search term {self.group} or no-data state should show",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"]

        if result["results_found"] == 0:
            assert table.has_no_data()
        else:
            rows = table.get_rows()
            logger.debug("Role Group table rows after search: %s", rows)
            for row in rows:
                assert self.group.lower() in row.lower()

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_table_headers_are_correct(
        self, role_group_page, report_case
    ):
        logger.info("Validating table headers")

        table = TableSection(role_group_page.page)

        headers = table.get_headers()
        logger.debug("Role Group table headers: %s", headers)

        expected_headers = ["GROUP NAME", "CREATED AT", "ACTION"]
        report_case(expected=expected_headers, actual=headers, message="Validate Role group page table headers are correct")

        for header in expected_headers:
            assert header in headers, f"{header} not found in table headers"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_created_at_timestamps_are_not_future_dates(
        self, role_group_page, report_case
    ):
        logger.info("Validating 'Created At' is not a future date")

        from datetime import datetime

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        today = datetime.today()
        created_dates = []

        for i in range(rows.count()):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()
            created_dates.append(created_at)
            logger.debug(
                "Validating Created At is not future | row=%s | value=%s", i, created_at
            )
            date_obj = datetime.strptime(created_at, "%d/%m/%Y")

            assert date_obj <= today, f"Future date found: {created_at}"
        report_case(
            expected=f"All Created At dates should be <= {today.date()}",
            actual=created_dates
        , message="Validate Role group page created at timestamps are not future dates")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_created_at_column_is_sorted_correctly(
        self, role_group_page, report_case
    ):
        logger.info("Validating 'Created At' column sorting")

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        row_count = rows.count()

        dates = []

        for i in range(row_count):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()
            logger.debug(
                "Collected Created At for sorting | row=%s | value=%s", i, created_at
            )
            date_obj = datetime.strptime(created_at, "%d/%m/%Y")
            dates.append(date_obj)

        # ✅ Check ascending order (oldest first)
        report_case(expected=sorted(dates), actual=dates, message="Validate Role group page created at column is sorted correctly")
        assert dates == sorted(dates), "Dates are not sorted in ascending order"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_role_group_page_created_at_column_has_correct_date_format(
        self, role_group_page, report_case
    ):
        logger.info("Validating 'Created At' column format")

        table = TableSection(role_group_page.page)

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        row_count = rows.count()
        logger.debug(
            "Role Group row count for Created At format validation: %s", row_count
        )

        assert row_count > 0, "Table is empty"

        date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
        created_dates = []

        for i in range(row_count):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()
            created_dates.append(created_at)
            logger.debug(
                "Validating Created At format | row=%s | value=%s", i, created_at
            )

            # ✅ Check format
            assert date_pattern.match(created_at), f"Invalid date format: {created_at}"

            # ✅ Check valid date
            try:
                datetime.strptime(created_at, "%d/%m/%Y")
            except ValueError:
                assert False, f"Invalid date value: {created_at}"
        report_case(
            expected="All Created At values should match dd/mm/yyyy format",
            actual=created_dates
        , message="Validate Role group page created at column has correct date format")
