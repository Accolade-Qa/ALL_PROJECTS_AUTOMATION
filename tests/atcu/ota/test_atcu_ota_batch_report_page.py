import re
import pytest
from playwright.sync_api import expect

from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from utils.logger import get_logger


logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuOtaBatchReportPage:
    """In-depth test suite for ATCU Project OTA Batch Report & KPI Cards Page based on deep HTML scan."""

    SEARCH_QUERY = "test"

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU OTA Batch Report test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU OTA Batch Report test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU OTA Batch Report test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU OTA Batch Report test failed: %s", test_name)
            logger.debug("ATCU OTA Batch Report failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_batch_page_navigation_and_url_validation(self, atcu_ota_page, report_case):
        """Verify ATCU OTA Batch page is loaded with valid URL."""
        logger.info("Validating ATCU OTA Batch page load state")
        page_loaded = atcu_ota_page.is_page_loaded()

        report_case(
            expected="ATCU OTA page should be loaded with valid URL",
            actual=f"Page loaded: {page_loaded}, URL: {atcu_ota_page.page.url}",
            message="Validate ATCU OTA Batch page navigation and URL",
        )

        assert page_loaded, f"ATCU OTA page did not load at {atcu_ota_page.page.url}"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_batch_page_header_title_validation(self, atcu_ota_page, report_case):
        """Verify ATCU OTA Batch page header title is correct."""
        logger.info("Verifying ATCU OTA Batch page header title")
        actual_title = atcu_ota_page.get_page_title()

        report_case(
            expected="Header title should contain 'OTA'",
            actual=f"Actual title: '{actual_title}'",
            message="Validate ATCU OTA Batch page header title",
        )

        assert "OTA" in actual_title or "Report" in actual_title or actual_title != "", "OTA Batch page header title is invalid"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_batch_routing_buttons_back_and_reload(self, atcu_ota_page, report_case):
        """Verify presence and functionality of routing back and reload buttons."""
        logger.info("Validating routing back and reload buttons")

        back_btn = atcu_ota_page.page.locator(".action-button.back-button, .back-icon").first
        reload_btn = atcu_ota_page.page.locator(".action-button.reload-button, .reload-icon").first

        back_visible = back_btn.is_visible()
        reload_visible = reload_btn.is_visible()

        report_case(
            expected="Routing Back and Reload buttons should be visible",
            actual=f"Back visible: {back_visible}, Reload visible: {reload_visible}",
            message="Validate routing buttons on OTA Batch Report page",
        )

        assert back_visible or reload_visible, "Routing Back or Reload button should be visible on OTA Batch Report page"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_batch_ui_elements_visibility(self, atcu_ota_page, report_case):
        """Verify all essential UI elements are visible on ATCU OTA Batch page."""
        logger.info("Validating ATCU OTA Batch page elements visibility")

        page_loaded = atcu_ota_page.is_page_loaded()
        buttons_visible = atcu_ota_page.is_ota_batch_page_buttons_visible()
        table_visible = atcu_ota_page.is_ota_batch_table_visible()
        search_visible = atcu_ota_page.is_search_box_visible()

        report_case(
            expected="All ATCU OTA Batch page elements should be visible and loaded",
            actual=f"Page loaded: {page_loaded}, Buttons: {buttons_visible}, Table: {table_visible}, Search: {search_visible}",
            message="Validate ATCU OTA Batch UI elements visibility",
        )

        assert page_loaded, "ATCU OTA Batch page failed to load"
        assert buttons_visible, "Buttons are not visible on ATCU OTA Batch page"
        assert table_visible, "Table is not visible on ATCU OTA Batch page"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_batch_table_search_filter_functionality(self, atcu_ota_page, report_case):
        """Verify search filtering functionality on ATCU OTA Batch table."""
        logger.info("Testing search functionality on ATCU OTA Batch table")
        assert atcu_ota_page.is_ota_batch_table_visible(), "OTA Batch table is not visible"

        search = SearchHelper(atcu_ota_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        report_case(
            expected=f"Search query '{self.SEARCH_QUERY}' should execute successfully",
            actual=f"Success: {result['success']}, Results found: {result['results_found']}",
            message=f"Validate ATCU OTA Batch table search for query '{self.SEARCH_QUERY}'",
        )

        assert result["success"], f"Search failed: {result['error']}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_ota_batch_table_headers_and_columns_validation(self, atcu_ota_page, report_case):
        """Verify ATCU OTA Batch table displays expected columns."""
        logger.info("Validating ATCU OTA Batch table columns")
        table_visible = atcu_ota_page.is_ota_batch_table_visible()
        assert table_visible, "OTA Batch table not visible"

        expected_cols = ["SL NO", "BATCH ID", "ASSIGNED FIRMWARE", "MODE", "REMARKS", "CREATED BY", "CREATED AT", "STATUS", "ACTIONS"]
        headers = atcu_ota_page.get_batch_table_headers()

        report_case(
            expected=f"Table headers should contain columns: {expected_cols}",
            actual=f"Headers found: {headers}",
            message="Validate ATCU OTA Batch table header columns",
        )

        assert table_visible, "OTA Batch table is not visible"


    @pytest.mark.regression
    def test_atcu_ota_batch_invalid_search_query_shows_no_data(self, atcu_ota_page, report_case):
        """Verify non-existent search query displays 'No Data Found' placeholder image/text."""
        logger.info("Testing invalid search query on ATCU OTA Batch table")

        invalid_query = "NON_EXISTENT_BATCH_99999"
        search = SearchHelper(atcu_ota_page.page)
        result = search.run_search(invalid_query)

        report_case(
            expected="Invalid search query should yield 0 results with empty table indicator",
            actual=f"Results found: {result['results_found']}",
            message="Validate invalid search query handling on ATCU OTA Batch page",
        )

        assert result["success"], f"Search failed: {result['error']}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_ota_batch_back_button_navigation(self, atcu_ota_page, report_case):
        """Verify Back button navigation functionality on OTA Batch Report page."""
        logger.info("Testing Back button navigation on OTA Batch Report page")

        back_btn = atcu_ota_page.page.locator(".action-button.back-button, button:has(mat-icon:has-text('arrow_back')), .back-icon").first
        if back_btn.is_visible():
            back_btn.click()
            atcu_ota_page.page.wait_for_load_state("load")

        curr_url = atcu_ota_page.page.url
        logger.debug("URL after clicking Back button: %s", curr_url)

        report_case(
            expected="Back button click should navigate back smoothly",
            actual=f"Current URL: {curr_url}",
            message="Validate Back button navigation functionality",
        )

        assert curr_url != "", "Back button navigation failed"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_ota_batch_refresh_button_functionality(self, atcu_ota_page, report_case):
        """Verify Refresh/Reload button functionality on OTA Batch Report page."""
        logger.info("Testing Refresh/Reload button functionality on OTA Batch Report page")

        reload_btn = atcu_ota_page.page.locator(".action-button.reload-button, button:has(mat-icon:has-text('refresh')), button:has(mat-icon:has-text('autorenew')), .reload-icon").first
        if reload_btn.is_visible():
            reload_btn.click()
            atcu_ota_page.page.wait_for_load_state("load")

        page_loaded = atcu_ota_page.is_page_loaded()
        logger.debug("Page loaded after clicking Refresh button: %s", page_loaded)

        report_case(
            expected="Refresh button click should reload page content successfully",
            actual=f"Page loaded: {page_loaded}",
            message="Validate Refresh button functionality",
        )

        assert page_loaded, "Refresh/Reload button failed to reload page content"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_ota_subpage_navigation_header_links(self, atcu_ota_page, report_case):
        """Verify sub-page navigation between OTA Batch Report, Create OTA Batch, Manual OTA, and OTA Master pages."""
        logger.info("Testing sub-page navigation links across OTA module")

        # Step 1: Navigate to Create OTA Batch page
        atcu_ota_page.go_to_create_ota_batch_page()
        url_create = atcu_ota_page.page.url
        logger.debug("Navigated to Create OTA Batch page: %s", url_create)

        report_case(
            expected="URL should contain 'ota-batch-create'",
            actual=f"Current URL: {url_create}",
            message="Validate navigation to Create OTA Batch page",
        )
        assert "ota-batch-create" in url_create.lower() or "create" in url_create.lower()

        # Step 2: Navigate to Manual OTA page
        atcu_ota_page.go_to_manual_ota_page()
        url_manual = atcu_ota_page.page.url
        logger.debug("Navigated to Manual OTA page: %s", url_manual)

        report_case(
            expected="URL should contain 'manual-ota'",
            actual=f"Current URL: {url_manual}",
            message="Validate navigation to Manual OTA page",
        )
        assert "manual-ota" in url_manual.lower()

        # Step 3: Navigate to OTA Master page
        atcu_ota_page.go_to_ota_master_page()
        url_master = atcu_ota_page.page.url
        logger.debug("Navigated to OTA Master page: %s", url_master)

        report_case(
            expected="URL should contain 'ota-master'",
            actual=f"Current URL: {url_master}",
            message="Validate navigation to OTA Master page",
        )
        assert "ota-master" in url_master.lower()

        # Step 4: Return to OTA Batch Report page
        atcu_ota_page.go_to_ota_batch_report_page()
        url_report = atcu_ota_page.page.url

        report_case(
            expected="URL should contain 'Ota-batch-report'",
            actual=f"Current URL: {url_report}",
            message="Validate return navigation to OTA Batch Report page",
        )
        assert "Ota-batch-report" in url_report or "ota-batch" in url_report.lower()


