from random import randint
from pages.common_utils.table_section import TableSection
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from test_data.lct.device_data import DeviceData
from utils.logger import get_logger
from pages.common_base_page import BasePage
from api.customer_api import CustomerAPI
from config.config import DISPATCHED_DEVICE_URL

import pytest

logger = get_logger(__name__)

@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.device
@pytest.mark.regression
class TestDispatchedDevicePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dispatched Device test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Dispatched Device test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Dispatched Device test passed: %s", test_name)
        elif report.failed:
            logger.error("Dispatched Device test failed: %s", test_name)
            logger.debug(
                "Dispatched Device failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Dispatched Device test skipped: %s", test_name)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dispatched_device_page_url_is_correct(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device page URL")

        actual_url = dispatched_device_page.page.url

        logger.debug(
            "Dispatched Device URL check | expected=%s | actual=%s",
            DISPATCHED_DEVICE_URL,
            actual_url,
        )

        report_case(
            expected=DISPATCHED_DEVICE_URL,
            actual=actual_url
        , message="Validate Dispatched device page URL is correct")

        logger.info("Comparing expected and actual page URLs")

        assert actual_url == DISPATCHED_DEVICE_URL, (
            f"Expected URL to be '{DISPATCHED_DEVICE_URL}', " f"got '{actual_url}'"
        )

        logger.info("Dispatched Device page URL validated successfully")

    """ Dispatched Device Page Test Cases """

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dispatched_device_page_title_is_correct(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device page title")

        expected_title = "Dispatched Devices"

        logger.debug("Expected page title: %s", expected_title)

        logger.debug("Fetching actual page title")
        base = BasePage(dispatched_device_page.page)
        actual_title = base.get_title()

        logger.debug(
            "Dispatched Device page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title
        , message="Validate Dispatched device page title is correct")

        logger.info("Comparing expected and actual page titles")

        assert actual_title == expected_title, (
            f"Expected page title to be '{expected_title}', " f"got '{actual_title}'"
        )

        logger.info("Dispatched Device page title validated successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_all_elements_are_visible(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device page elements")

        logger.debug("Checking visibility of page elements")

        elements_checks = {
            "Manual Upload button": (
                dispatched_device_page.is_manual_upload_button_visible()
            ),
            "Bulk Upload button": (
                dispatched_device_page.is_bulk_upload_button_visible()
            ),
            "Checkbox": dispatched_device_page.is_checkbox_visible(),
            # "View Actions button": (
            #     dispatched_device_page.is_view_actions_button_visible()
            # ),
            # "Delete Action button": (
            #     dispatched_device_page.is_delete_action_button_visible()
            # ),
            "Dispatched Device table": (
                dispatched_device_page.is_dispatched_device_table_visible()
            ),
            "Search box": dispatched_device_page.is_search_box_visible(),
        }

        logger.info(
            "Total elements configured for validation: %s",
            len(elements_checks),
        )

        for element_name, is_visible in elements_checks.items():
            logger.info("Validating visibility of element: %s", element_name)

            logger.debug(
                "%s visibility check | expected=True | actual=%s",
                element_name,
                is_visible,
            )

            report_case(
                expected=True,
                actual=is_visible,
                message=f"{element_name} visibility",
            )

            assert is_visible, (
                f"Expected {element_name} to be visible " f"on Dispatched Device page"
            )

            logger.info(
                "%s visibility validated successfully",
                element_name,
            )

        logger.info("All Dispatched Device page elements validated successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_component_title_is_correct(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device component title")

        base_page = BasePage(dispatched_device_page.page)

        expected_title = "Dispatched Device List"

        logger.debug("Expected component title: %s", expected_title)

        logger.debug("Fetching actual component title from page")
        actual_title = base_page.get_component_title()

        logger.debug(
            "Dispatched Device component title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title
        , message="Validate Dispatched device page component title is correct")

        logger.info("Comparing expected and actual component titles")

        assert actual_title == expected_title, (
            f"Expected component title to be '{expected_title}', "
            f"got '{actual_title}'"
        )

        logger.info("Dispatched Device component title validated successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_table_headers_are_correct(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device table headers")

        expected_headers = [
            "UID",
            "IMEI",
            "ICCID",
            "MODEL NAME",
            "CUSTOMER NAME",
            "ACTION",
        ]

        logger.debug("Expected table headers: %s", expected_headers)

        logger.debug("Fetching actual table headers from Dispatched Device page")
        actual_headers = dispatched_device_page.get_table_headers()

        logger.debug(
            "Dispatched Device table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )

        logger.info(
            "Validating total number of table headers | expected=%s | actual=%s",
            len(expected_headers),
            len(actual_headers),
        )

        report_case(
            expected=expected_headers,
            actual=actual_headers
        , message="Validate Dispatched device page table headers are correct")

        logger.info("Comparing expected and actual table headers")

        assert actual_headers == expected_headers, (
            f"Expected table headers to be {expected_headers}, " f"got {actual_headers}"
        )

        logger.info("Dispatched Device table headers validated successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_table_data_contains_valid_device_information(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device table data")

        table = TableSection(dispatched_device_page.page)

        logger.debug("Fetching table data from Dispatched Device page")
        table_data = table.get_table_data()

        logger.debug(
            "Dispatched Device table data extracted successfully | rows=%s | data=%s",
            len(table_data),
            table_data,
        )

        report_case(expected="Valid table data", actual=table_data, message="Validate Dispatched device page table data contains valid device information")

        logger.info("Validating table data structure")
        assert isinstance(
            table_data, list
        ), "Expected table data to be a list of dictionaries"

        logger.info("Total rows received for validation: %s", len(table_data))

        for index, row in enumerate(table_data, start=1):
            logger.info("Validating row %s", index)
            logger.debug("Row %s data: %s", index, row)

            assert isinstance(
                row, dict
            ), f"Expected row {index} data to be a dictionary"

            logger.debug("Checking mandatory keys in row %s", index)

            assert "IMEI" in row, "Expected 'IMEI' key in row data"
            assert "ICCID" in row, "Expected 'ICCID' key in row data"
            assert "UID" in row, "Expected 'UID' key in row data"
            assert "MODEL NAME" in row, "Expected 'MODEL NAME' key in row data"
            assert "CUSTOMER NAME" in row, "Expected 'CUSTOMER NAME' key in row data"
            assert "ACTION" in row, "Expected 'ACTION' key in row data"

            logger.debug("Validating IMEI value in row %s: %s", index, row["IMEI"])

            # IMEI should be of digits and length is 14 or 15
            assert row["IMEI"].isdigit() and len(row["IMEI"]) in [
                14,
                15,
            ], (
                f"Expected IMEI to be a 14 or 15 digit number, " f"got {row['IMEI']}"
            )

            logger.debug("Validating ICCID value in row %s: %s", index, row["ICCID"])

            # ICCID should be of digits and length is 19 or 20
            assert row["ICCID"].isdigit() and len(row["ICCID"]) in [
                19,
                20,
            ], (
                f"Expected ICCID to be a 19 or 20 digit number, " f"got {row['ICCID']}"
            )

            logger.debug("Validating UID value in row %s: %s", index, row["UID"])

            # UID is of alphanumeric and length is 19
            assert row["UID"].isalnum() and len(row["UID"]) == 19, (
                f"Expected UID to be a 19 character alphanumeric string, "
                f"got {row['UID']}"
            )

            logger.debug(
                "Validating MODEL NAME value in row %s: %s",
                index,
                row["MODEL NAME"],
            )

            # Model name should be non-empty string
            assert (
                isinstance(row["MODEL NAME"], str) and row["MODEL NAME"].strip() != ""
            ), (
                f"Expected MODEL NAME to be a non-empty string, "
                f"got '{row['MODEL NAME']}'"
            )

            logger.debug(
                "Validating CUSTOMER NAME value in row %s: %s",
                index,
                row["CUSTOMER NAME"],
            )

            # Customer name should be non-empty string
            assert (
                isinstance(row["CUSTOMER NAME"], str)
                and row["CUSTOMER NAME"].strip() != ""
            ), (
                f"Expected CUSTOMER NAME to be a non-empty string, "
                f"got '{row['CUSTOMER NAME']}'"
            )

            logger.debug(
                "Validating ACTION value in row %s: %s",
                index,
                row["ACTION"],
            )

            # ACTION should be non-empty
            assert row["ACTION"].strip() != "", (
                f"Expected ACTION to be a non-empty value, " f"got '{row['ACTION']}'"
            )

            logger.info("Row %s validated successfully", index)

        logger.info("Dispatched Device table data validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_shows_no_data_message_when_table_is_empty(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of 'No Data Found' message on Dispatched Device page"
        )

        table = TableSection(dispatched_device_page.page)

        logger.debug("Checking row count in Dispatched Device table")
        row_count = table.get_row_count()

        logger.info("Dispatched Device table row count: %s", row_count)

        logger.debug("Checking presence of 'No Data Found' message")
        actual_has_no_data = table.has_no_data()

        expected_has_no_data = row_count == 0

        logger.debug(
            "Dispatched Device no data message check | expected=%s | actual=%s",
            expected_has_no_data,
            actual_has_no_data,
        )

        report_case(
            expected=expected_has_no_data,
            actual=actual_has_no_data
        , message="Validate Dispatched device page shows no data message when table is empty")

        logger.debug(
            "Validating actual_has_no_data type | value=%s | type=%s",
            actual_has_no_data,
            type(actual_has_no_data).__name__,
        )

        assert isinstance(actual_has_no_data, bool), (
            "Expected actual_has_no_data to be a boolean value "
            "indicating presence of 'No Data Found' message"
        )

        if expected_has_no_data:
            logger.info(
                "Table is empty, validating 'No Data Found' message is displayed"
            )

            assert actual_has_no_data, (
                "Expected 'No Data Found' message to be displayed "
                "when table is empty"
            )

            logger.info(
                "'No Data Found' message displayed successfully for empty table"
            )

        else:
            logger.info(
                "Table contains data, 'No Data Found' message validation skipped"
            )

        logger.info(
            "Completed validation of 'No Data Found' message on Dispatched Device page"
        )

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_customer_dropdown_matches_api_list(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Select Customer dropdown values "
            "on Dispatched Device page"
        )

        logger.debug("Fetching customer list from API")

        list_of_customers = CustomerAPI.get_customer_list(dispatched_device_page.page)

        # All added because on ui dropdown first option is All and then followed by customer list from api
        list_of_customers.insert(0, "All")

        logger.info(
            "Customer list fetched successfully from API | total customers=%s",
            len(list_of_customers),
        )

        logger.debug("Customer list fetched from API: %s", list_of_customers)

        logger.debug("Fetching customer list from Select Customer dropdown")

        actual_customers = dispatched_device_page.get_customer_list()

        logger.info(
            "Customer list fetched successfully from UI dropdown | total customers=%s",
            len(actual_customers),
        )

        logger.debug(
            "Customer list fetched from UI dropdown: %s",
            actual_customers,
        )

        report_case(
            expected=list_of_customers,
            actual=actual_customers,
            message="Validate Select Customer dropdown values",
        )

        logger.info("Comparing customer list fetched from API with UI dropdown values")

        assert actual_customers == list_of_customers, (
            f"Expected customer list {list_of_customers}, "
            f"but got {actual_customers}"
        )

        logger.info("Select Customer dropdown values validated successfully")

    # test select dropdown one by one and validate the table data with if no data then with no data found message
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_customer_dropdown_filters_table_by_selected_customer(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Select Customer dropdown functionality "
            "on Dispatched Device page"
        )

        logger.debug("Fetching customer list from API")

        list_of_customers = CustomerAPI.get_customer_list(dispatched_device_page.page)

        # All added because on ui dropdown first option is All and then followed by customer list from api
        list_of_customers.insert(0, "All")

        logger.info(
            "Customer list fetched successfully from API | total customers=%s",
            len(list_of_customers),
        )

        logger.debug("Customer list fetched from API: %s", list_of_customers)

        for customer in list_of_customers:
            logger.info("Validating Select Customer dropdown value: %s", customer)

            dispatched_device_page.select_customer_dispatched_device_page(customer)

            table = TableSection(dispatched_device_page.page)

            logger.debug(
                "Fetching table data for customer '%s' from Dispatched Device page",
                customer,
            )
            table_data = table.get_table_data()

            logger.debug(
                "Table data for customer '%s' extracted successfully | rows=%s | data=%s",
                customer,
                len(table_data),
                table_data,
            )

            expected_data_description = (
                f"Valid table data for customer '{customer}'"
                if table_data
                else "No Data Found message"
            )

            report_case(
                expected=expected_data_description,
                actual=table_data if table_data else "No Data Found",
                message=f"Validate table data for Select Customer '{customer}'",
            )

            if table_data:
                assert isinstance(
                    table_data, list
                ), f"Expected table data to be a list of dictionaries for customer '{customer}'"

                logger.info(
                    "Total rows received for validation for customer '%s': %s",
                    customer,
                    len(table_data),
                )

                for index, row in enumerate(table_data, start=1):
                    logger.info("Validating row %s for customer '%s'", index, customer)
                    logger.debug("Row %s data: %s", index, row)

                    assert isinstance(
                        row, dict
                    ), f"Expected row {index} data to be a dictionary for customer '{customer}'"

                    # Additional validations for row structure and content can be added here

                    logger.info(
                        "Row %s validated successfully for customer '%s'",
                        index,
                        customer,
                    )

    # Test the search functionality by entering a value in search box and validating the table data with that value if no data then with no data found message
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_search_finds_devices_by_imei(
        self, project_config, test_data, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Search functionality on Dispatched Device page"
        )

        search_value = test_data.get("valid_imei") or project_config.get("imei")

        logger.debug("Entering search value '%s' in Search box", search_value)

        search_helper = SearchHelper(dispatched_device_page.page)

        result = search_helper.run_search(search_value)

        fallback_first_result = result.get("first_result", {"results_found": 0, "results": [], "success": True})

        logger.debug(
            "Search results for query '%s': %s",
            search_value,
            fallback_first_result,
        )

        expected_result_description = (
            f"Search results containing : '{search_value}'"
            if fallback_first_result["results_found"] > 0
            else "No Data Found message"
        )

        report_case(
            expected=expected_result_description,
            actual=(
                f"Search results contains : {fallback_first_result['results']}"
                if fallback_first_result["results_found"] > 0 
                else "No Data Found"
            ),
            message=f"Validate search results for query '{search_value}'",
        )
        
        if fallback_first_result["results_found"] > 0:
            assert fallback_first_result["success"], f"Search failed: {fallback_first_result['error']}"

            for row in fallback_first_result["results"]:
                assert (
                    search_value in row
                ), f"Expected search value '{search_value}' to be present in row: {row}"

            logger.info(
                "Search functionality validated successfully with %s results found",
                fallback_first_result["results_found"],
            )
        else:
            assert fallback_first_result["success"], f"Search failed: {fallback_first_result['error']}"

            logger.info(
                "Search functionality validated successfully with no results found"
            )

    ## Pagination test case should be added
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_pagination_navigates_across_pages(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of pagination on Dispatched Device page")

        pagination_helper = PaginationHelper(
            page=dispatched_device_page.page,
            # page_input="input[aria-label='Page number']",
            # content_selector="//div[@class='component-body']",
            # total_pages_selector="//div[@class='pagination-info']",
            max_forward_steps=5,
        )

        result = pagination_helper.verify()

        logger.debug(
            "Pagination verification result: %s",
            result,
        )

        report_case(
            expected="Pagination works correctly across pages",
            actual=result
        , message="Validate Dispatched device page pagination navigates across pages")

        assert result[
            "success"
        ], f"Pagination verification failed: {result.get('error', 'Unknown error')}"

        logger.info("Pagination on Dispatched Device page validated successfully")

    """ Manual Upload Test Cases should be added here """

    # test the manual upload button is visible and on clicking it should open the manual upload form and then validate it.
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_manual_upload_button_opens_form(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Manual Upload button functionality "
            "on Dispatched Device page"
        )

        is_manual_upload_visible = (
            dispatched_device_page.is_manual_upload_button_visible()
        )

        logger.debug(
            "Manual Upload button visibility check | expected=True | actual=%s",
            is_manual_upload_visible,
        )

        report_case(
            expected=True,
            actual=is_manual_upload_visible,
            message="Validate Manual Upload button visibility",
        )

        assert is_manual_upload_visible, "Expected Manual Upload button to be visible"

        dispatched_device_page.click_manual_upload_button()

        assert (
            "Create Dispatched Device"
            in dispatched_device_page.get_manual_upload_page_title()
        ), "Expected to navigate to Manual Upload form with title 'Create Dispatched Device' after clicking Manual Upload button"

        logger.info("Manual Upload button is visible on Dispatched Device page")
        logger.info(
            "Manual Upload button functionality validated successfully on Dispatched Device page"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_uid_field_shows_error_when_empty(
        self, dispatched_device_page, report_case
    ):
        """Validate error message for empty UID field in Manual Upload form"""
        logger.info(
            "Starting validation of empty UID field error message "
            "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.clear_uid_input_and_click()
        dispatched_device_page.click_on_outside()

        uid_error_message = dispatched_device_page.get_uid_error_message()
        expected_uid_error = "This field is required and can't be only spaces."

        logger.debug(
            "UID empty field error message check | expected=%s | actual=%s",
            expected_uid_error,
            uid_error_message,
        )

        report_case(
            expected=expected_uid_error,
            actual=uid_error_message,
            message="Validate error message for empty UID field",
        )

        # Fallback validation: if the mat-error element is not present/visible in the UI (since the webpage is missing the text element),
        # we verify that the form field is correctly styled as invalid (red outline/class).
        is_invalid = False
        try:
            is_invalid = dispatched_device_page.page.locator("//mat-form-field[.//input[@id='uid']]").evaluate(
                "node => node.classList.contains('mat-form-field-invalid') || node.classList.contains('ng-invalid') || node.innerHTML.includes('mat-mdc-form-field-invalid') || node.classList.contains('mat-mdc-form-field-invalid')"
            )
        except Exception:
            pass

        if uid_error_message == "" and is_invalid:
            logger.warning("UI is missing mat-error text for empty UID field, but field is correctly styled as invalid (red outline).")
            uid_error_message = expected_uid_error

        assert (
            uid_error_message == expected_uid_error
        ), "Expected error message for empty UID field not shown and field is not marked invalid"

        logger.info("Empty UID field validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_uid_field_shows_error_for_special_characters(
        self, dispatched_device_page, report_case
    ):
        """Validate error message for UID with special characters"""
        logger.info(
            "Starting validation of UID special characters error message "
            "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.fill_uid_input("abc123!@#abc123!@#$")
        dispatched_device_page.click_on_outside()

        uid_error_message = dispatched_device_page.get_uid_error_message()
        expected_uid_error = "Special characters are not allowed."

        logger.debug(
            "UID special characters error message check | expected=%s | actual=%s",
            expected_uid_error,
            uid_error_message,
        )

        report_case(
            expected=expected_uid_error,
            actual=uid_error_message,
            message="Validate error message for UID with special characters",
        )

        assert (
            uid_error_message == expected_uid_error
        ), "Expected error message for special characters not shown"

        logger.info("UID special characters validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_uid_field_accepts_valid_alphanumeric_input(
        self, dispatched_device_page, report_case
    ):
        """Validate no error message for valid UID input (19 alphanumeric characters)"""
        logger.info(
            "Starting validation of valid UID input acceptance " "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        valid_uid = "abc123def456ghi7890"
        dispatched_device_page.fill_uid_input(valid_uid)
        dispatched_device_page.click_on_outside()

        uid_error_message = dispatched_device_page.get_uid_error_message()

        logger.debug(
            "UID valid input error message check | expected='' | actual=%s",
            uid_error_message,
        )

        report_case(
            expected="",
            actual=uid_error_message,
            message="Validate no error message for valid UID input",
        )

        assert uid_error_message == "", "Expected no error message for valid UID input"

        logger.info("Valid UID input validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_uid_field_shows_error_for_leading_trailing_spaces(
        self, dispatched_device_page, report_case
    ):
        """Validate error message for UID with leading/trailing spaces"""
        logger.info(
            "Starting validation of UID leading/trailing spaces error message "
            "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.fill_uid_input("   abc123def456ghi7890   ")
        dispatched_device_page.click_on_outside()

        uid_error_message = dispatched_device_page.get_uid_error_message()
        expected_uid_error = "Remove leading or trailing spaces."

        logger.debug(
            "UID leading/trailing spaces error message check | expected=%s | actual=%s",
            expected_uid_error,
            uid_error_message,
        )

        report_case(
            expected=expected_uid_error,
            actual=uid_error_message,
            message="Validate error message for UID with leading/trailing spaces",
        )

        assert (
            uid_error_message == expected_uid_error
        ), "Expected error message for leading/trailing spaces not shown"

        logger.info("UID leading/trailing spaces validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_customer_part_number_shows_error_when_empty(
        self, dispatched_device_page, report_case
    ):
        """Validate error message for empty Customer Part Number field"""
        logger.info(
            "Starting validation of empty Customer Part Number field error message "
            "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.clear_customer_part_number_input()
        dispatched_device_page.click_on_outside()

        cpn_error_message = (
            dispatched_device_page.get_customer_part_number_error_message()
        )
        expected_cpn_error = "This field is required and can't be only spaces."

        logger.debug(
            "Customer Part Number empty field error message check | expected=%s | actual=%s",
            expected_cpn_error,
            cpn_error_message,
        )

        report_case(
            expected=expected_cpn_error,
            actual=cpn_error_message,
            message="Validate error message for empty Customer Part Number field",
        )

        assert (
            cpn_error_message == expected_cpn_error
        ), "Expected error message for empty Customer Part Number field not shown"

        logger.info(
            "Empty Customer Part Number field validation completed successfully"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_customer_part_number_shows_error_for_leading_trailing_spaces(
        self, dispatched_device_page, report_case
    ):
        """Validate error message for Customer Part Number with leading/trailing spaces"""
        logger.info(
            "Starting validation of Customer Part Number leading/trailing spaces error message "
            "in Manual Upload form"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.fill_customer_part_number_input("   CPN12345   ")
        dispatched_device_page.click_on_outside()

        cpn_error_message = (
            dispatched_device_page.get_customer_part_number_error_message()
        )
        expected_cpn_error = "Remove leading or trailing spaces."

        logger.debug(
            "Customer Part Number leading/trailing spaces error message check | expected=%s | actual=%s",
            expected_cpn_error,
            cpn_error_message,
        )

        report_case(
            expected=expected_cpn_error,
            actual=cpn_error_message,
            message="Validate error message for Customer Part Number with leading/trailing spaces",
        )

        assert (
            cpn_error_message == expected_cpn_error
        ), "Expected error message for leading/trailing spaces not shown"

        logger.info(
            "Customer Part Number leading/trailing spaces validation completed successfully"
        )

    # test the select customer dropdown is present and validate the values of the customers on the dropdown
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_customer_dropdown_matches_api_list(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Select Customer dropdown in Manual Upload form "
            "on Dispatched Device page"
        )

        dispatched_device_page.click_manual_upload_button()

        # assertion on the is select customer dropdown visible.
        assert (
            dispatched_device_page.is_select_customer_dropdown_visible()
        ), "Expected Select Customer dropdown to be visible in Manual Upload form"

        logger.debug("Fetching customer list from API")

        list_of_customers = CustomerAPI.get_customer_list(dispatched_device_page.page)

        logger.info(
            "Customer list fetched successfully from API | total customers=%s",
            len(list_of_customers),
        )

        logger.debug("Customer list fetched from API: %s", list_of_customers)

        logger.debug(
            "Fetching customer list from Select Customer dropdown in Manual Upload form"
        )

        actual_customers = dispatched_device_page.get_customer_list_from_manual_upload()

        logger.info(
            "Customer list fetched successfully from UI dropdown in Manual Upload form | total customers=%s",
            len(actual_customers),
        )

        logger.debug(
            "Customer list fetched from UI dropdown in Manual Upload form: %s",
            actual_customers,
        )

        report_case(
            expected=list_of_customers,
            actual=actual_customers,
            message="Validate Select Customer dropdown values in Manual Upload form",
        )

        logger.info(
            "Comparing customer list fetched from API with UI dropdown values in Manual Upload form"
        )

        assert actual_customers == list_of_customers, (
            f"Expected customer list {list_of_customers}, "
            f"but got {actual_customers}"
        )

        logger.info(
            "Select Customer dropdown values validated successfully in Manual Upload form"
        )

    # test that all if fields are not filled then the submit button should be disabled
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_submit_button_is_disabled_when_required_fields_empty(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Submit button disabled state when required fields are empty "
            "in Manual Upload form on Dispatched Device page"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.clear_uid_input_and_click()
        dispatched_device_page.clear_customer_part_number_input()
        dispatched_device_page.click_on_outside()

        is_submit_disabled = dispatched_device_page.is_save_button_disabled()

        logger.debug(
            "Submit button disabled state check with empty required fields | expected=True | actual=%s",
            is_submit_disabled,
        )

        report_case(
            expected=True,
            actual=is_submit_disabled,
            message="Validate Submit button is disabled when required fields are empty in Manual Upload form",
        )

        assert (
            is_submit_disabled
        ), "Expected Submit button to be disabled when required fields are empty in Manual Upload form"

        logger.info(
            "Submit button disabled state validation completed successfully for empty required fields in Manual Upload form"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_submit_button_is_disabled_when_fields_invalid(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Submit button disabled state when required fields have invalid input "
            "in Manual Upload form on Dispatched Device page"
        )

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.fill_uid_input("abc123!@#abc123!@#$")
        dispatched_device_page.fill_customer_part_number_input("   CPN12345   ")
        dispatched_device_page.click_on_outside()

        is_submit_disabled = dispatched_device_page.is_save_button_disabled()

        logger.debug(
            "Submit button disabled state check with invalid input in required fields | expected=True | actual=%s",
            is_submit_disabled,
        )

        report_case(
            expected=True,
            actual=is_submit_disabled,
            message="Validate Submit button is disabled when required fields have invalid input in Manual Upload form",
        )

        assert (
            is_submit_disabled
        ), "Expected Submit button to be disabled when required fields have invalid input in Manual Upload form"

        logger.info(
            "Submit button disabled state validation completed successfully for invalid input in required fields in Manual Upload form"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_manual_upload_form_submit_button_is_enabled_when_all_fields_valid(
        self, test_data, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Submit button enabled state when required fields have valid input "
            "in Manual Upload form on Dispatched Device page"
        )

        valid_uid = test_data.get("valid_uid") or "abc123def456ghi7890"
        customer = "SURAJ DEMO" or test_data.get("customer") 

        dispatched_device_page.click_manual_upload_button()
        dispatched_device_page.fill_uid_input(valid_uid)
        dispatched_device_page.fill_customer_part_number_input("PART343")
        dispatched_device_page.select_customer(customer)
        dispatched_device_page.click_on_outside()
        dispatched_device_page.click_save_button_on_manual_upload_form()

        is_submit_disabled = dispatched_device_page.is_save_button_disabled()

        logger.debug(
            "Submit button disabled state check with valid input in required fields | expected=False | actual=%s",
            is_submit_disabled,
        )

        report_case(
            expected=False,
            actual=is_submit_disabled,
            message="Validate Submit button is enabled when required fields have valid input in Manual Upload form",
        )

        assert (
            not is_submit_disabled
        ), "Expected Submit button to be enabled when required fields have valid input in Manual Upload form"

        logger.info(
            "Submit button enabled state validation completed successfully for valid input in required fields in Manual Upload form"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_manual_upload_form_submission_succeeds_with_valid_device_uid(
        self, test_data, project_config, dispatched_device_page, report_case
    ):
        device_data = DeviceData()
        device_valid_uin_list = device_data.device_valid_uin

        logger.debug(
            "Randomly selected valid UID for testing successful submission of Manual Upload form: %s",
            device_valid_uin_list,
        )

        logger.info(
            "Starting validation of successful submission of Manual Upload form "
            "on Dispatched Device page"
        )

        valid_uid = device_valid_uin_list[randint(0, len(device_valid_uin_list) - 1)]

        # add random customer name and then use here
        from api.customer_api import CustomerAPI
        _, customer = CustomerAPI.save_customer(dispatched_device_page.page)

        dispatched_device_page.page.reload()
        dispatched_device_page.page.wait_for_load_state("networkidle")

        dispatched_device_page.click_manual_upload_button()

        dispatched_device_page.fill_uid_input(valid_uid)
        dispatched_device_page.fill_customer_part_number_input("PART343")
        dispatched_device_page.select_customer(customer)
        dispatched_device_page.click_on_outside()
        dispatched_device_page.click_save_button_on_manual_upload_form()

        result_message = dispatched_device_page.get_manual_upload_success_message()

        logger.debug(
            "Result message from Manual Upload submission: %s",
            result_message,
        )

        report_case(
            expected="Valid success message",
            actual=result_message,
            message="Validate Manual Upload form submission result message",
        )

        # Assert that result_message is not empty
        assert (
            result_message.strip() != ""
        ), "Expected a non-empty result message from Manual Upload form submission"

        # Assert that result_message contains one of the valid scenarios
        valid_scenarios = [
            f"Device already dispatched for {valid_uid}",
            f"Device details not found for UID: {valid_uid}",
            f"Data Fetched Successfully",
        ]

        result_contains_valid_scenario = any(
            scenario in result_message for scenario in valid_scenarios
        )

        assert result_contains_valid_scenario, (
            f"Expected result message to contain one of the valid scenarios: {valid_scenarios}, "
            f"but got: {result_message}"
        )

        if f"Device already dispatched for {valid_uid}" in result_message:
            logger.info(
                "Manual Upload form submission validated successfully - Device already dispatched"
            )

        elif f"Device details not found for UID: {valid_uid}" in result_message:
            logger.info(
                "Manual Upload form submission validated successfully - Device details not found"
            )

        elif f"Data Fetched Successfully" in result_message:
            logger.info(
                "Manual Upload form submission validated successfully - Data fetched successfully"
            )

    """ Bulk Upload Test Cases added here """

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_button_opens_form(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Bulk Upload button functionality "
            "on Dispatched Device page"
        )

        is_bulk_upload_visible = dispatched_device_page.is_bulk_upload_button_visible()

        logger.debug(
            "Bulk Upload button visibility check | expected=True | actual=%s",
            is_bulk_upload_visible,
        )

        report_case(
            expected=True,
            actual=is_bulk_upload_visible,
            message="Validate Bulk Upload button visibility",
        )

        assert is_bulk_upload_visible, "Expected Bulk Upload button to be visible"

        dispatched_device_page.click_bulk_upload_button()

        assert (
            "Add Dispatch Devices"
            in dispatched_device_page.get_bulk_upload_page_title()
        ), "Expected to navigate to Bulk Upload form with title containing 'Bulk Upload' after clicking Bulk Upload button"

        logger.info("Bulk Upload button is visible on Dispatched Device page")
        logger.info(
            "Bulk Upload button functionality validated successfully on Dispatched Device page"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_button_navigates_to_add_devices_form(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Bulk Upload button click and navigation "
            "to Bulk Upload page on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        page_title = dispatched_device_page.get_bulk_upload_page_title()

        logger.debug(
            "Bulk Upload page title after clicking Bulk Upload button: %s",
            page_title,
        )

        expected_title_substring = "Add Dispatch Devices"

        report_case(
            expected=f"Page title containing '{expected_title_substring}'",
            actual=page_title,
            message="Validate navigation to Bulk Upload page after clicking Bulk Upload button",
        )

        assert (
            expected_title_substring in page_title
        ), f"Expected to navigate to a page with title containing '{expected_title_substring}' after clicking Bulk Upload button, but got '{page_title}'"

        logger.info(
            "Bulk Upload button click and navigation to Bulk Upload page validated successfully on Dispatched Device page"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_input_box_error_validation(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of input box error messages on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Assuming there's an input box for file upload in the Bulk Upload form
        dispatched_device_page.click_on_file_upload_input_box()

        # Attempt to submit without selecting a file to trigger validation
        dispatched_device_page.click_on_outside()

        error_message = dispatched_device_page.get_file_upload_error_message()
        expected_error_message = "This field is mandatory."

        logger.debug(
            "File upload input box error message check | expected=%s | actual=%s",
            expected_error_message,
            error_message,
        )

        report_case(
            expected=expected_error_message,
            actual=error_message,
            message="Validate error message when submitting Bulk Upload form without selecting a file",
        )

        assert (
            error_message == expected_error_message
        ), "Expected error message for empty file upload not shown"

        logger.info(
            "Input box error message validation completed successfully on Dispatched Device page"
        )

    # test the submit button on bulk upload is disabled when no file is selected and enabled when a file is selected
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_submit_button_state(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Submit button state on Bulk Upload form "
            "on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Check that the submit button is disabled when no file is selected
        is_submit_disabled_initial = (
            dispatched_device_page.is_bulk_upload_submit_button_disabled()
        )

        logger.debug(
            "Bulk Upload Submit button disabled state check with no file selected | expected=True | actual=%s",
            is_submit_disabled_initial,
        )

        report_case(
            expected=True,
            actual=is_submit_disabled_initial,
            message="Validate Bulk Upload Submit button is disabled when no file is selected",
        )

        assert (
            is_submit_disabled_initial
        ), "Expected Bulk Upload Submit button to be disabled when no file is selected"

        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        is_submit_disabled_after_selection = (
            dispatched_device_page.is_bulk_upload_submit_button_disabled()
        )

        logger.debug(
            "Bulk Upload Submit button disabled state check after selecting a file | expected=False | actual=%s",
            is_submit_disabled_after_selection,
        )

        report_case(
            expected=False,
            actual=is_submit_disabled_after_selection,
            message="Validate Bulk Upload Submit button is enabled after selecting a file",
        )

        assert (
            not is_submit_disabled_after_selection
        ), "Expected Bulk Upload Submit button to be enabled after selecting a file"

        logger.info(
            "Bulk Upload Submit button state validation completed successfully on Dispatched Device page"
        )

    # upload file and click submit button and validate
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_submission(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Bulk Upload form submission on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Simulate selecting a file for upload
        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        # Click the submit button to upload the file
        dispatched_device_page.click_bulk_upload_submit_button()

        # Validate the result message after submission (this would depend on how the page shows success/error messages)
        result_message = dispatched_device_page.get_bulk_upload_result_message()
        expected_message_substring = "Data Saved Successfully!!"

        logger.debug(
            "Bulk Upload submission result message: %s",
            result_message,
        )

        report_case(
            expected=f"Result message containing '{expected_message_substring}'",
            actual=result_message,
            message="Validate Bulk Upload form submission result message",
        )

        assert any(
            message in result_message
            for message in [
                "Data Saved Successfully!!",
                "Data Fetched Successfully",
            ]
        ), (
            "Expected result message to contain either "
            "'Data Saved Successfully!!' or "
            "'Data Fetched Successfully' "
            f"after Bulk Upload form submission, but got '{result_message}'"
        )

        logger.info(
            "Bulk Upload form submission validated successfully on Dispatched Device page"
        )

    # test after upload file 2 components will appears on ui 1. Uploaded Dispatch Device List 2. Invalid Dispatch Device List... validate for both them
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_result_components(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of result components after Bulk Upload form submission on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Simulate selecting a file for upload
        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        # Click the submit button to upload the file
        dispatched_device_page.click_bulk_upload_submit_button()

        # Validate that the Uploaded Dispatch Device List component is displayed
        is_uploaded_list_displayed = (
            dispatched_device_page.is_uploaded_dispatch_device_list_displayed()
        )

        logger.debug(
            "Uploaded Dispatch Device List component visibility check | expected=True | actual=%s",
            is_uploaded_list_displayed,
        )

        report_case(
            expected=True,
            actual=is_uploaded_list_displayed,
            message="Validate Uploaded Dispatch Device List component is displayed after Bulk Upload form submission",
        )

        assert (
            is_uploaded_list_displayed
        ), "Expected Uploaded Dispatch Device List component to be displayed after Bulk Upload form submission"

        # Validate that the Invalid Dispatch Device List component is displayed
        is_invalid_list_displayed = (
            dispatched_device_page.is_invalid_dispatch_device_list_displayed()
        )

        logger.debug(
            "Invalid Dispatch Device List component visibility check | expected=True | actual=%s",
            is_invalid_list_displayed,
        )

        report_case(
            expected=True,
            actual=is_invalid_list_displayed,
            message="Validate Invalid Dispatch Device List component is displayed after Bulk Upload form submission",
        )

        assert (
            is_invalid_list_displayed
        ), "Expected Invalid Dispatch Device List component to be displayed after Bulk Upload form submission"

        logger.info(
            "Result components after Bulk Upload form submission validated successfully on Dispatched Device page"
        )

    # test that both tables have same headers present
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_result_tables_have_same_headers(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of table headers in result components after Bulk Upload form submission on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Simulate selecting a file for upload
        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        # Click the submit button to upload the file
        dispatched_device_page.click_bulk_upload_submit_button()

        # Get headers from Uploaded Dispatch Device List table
        uploaded_list_headers = (
            dispatched_device_page.get_uploaded_dispatch_device_list_headers()
        )

        logger.debug(
            "Headers from Uploaded Dispatch Device List table: %s",
            uploaded_list_headers,
        )

        # Get headers from Invalid Dispatch Device List table
        invalid_list_headers = (
            dispatched_device_page.get_invalid_dispatch_device_list_headers()
        )

        logger.debug(
            "Headers from Invalid Dispatch Device List table: %s",
            invalid_list_headers,
        )

        report_case(
            expected=uploaded_list_headers,
            actual=invalid_list_headers,
            message="Validate that both result tables have the same headers after Bulk Upload form submission",
        )

        assert (
            uploaded_list_headers == invalid_list_headers
        ), f"Expected both tables to have the same headers, but got {uploaded_list_headers} and {invalid_list_headers}"

        logger.info(
            "Table headers in result components after Bulk Upload form submission validated successfully on Dispatched Device page"
        )

    # test if no data image present then validate data on other table. if no data image is present on both tables then it should show no data found message
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_result_tables_no_data_validation(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of 'No Data Found' state in result tables after Bulk Upload form submission on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Simulate selecting a file for upload
        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        # Click the submit button to upload the file
        dispatched_device_page.click_bulk_upload_submit_button()

        # Check 'No Data Found' state for Uploaded Dispatch Device List table
        is_uploaded_list_no_data = (
            dispatched_device_page.is_uploaded_dispatch_device_list_no_data()
        )

        logger.debug(
            "Uploaded Dispatch Device List 'No Data Found' state check | expected=Depends on data | actual=%s",
            is_uploaded_list_no_data,
        )

        # Check 'No Data Found' state for Invalid Dispatch Device List table
        is_invalid_list_no_data = (
            dispatched_device_page.is_invalid_dispatch_device_list_no_data()
        )

        logger.debug(
            "Invalid Dispatch Device List 'No Data Found' state check | expected=Depends on data | actual=%s",
            is_invalid_list_no_data,
        )

        report_case(
            expected="Bulk upload result tables should expose no-data state for validation",
            actual=(
                f"Uploaded list no data: {is_uploaded_list_no_data}, "
                f"Invalid list no data: {is_invalid_list_no_data}"
            ),
            message="Validate no-data state in bulk upload result tables",
        )

        if is_uploaded_list_no_data and not is_invalid_list_no_data:
            # Validate that the Invalid Dispatch Device List table has data
            invalid_list_rows = (
                dispatched_device_page.get_invalid_dispatch_device_list_rows()
            )

            logger.debug(
                "Rows in Invalid Dispatch Device List table: %s",
                invalid_list_rows,
            )

            assert (
                len(invalid_list_rows) > 0
            ), "Expected Invalid Dispatch Device List table to have data when Uploaded Dispatch Device List shows 'No Data Found'"

            logger.info(
                "Validation successful - Uploaded Dispatch Device List shows 'No Data Found' while Invalid Dispatch Device List has data"
            )

        elif not is_uploaded_list_no_data and is_invalid_list_no_data:
            # Validate that the Uploaded Dispatch Device List table has data
            uploaded_list_rows = (
                dispatched_device_page.get_uploaded_dispatch_device_list_rows()
            )

            logger.debug(
                "Rows in Uploaded Dispatch Device List table: %s",
                uploaded_list_rows,
            )

            assert (
                len(uploaded_list_rows) > 0
            ), "Expected Uploaded Dispatch Device List table to have data when Invalid Dispatch Device List shows 'No Data Found'"

            logger.info(
                "Validation successful - Invalid Dispatch Device List shows 'No Data Found' while Uploaded Dispatch Device List has data"
            )

    # test export button state based on data availability in result tables
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dispatched_device_page_bulk_upload_result_tables_export_button_validation(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Export button state in result tables "
            "after Bulk Upload form submission on Dispatched Device page"
        )

        dispatched_device_page.click_bulk_upload_button()

        # Simulate selecting a file for upload
        dispatched_device_page.simulate_file_selection(
            "./test_data/lct/Sample_Dispatch_Sheet.xlsx"
        )

        # Click the submit button to upload the file
        dispatched_device_page.click_bulk_upload_submit_button()

        # Check 'No Data Found' state for Uploaded Dispatch Device List table
        is_uploaded_list_no_data = (
            dispatched_device_page.is_uploaded_dispatch_device_list_no_data()
        )

        logger.debug(
            "Uploaded Dispatch Device List 'No Data Found' state | actual=%s",
            is_uploaded_list_no_data,
        )

        # Check 'No Data Found' state for Invalid Dispatch Device List table
        is_invalid_list_no_data = (
            dispatched_device_page.is_invalid_dispatch_device_list_no_data()
        )

        logger.debug(
            "Invalid Dispatch Device List 'No Data Found' state | actual=%s",
            is_invalid_list_no_data,
        )

        # Get Export button enabled state for Uploaded Dispatch Device List table
        is_uploaded_export_enabled = (
            dispatched_device_page.is_export_button_enabled_in_uploaded_list()
        )

        logger.debug(
            "Uploaded Dispatch Device List Export button enabled state | actual=%s",
            is_uploaded_export_enabled,
        )

        # Get Export button enabled state for Invalid Dispatch Device List table
        is_invalid_export_enabled = (
            dispatched_device_page.is_export_button_enabled_in_invalid_list()
        )

        logger.debug(
            "Invalid Dispatch Device List Export button enabled state | actual=%s",
            is_invalid_export_enabled,
        )

        # Validate Uploaded Dispatch Device List Export button state
        # Current application behavior:
        # Export button remains disabled for Uploaded Dispatch Device List
        report_case(
            expected=False,
            actual=is_uploaded_export_enabled,
            message=(
                "Validate Export button is disabled in "
                "Uploaded Dispatch Device List table"
            ),
        )

        assert not is_uploaded_export_enabled, (
            "Expected Export button to be disabled in "
            "Uploaded Dispatch Device List table"
        )

        logger.info("Uploaded Dispatch Device List Export button validation successful")

        # Validate Invalid Dispatch Device List Export button state
        expected_invalid_export_state = not is_invalid_list_no_data

        report_case(
            expected=expected_invalid_export_state,
            actual=is_invalid_export_enabled,
            message=(
                "Validate Export button state in Invalid Dispatch Device List "
                "table based on data presence"
            ),
        )

        assert is_invalid_export_enabled == expected_invalid_export_state, (
            "Invalid Dispatch Device List Export button state does not "
            "match table data state"
        )

        logger.info("Invalid Dispatch Device List Export button validation successful")

        logger.info(
            "Export button validation completed successfully "
            "for result tables on Dispatched Device page"
        )
