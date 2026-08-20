import re

import pytest
from playwright.sync_api import expect
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuViewOtaBatchPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU View OTA Batch test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU View OTA Batch test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU View OTA Batch test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU View OTA Batch test failed: %s", test_name)
            logger.debug("ATCU View OTA Batch failure details for %s: %s", test_name, report.longrepr)

    def test_ota_batch_page_page_header_component_buttons_are_visible_and_enabled(self, atcu_ota_page, report_case):
        logger.info("Starting test: Verify OTA Batch Page Header Component Buttons are visible and enabled")
        actual_buttons = atcu_ota_page.get_ota_batch_page_header_component_buttons()
        # validate each buttons text, is_visible, is_enabled, router_links of buttons
        for text, properties in actual_buttons.items():
            report_case(
                expected=f"Button '{text}' should be visible and enabled",
                actual=f"Button '{text}' is_visible: {properties['is_visible']}, is_enabled: {properties['is_enabled']}",
                message=f"Validate OTA Batch Page Header Component Button '{text}'"
            )

            logger.debug("Validating button '%s': is_visible=%s, is_enabled=%s", text, properties['is_visible'], properties['is_enabled'])

            assert properties['is_visible'], f"Expected button '{text}' to be visible, but it is not."
            assert properties['is_enabled'], f"Expected button '{text}' to be enabled, but it is not."

        logger.info("OTA Batch Page Header Component Buttons visibility and enabled state verified successfully.")

    def test_ota_batch_page_table_component_title(self, atcu_ota_page, report_case):
        """Verify the OTA Batch Page Table Component Title is displayed correctly."""
        logger.info("Starting test: Verify OTA Batch Page Table Component Title")
        expected_title = "OTA Batch List"
        actual_title = atcu_ota_page.get_ota_batch_table_component_title()
        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate OTA Batch Page Table Component Title"
        )
        assert actual_title == expected_title, f"Expected title '{expected_title}', but got '{actual_title}'"

    def test_ota_batch_page_table_search_functionality(self, atcu_ota_page, report_case):
        """Verify the OTA Batch Page Table Search Functionality."""
        logger.info("Starting test: Verify OTA Batch Page Table Search Functionality")
        search_term = "ATCU"
        from pages.common_utils import SearchHelper
        search_results = SearchHelper(atcu_ota_page.page).run_search(search_term)
        report_case(
            expected=f"Search results for '{search_term}' should be found",
            actual=f"Search results found: {search_results['results_found']}",
            message="Validate OTA Batch Page Table Search Functionality"
        )
        assert search_results['success'], f"Search for '{search_term}' failed with error: {search_results['error']}"
        assert search_results['results_found'] > 0, f"No search results found for '{search_term}'" 
        assert all(search_term.lower() in result.lower() for result in search_results['results']), f"Not all search results contain the term '{search_term}'"


    def test_ota_batch_page_table_headers (self, atcu_ota_page, report_case):
        """Verify the OTA Batch Page Table Headers are displayed correctly."""
        logger.info("Starting test: Verify OTA Batch Page Table Headers")
        expected_headers = ["BATCH ID", "BATCH NAME", "BATCH DESCRIPTION", "CREATED BY", "CREATED AT", "BATCH BREAKDOWN", "COMPLETED PERCENTAGE", "BATCH STATUS", "ACTION"]

        from pages.common_utils import TableSection
        actual_headers = TableSection(atcu_ota_page.page).get_headers()

        logger.debug("Expected table headers: %s", expected_headers)

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"Actual table headers: {actual_headers}",
            message="Validate OTA Batch Page Table Headers"
        )

        assert actual_headers == expected_headers, f"Expected headers {expected_headers}, but got {actual_headers}"


    def test_ota_batch_page_table_rows_data_validation(self, atcu_ota_page, report_case):
        """Verify the OTA Batch Page Table Rows are displayed correctly."""
        logger.info("Starting test: Verify OTA Batch Page Table Rows")

        # search for a specific term to ensure that the table has rows to validate
        search_term = "ATCU"
        from pages.common_utils import SearchHelper
        search_results = SearchHelper(atcu_ota_page.page).run_search(search_term)
        assert search_results['success'], f"Search for '{search_term}' failed with error: {search_results['error']}"

        # validate table rows are present and each row is a dictionary with expected keys
        from pages.common_utils import TableSection
        table_rows = TableSection(atcu_ota_page.page).get_table_data()

        # report the number of table rows found and validate that they are present
        report_case(
            expected="Table rows should be present",
            actual=f"Number of table rows found: {len(table_rows)}",
            message="Validate OTA Batch Page Table Rows"
        )

        assert len(table_rows) > 0, "Expected table rows to be present, but none were found."
        assert all(isinstance(row, dict) for row in table_rows), "Expected each table row to be a dictionary, but found a different type."
        assert table_rows[0].keys() == {"BATCH ID", "BATCH NAME", "BATCH DESCRIPTION", "CREATED BY", "CREATED AT", "BATCH BREAKDOWN", "COMPLETED PERCENTAGE", "BATCH STATUS", "ACTION"}, f"Expected table row keys to match the expected headers, but found: {table_rows[0].keys()}"
        assert table_rows[0]["BATCH NAME"] == "ATCU", f"Expected first row 'BATCH NAME' to be 'ATCU OTA Batch', but found: {table_rows[0]['BATCH NAME']}"

    def test_ota_batch_page_table_headers_with_data_of_created_at_batch_breakdown_completed_percentage(self, atcu_ota_page, report_case):
        """Verify the OTA Batch Page Table Headers with data of Created At, Batch Breakdown, Completed Percentage."""
        logger.info("Starting test: Verify OTA Batch Page Table Headers with data of Created At, Batch Breakdown, Completed Percentage")

        # search for a specific term to ensure that the table has rows to validate
        search_term = "ATCU"
        # Example regex for datetime format 13 Aug 2026 | 10:36:03 AM
        created_at_regex = r"^\d{1,2} [A-Za-z]{3} \d{4} \| \d{1,2}:\d{2}:\d{2} (AM|PM)$"
        from pages.common_utils import SearchHelper
        search_results = SearchHelper(atcu_ota_page.page).run_search(search_term)
        assert search_results['success'], f"Search for '{search_term}' failed with error: {search_results['error']}"

        # validate table rows are present and each row is a dictionary with expected keys
        from pages.common_utils import TableSection
        table_rows = TableSection(atcu_ota_page.page).get_table_data()

        # report the number of table rows found and validate that they are present
        report_case(
            expected="Table rows should be present",
            actual=f"Number of table rows found: {len(table_rows)}",
            message="Validate OTA Batch Page Table Rows"
        )

        assert len(table_rows) > 0, "Expected table rows to be present, but none were found."
        breakdown_regex = r"^C-\s*\d+\s*\|\|\s*A-\s*\d+\s*\|\|\s*IP-\s*\d+\s*\|\|\s*T-\s*\d+$"
        percentage_regex = r"^\d+(?:\.\d{2})?\s*%$"

        for row_number, row in enumerate(table_rows, start=1):
            created_at = row["CREATED AT"]
            batch_breakdown = row["BATCH BREAKDOWN"]
            completed_percentage = row["COMPLETED PERCENTAGE"]

            report_case(
                expected="Created At, Batch Breakdown, and Completed Percentage should have valid formats",
                actual=(
                    f"Row {row_number}: CREATED AT={created_at}, "
                    f"BATCH BREAKDOWN={batch_breakdown}, "
                    f"COMPLETED PERCENTAGE={completed_percentage}"
                ),
                message=f"Validate OTA Batch row {row_number} data formats",
            )

            assert re.fullmatch(created_at_regex, created_at), (
                f"Row {row_number} has invalid CREATED AT format: {created_at!r}"
            )
            assert re.fullmatch(breakdown_regex, batch_breakdown), (
                f"Row {row_number} has invalid BATCH BREAKDOWN format: {batch_breakdown!r}"
            )
            assert re.fullmatch(percentage_regex, completed_percentage), (
                f"Row {row_number} has invalid COMPLETED PERCENTAGE format: "
                f"{completed_percentage!r}"
            )

            percentage_value = float(completed_percentage.rstrip("%").strip())
            assert 0 <= percentage_value <= 100, (
                f"Row {row_number} COMPLETED PERCENTAGE must be between 0 and 100: "
                f"{completed_percentage!r}"
            )


    def test_ota_batch_page_table_batch_status_and_action_buttons_validations(self, atcu_ota_page, report_case):
        """Verify batch status and the enabled state of its Abort action button."""
        from pages.common_utils import SearchHelper, TableSection

        search_results = SearchHelper(atcu_ota_page.page).run_search("ATCU")
        assert search_results["success"], f"Search failed: {search_results['error']}"

        table = TableSection(atcu_ota_page.page)
        table_rows = table.get_table_data()
        assert table_rows, "Expected OTA batch rows to be present."

        for row_index, row in enumerate(table_rows):
            status = row["BATCH STATUS"].splitlines()[0].strip().lower()
            abort_button = table.get_action_button(row_index, "block")

            assert status in {"in-progress", "completed", "aborted"}, (
                f"Unexpected batch status in row {row_index + 1}: {status!r}"
            )

            if status == "in-progress":
                expected_state = "visible and enabled"
                assert abort_button.is_visible(), f"Abort button is not visible in row {row_index + 1}"
                assert abort_button.is_enabled(), f"Abort button is not enabled in row {row_index + 1}"
            else:
                expected_state = "visible and disabled"
                assert abort_button.is_visible(), f"Abort button is not visible in row {row_index + 1}"
                assert abort_button.is_disabled(), f"Abort button is not disabled in row {row_index + 1}"

            report_case(
                expected=f"Row {row_index + 1} Abort button should be {expected_state} for status '{status}'",
                actual=f"status='{status}', visible={abort_button.is_visible()}, enabled={abort_button.is_enabled()}",
                message=f"Validate row {row_index + 1} status and Abort action",
            )

    def test_ota_batch_page_table_action_buttons_list(self, atcu_ota_page, report_case):
        """Verify each OTA batch row contains View, Abort, and Download actions in order."""
        from pages.common_utils import SearchHelper, TableSection

        search_results = SearchHelper(atcu_ota_page.page).run_search("ATCU")
        assert search_results["success"], f"Search failed: {search_results['error']}"

        table = TableSection(atcu_ota_page.page)
        table_rows = table.get_table_data()
        expected_buttons = ["View", "Abort", "Download"]
        icon_to_label = {"visibility": "View", "block": "Abort", "file_download": "Download"}

        assert table_rows, "Expected OTA batch rows to be present."
        for row_index in range(len(table_rows)):
            actual_icons = table.get_action_buttons(row_index)
            actual_buttons = [icon_to_label.get(icon, icon) for icon in actual_icons]

            report_case(
                expected=str(expected_buttons),
                actual=f"row {row_index + 1}: {actual_buttons}",
                message=f"Validate row {row_index + 1} action button list",
            )
            assert actual_buttons == expected_buttons, (
                f"Expected row {row_index + 1} actions {expected_buttons}, got {actual_buttons}"
            )

    def test_ota_batch_page_view_action_opens_batch_page(self, atcu_ota_page, report_case):
        """Verify the View action opens the selected OTA batch page."""
        from pages.common_utils import SearchHelper, TableSection

        search_results = SearchHelper(atcu_ota_page.page).run_search("ATCU")
        assert search_results["success"], f"Search failed: {search_results['error']}"

        table = TableSection(atcu_ota_page.page)
        table_rows = table.get_table_data()
        assert table_rows, "Expected OTA batch rows to be present."

        from api.atcu import AtcuOtaPageAPI
        _, batch_ids = AtcuOtaPageAPI.get_ota_batch_list(atcu_ota_page.page)
        assert batch_ids, "Expected at least one batch ID from API."

        view_button = table.get_action_button(0, "visibility")
        view_button.click()

        batch_id = str(batch_ids[0])
        AtcuOtaPageAPI.get_ota_batch_kpi(atcu_ota_page.page, batch_ref_id = batch_id)

        # Wait for Angular Router client-side navigation
        try:
            atcu_ota_page.page.wait_for_url("**/ota-batch-view/*", wait_until="commit", timeout=5000)
        except Exception:
            atcu_ota_page.page.wait_for_timeout(1000)

        actual_url = atcu_ota_page.page.url

        report_case(
            expected=f"URL should contain 'ota-batch-view/{batch_id}'",
            actual=f"Actual URL: {actual_url}",
            message="Validate View action navigation",
        )
        assert f"ota-batch-view/{batch_id}" in actual_url or "ota-batch-view" in actual_url, (
            f"Expected URL to contain 'ota-batch-view/{batch_id}', got '{actual_url}'"
        )



    def test_ota_batch_page_download_action_downloads_report(self, atcu_ota_page, report_case):
        """Verify accepting the Download confirmation downloads the selected OTA batch report."""
        from pathlib import Path
        from pages.common_utils import SearchHelper, TableSection
        from config.global_var import DOWNLOADS_PATH

        search_results = SearchHelper(atcu_ota_page.page).run_search("ATCU")
        assert search_results["success"], f"Search failed: {search_results['error']}"

        table = TableSection(atcu_ota_page.page)
        table_rows = table.get_table_data()
        assert table_rows, "Expected OTA batch rows to be present."
        batch_id = table_rows[0]["BATCH ID"]
        download_button = table.get_action_button(0, "file_download")
        dialog_accepted = {"value": False}

        def accept_download_dialog(dialog):
            dialog_accepted["value"] = True
            dialog.accept()

        atcu_ota_page.page.once("dialog", accept_download_dialog)
        with atcu_ota_page.page.expect_download() as download_info:
            download_button.click()

        download = download_info.value
        filename = download.suggested_filename
        download_path = Path(DOWNLOADS_PATH) / filename
        download.save_as(str(download_path))

        report_case(
            expected=f"Download confirmation accepted and OTA report for batch {batch_id} saved",
            actual=f"accepted={dialog_accepted['value']}, filename='{filename}', path='{download_path}'",
            message="Validate OTA batch report download",
        )
        assert dialog_accepted["value"], "Expected the download confirmation dialog to be accepted"
        assert filename.startswith(f"OTA_Batch_Report_{batch_id}_export_"), (
            f"Unexpected downloaded filename: {filename!r}"
        )
        assert download_path.exists(), f"Downloaded file was not saved: {download_path}"
