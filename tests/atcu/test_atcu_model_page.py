import time
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestModelPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Model page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Model page test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("ATCU Model page test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Model page test failed: %s", test_name)
            logger.debug(
                "ATCU Model page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Model page test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_page_loaded(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating ATCU Device Model page load")
        is_loaded = atcu_model_page.is_page_loaded()

        report_case(
            expected="ATCU Device Model page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Device Model page loaded",
        )
        assert is_loaded, "ATCU Device Model page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_page_title(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating ATCU Device Model page title")
        title = atcu_model_page.get_title()

        report_case(
            expected="Page title should be 'Device Models'",
            actual=f"title='{title}'",
            message="Validate ATCU Device Model page title",
        )
        assert title == "Device Models", f"Page title is incorrect: '{title}'"

    # 3. Test component header title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_component_header(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating ATCU Device Model component header title")
        comp_title = atcu_model_page.get_component_title()

        report_case(
            expected="Component header title should be 'Device Models List'",
            actual=f"comp_title='{comp_title}'",
            message="Validate ATCU Device Model component header title",
        )
        assert (
            comp_title == "Device Models List"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_table_headers(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Device Models table headers")
        headers = atcu_model_page.get_table_headers()
        expected_headers = ["MODEL NAME", "MODEL CODE", "HW VERSION", "ACTION"]

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"headers={headers}",
            message="Validate Device Models table headers",
        )
        assert (
            headers == expected_headers
        ), f"Device Models table headers mismatched: {headers}"

    # 5. Test sample data rows
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_sample_data_rows(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating first data row in Device Models table")
        first_row = atcu_model_page.get_first_row_data()

        report_case(
            expected="Table should contain valid data rows with MODEL NAME, MODEL CODE, and HW VERSION",
            actual=f"first_row={first_row}",
            message="Validate Device Models sample row data",
        )
        assert first_row, "Device Models table has no data rows"
        assert "MODEL NAME" in first_row
        assert "MODEL CODE" in first_row
        assert "HW VERSION" in first_row

    # 6. Test search by MODEL NAME (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_search_by_name(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating positive search by MODEL NAME")
        search_term = "AEPL052300"
        atcu_model_page.search_model_list(search_term)

        is_present = atcu_model_page.is_model_present_in_table(search_term)
        report_case(
            expected=f"Search for MODEL NAME '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by MODEL NAME",
        )
        assert is_present, f"Search result for MODEL NAME '{search_term}' not found in table"

    # 7. Test search by MODEL CODE (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_search_by_code(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating positive search by MODEL CODE")
        search_term = "AEPL052600"
        atcu_model_page.search_model_list(search_term)

        is_present = atcu_model_page.is_model_present_in_table(search_term)
        report_case(
            expected=f"Search for MODEL CODE '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by MODEL CODE",
        )
        assert is_present, f"Search result for MODEL CODE '{search_term}' not found in table"

    # 8. Test search by HW Version (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_search_by_hw_version(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating positive search by HW Version")
        search_term = "AEPL051401"
        atcu_model_page.search_model_list(search_term)

        is_present = atcu_model_page.is_model_present_in_table(search_term)
        report_case(
            expected=f"Search for HW Version '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by HW Version",
        )
        assert is_present, f"Search result for HW Version '{search_term}' not found in table"

    # 9. Test search clear query (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_search_clear_query(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating search input clearing restores full table results")
        atcu_model_page.search_model_list("AEPL052300")
        atcu_model_page.clear_search_input()

        rows = atcu_model_page.get_table_rows()
        report_case(
            expected="Clearing search query should restore full table data rows",
            actual=f"rows_count={len(rows)}",
            message="Validate search clear query",
        )
        assert len(rows) >= 1, "Clearing search failed to restore data rows"


    # 10. Test search non-existent term (Negative Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_search_non_existent_term(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating negative search with non-existent search term")
        invalid_term = "NON_EXISTENT_MODEL_99999"
        atcu_model_page.search_model_list(invalid_term)

        is_present = atcu_model_page.is_model_present_in_table(invalid_term, timeout=3000)
        report_case(
            expected=f"Searching non-existent term '{invalid_term}' should yield no matching rows",
            actual=f"is_present={is_present}",
            message="Validate negative search for non-existent term",
        )
        assert not is_present, f"Unexpectedly found matching row for non-existent term '{invalid_term}'"

    # 11. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_reload_button_click(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Device Models page")
        atcu_model_page.click_reload_button()
        is_loaded = atcu_model_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 12. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_back_button_click(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Back button click on Device Models page")
        atcu_model_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 13. Test pagination visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_pagination_visibility(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating pagination container visibility")
        is_pag_visible = atcu_model_page.is_pagination_visible()

        report_case(
            expected="Pagination container should be visible on Device Models table",
            actual=f"is_pag_visible={is_pag_visible}",
            message="Validate pagination container visibility",
        )
        assert is_pag_visible, "Pagination container is not visible"

    # 14. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_rows_per_page(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown selection")
        initial_rows = atcu_model_page.get_selected_rows_per_page()
        atcu_model_page.select_rows_per_page("25")
        updated_rows = atcu_model_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert updated_rows == "25", f"Expected updated rows per page '25', got '{updated_rows}'"

    # 15. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_pagination_navigation(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on Device Models page")
        pag_result = atcu_model_page.validate_pagination()

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate pagination navigation",
        )
        assert (
            pag_result["success"]
        ), f"Pagination validation failed: {pag_result.get('error')}"

    # 16. Test navigation to Add Device Model details page
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_navigate_to_add_device_model(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating navigation to Add Device Model sub-page")
        assert atcu_model_page.is_add_device_model_button_visible()
        atcu_model_page.click_add_device_model_button()

        is_sub_loaded = atcu_model_page.is_details_page_loaded()
        report_case(
            expected="Clicking 'Add Device Model' button should navigate to Device Model Details sub-page",
            actual=f"is_sub_loaded={is_sub_loaded}",
            message="Validate navigation to Add Device Model page",
        )
        assert is_sub_loaded, "Device Model Details sub-page failed to load"

    # 17. Test Add/Update Device Model page title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_add_details_page_title(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Add/Update Device Model page title")
        atcu_model_page.click_add_device_model_button()
        title = atcu_model_page.get_details_page_title()
        comp_title = atcu_model_page.get_details_component_title()

        report_case(
            expected="Page title should be 'Add/Update Device Model' and component title should be 'Create Device Model'",
            actual=f"title='{title}', comp_title='{comp_title}'",
            message="Validate Add/Update Device Model page titles",
        )
        assert title == "Add/Update Device Model", f"Page title mismatched: '{title}'"
        assert comp_title == "Create Device Model", f"Component title mismatched: '{comp_title}'"

    # 18. Test Add Form initial state & Submit button disabled (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_create_form_initial_disabled_state(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating initial disabled state of Submit button when form is empty")
        atcu_model_page.click_add_device_model_button()

        is_submit_enabled = atcu_model_page.is_submit_button_enabled()
        report_case(
            expected="Submit button should be disabled initially when all required inputs are empty",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate initial disabled state of Create Model form",
        )
        assert not is_submit_enabled, "Submit button should be disabled when form is empty"

    # 19. Test Add Form partial fill keeps Submit button disabled (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_create_form_partial_fill_disabled(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Submit button remains disabled when form is only partially filled")
        atcu_model_page.click_add_device_model_button()
        atcu_model_page.fill_create_model_form(model_name="PartialName", model_code=None, hw_version=None)

        is_submit_enabled = atcu_model_page.is_submit_button_enabled()
        report_case(
            expected="Submit button should remain disabled when required fields (MODEL CODE, HW Version) are missing",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate partial form fill disabled state",
        )
        assert not is_submit_enabled, "Submit button should remain disabled when fields are missing"

    # 20. Test Add Form valid fill enables Submit button (Positive Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_create_form_valid_fill_enablement(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Submit button enablement when all required fields are valid")
        atcu_model_page.click_add_device_model_button()
        atcu_model_page.fill_create_model_form(
            model_name="ValidModelName",
            model_code="ValidModelCode",
            hw_version="HW_V1.0",
        )

        is_submit_enabled = atcu_model_page.is_submit_button_enabled()
        values = atcu_model_page.get_form_input_values()

        report_case(
            expected="Submit button should be enabled after entering MODEL NAME, MODEL CODE, and HW Version",
            actual=f"is_submit_enabled={is_submit_enabled}, values={values}",
            message="Validate valid form fill enablement",
        )
        assert is_submit_enabled, "Submit button should be enabled when form is fully filled"
        assert values.get("modelName") == "ValidModelName"
        assert values.get("modelCode") == "ValidModelCode"
        assert values.get("hwVersion") == "HW_V1.0"

    # 21. Test View action button for existing model row
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_view_button_action(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating View action button for an existing model row")
        sample_model = "AEPL052300"
        assert atcu_model_page.is_model_present_in_table(sample_model)

        is_view_vis = atcu_model_page.is_view_button_visible_for_row(sample_model)
        atcu_model_page.click_view_button_for_row(sample_model)
        is_details_loaded = atcu_model_page.is_details_page_loaded()

        report_case(
            expected="Clicking View action button should navigate to Device Model Details page",
            actual=f"is_view_vis={is_view_vis}, is_details_loaded={is_details_loaded}",
            message="Validate View action button navigation",
        )
        assert is_view_vis, f"View button not visible for row '{sample_model}'"
        assert is_details_loaded, "Details page failed to load after clicking View button"

    # 22. Test Delete action button visibility for table row
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_delete_button_visibility(
        self,
        atcu_model_page,
        report_case,
    ):
        logger.info("Validating Delete action button visibility for model row")
        sample_model = "AEPL052300"
        assert atcu_model_page.is_model_present_in_table(sample_model)

        is_delete_vis = atcu_model_page.is_delete_button_visible_for_row(sample_model)
        report_case(
            expected=f"Delete action button should be visible for row '{sample_model}'",
            actual=f"is_delete_vis={is_delete_vis}",
            message="Validate Delete button visibility",
        )
        assert is_delete_vis, f"Delete button is not visible for row '{sample_model}'"

    # 23. End-to-End Scenario: Create unique device model, verify in search, and delete
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_add_delete_and_verify(
        self,
        atcu_model_page,
        report_case,
    ):
        """
        Flow:
        1. Navigate to Add Device Model form (/device-model-details)
        2. Create a new unique model (e.g. MODEL NAME: 'AUTO_MODEL_1700', MODEL CODE: 'CODE_1700', HW Version: 'V1.0')
        3. Submit form and return to model list
        4. Search for 'AUTO_MODEL_1700' in search bar
        5. Validate model appears in table list
        6. Delete model via Delete action button
        7. Search again and confirm model is deleted from list
        """
        logger.info("Step 1: Navigating to Add Device Model page")
        atcu_model_page.click_add_device_model_button()
        assert atcu_model_page.is_details_page_loaded()

        logger.info("Step 2: Entering unique MODEL NAME, Code, and HW Version")
        timestamp = int(time.time())
        unique_model_name = f"AUTO_MODEL_{timestamp}"
        unique_model_code = f"CODE_{timestamp}"
        unique_hw_ver = "V1.0.0"

        atcu_model_page.fill_create_model_form(
            model_name=unique_model_name,
            model_code=unique_model_code,
            hw_version=unique_hw_ver,
        )
        assert atcu_model_page.is_submit_button_enabled()

        logger.info("Step 3: Submitting form")
        atcu_model_page.click_submit_button()

        logger.info("Step 4: Searching for created model in list")
        atcu_model_page.search_model_list(unique_model_name)

        logger.info("Step 5: Validating model appears in table")
        is_created_present = atcu_model_page.is_model_present_in_table(unique_model_name, timeout=10000)
        assert is_created_present, f"Created model '{unique_model_name}' not found in table"

        logger.info("Step 6: Deleting created model")
        assert atcu_model_page.is_delete_button_visible_for_row(unique_model_name)
        atcu_model_page.click_delete_button_for_row(unique_model_name)

        logger.info("Step 7: Confirming model is deleted from table")
        atcu_model_page.search_model_list(unique_model_name)
        is_still_present = atcu_model_page.is_model_present_in_table(unique_model_name, timeout=3000)
        assert not is_still_present, f"Deleted model '{unique_model_name}' is still present in table"

        report_case(
            expected="Device model should be created, verified via search, deleted, and confirmed absent",
            actual=f"unique_model='{unique_model_name}', is_created_present={is_created_present}, is_still_present={is_still_present}",
            message="Validate end-to-end create, search, and delete model flow",
        )

    # 24. Corner Case Test: Form fields handling leading and trailing whitespace
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_model_create_form_leading_trailing_spaces(
        self,
        atcu_model_page,
        report_case,
    ):
        """
        Corner Case Test:
        Validate form field behavior when inputs contain leading and trailing whitespace.
        Submit should not enable and save/trim properly without error.
        """
        logger.info("Starting corner case validation for leading/trailing spaces in form fields")
        atcu_model_page.click_add_device_model_button()
        assert atcu_model_page.is_details_page_loaded()

        timestamp = int(time.time())
        raw_model_name = f"  TRIM_MODEL_{timestamp}  "
        raw_model_code = f"  TRIM_CODE_{timestamp}  "
        raw_hw_version = "  TRIM_HW_V1.0  "

        atcu_model_page.fill_create_model_form(
            model_name=raw_model_name,
            model_code=raw_model_code,
            hw_version=raw_hw_version,
        )

        is_submit_enabled = atcu_model_page.is_submit_button_enabled()
        assert not is_submit_enabled, "Submit button should be disabled even with leading/trailing spaces in inputs"
        logger.info("Form filled with leading/trailing spaces, submit enabled: %s", is_submit_enabled)

        report_case(
            expected="Form with leading/trailing spaces should not enable submit",
            actual=f"is_submit_enabled={is_submit_enabled}",
            message="Validate leading/trailing whitespace handling in form fields",
        )

    # 25. Scenario Test: Add new model and validate entry into list table
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_model_add_new_model_and_validate_in_list(
        self,
        atcu_model_page,
        report_case,
    ):
        """
        Scenario: Add new model then validate into the list.
        Steps:
        1. Navigate to Create Model form (/device-model-details)
        2. Fill Model Name, Model Code, and HW Version with new unique values
        3. Submit form
        4. Return to / Navigate to Device Models list (/device-model-list)
        5. Search for newly added model name in search bar
        6. Validate entry is present in table and row data (Model Name, Model Code, HW Version) matches
        7. Clean up created model
        """
        logger.info("Step 1: Navigating to Add Device Model form")
        atcu_model_page.click_add_device_model_button()
        assert atcu_model_page.is_details_page_loaded()

        logger.info("Step 2: Filling form with new model details")
        ts = int(time.time())
        new_model_name = f"NEW_MODEL_{ts}"
        new_model_code = f"NEW_CODE_{ts}"
        new_hw_ver = f"NEW_HW_{ts}"

        atcu_model_page.fill_create_model_form(
            model_name=new_model_name,
            model_code=new_model_code,
            hw_version=new_hw_ver,
        )
        assert atcu_model_page.is_submit_button_enabled()

        logger.info("Step 3: Submitting Create Model form")
        atcu_model_page.click_submit_button()

        logger.info("Step 4: Returning to Device Models list page")
        atcu_model_page.is_page_loaded()

        logger.info("Step 5: Searching for newly added model '%s' in table", new_model_name)
        atcu_model_page.search_model_list(new_model_name)

        logger.info("Step 6: Validating entry present in list table and matching details")
        is_entry_present = atcu_model_page.is_model_present_in_table(new_model_name, timeout=10000)
        assert is_entry_present, f"Newly added model '{new_model_name}' not found in Device Models list table"

        row_details = atcu_model_page.get_row_details_by_model_name(new_model_name)
        logger.info("Row details for newly added model: %s", row_details)

        # Cleanup created model
        atcu_model_page.click_delete_button_for_row(new_model_name)

        report_case(
            expected="Newly added model should appear in Device Models list table with matching details",
            actual=f"new_model='{new_model_name}', is_entry_present={is_entry_present}, row_details={row_details}",
            message="Validate add new model and verify entry in list",
        )
        assert (
            row_details.get("MODEL NAME") == new_model_name
            or row_details.get("Model Name") == new_model_name
            or new_model_name in str(row_details)
        ), f"Model Name mismatched in list row: {row_details}"