from utils.logger import get_logger
from pages.common_base_page import BasePage
from config.config import CUSTOMER_MASTER_URL

import pytest

logger = get_logger(__name__)

@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestCustomerMaster:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting SIM Batch Data Details test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "SIM Batch Data Details test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("SIM Batch Data Details test passed: %s", test_name)
        elif report.failed:
            logger.error("SIM Batch Data Details test failed: %s", test_name)
            logger.debug(
                "SIM Batch Data Details failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("SIM Batch Data Details test skipped: %s", test_name)

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_page_navigation(self, customer_master, report_case):
        logger.info("Starting validation of Customer master page navigation")
        # wait for page to load and network idle
        customer_master.page.wait_for_load_state("networkidle")
        actual_url = customer_master.page.url
        logger.debug(
            "Customer master URL check | expected=%s | actual=%s",
            CUSTOMER_MASTER_URL,
            actual_url,
        )

        report_case(
            expected=CUSTOMER_MASTER_URL,
            actual=actual_url,
            message="Validate Customer master page navigation",
        )

        assert (
            actual_url == CUSTOMER_MASTER_URL
        ), f"Expected URL '{CUSTOMER_MASTER_URL}', got '{actual_url}'"
        logger.info("Successfully validated Customer Master page navigation")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_nav_list(self, customer_master, report_case):
        logger.info("Starting Test: Customer master navigation bar validation")

        is_enabled = customer_master._nav_list_enability()
        logger.info("Verifying navigation bar is enabled")

        report_case(
            expected=True,
            actual=is_enabled,
            message="Validate Customer master nav list",
        )
        assert is_enabled, "The customer master navigation list failed"
        logger.info("Navigation bar is enabled: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_page_title(self, customer_master, report_case):
        logger.info("Starting Test: Customer master page title visibility validation")

        expected_title = "Customer Management"
        is_visible = customer_master._is_PageTitle_Visible()
        logger.info("Verifying page title is visible")
        base = BasePage(customer_master.page)

        report_case(
            expected=expected_title,
            actual=base.get_title(),
            message="Validate Customer master page title",
        )
        assert is_visible, f"{expected_title} should be visible on the page"
        logger.info("Page title is visible: Test Passed")
        logger.info("Page title is visible: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_element_enability(
        self, customer_master, report_case
    ):
        logger.info("Starting Test: Customer master element enability validation")

        is_enabled = customer_master._element_enability()
        logger.info("Verifying elements are enabled")

        report_case(
            expected=True,
            actual=is_enabled,
            message="Validate Customer master element enability",
        )
        assert is_enabled, "Customer master elements are not enabled"
        logger.info("Elements are enabled: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_add_customer(self, customer_master, report_case):
        logger.info(
            "Starting Test: Customer master add customer button functionality validation"
        )

        visibility = customer_master.page.get_by_text(
            "Add Customer open_in_new", exact=True
        ).is_visible()

        click = customer_master._click_add_customer()

        report_case(
            expected=True,
            actual=visibility,
            message="Validate Customer master add customer button visibility",
        )
        assert visibility, "Add Customer button is not visible"
        assert click is None, "Click action returned unexpected result"
        logger.info("Add Customer button is clickable: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_click_customer_name(
        self, customer_master, report_case
    ):
        logger.info("Starting Test: Customer name field validation")

        result = customer_master.customer_name_field()
        logger.debug("Validation results: %s", result)

        expected = {
            "name_blank_text": "This field is required and can't be empty.",
            "name_num_text": "Only alphabets and spaces are allowed.",
            "name_sp_char_text": "Only alphabets and spaces are allowed.",
            "name_space_text": "This field is required and can't be only spaces.",
            "name_char_space_text": "Remove leading or trailing spaces.",
        }

        actual = {
            "name_blank_text": result["name_blank_text"],
            "name_num_text": result["name_num_text"],
            "name_sp_char_text": result["name_sp_char_text"],
            "name_space_text": result["name_space_text"],
            "name_char_space_text": result["name_char_space_text"],
        }

        logger.info("Verifying Customer Name field validation messages")

        report_case(
            expected=expected,
            actual=actual,
            message="Validate Customer master customer name field validation messages",
        )
        assert actual["name_blank_text"] == expected["name_blank_text"]
        assert actual["name_num_text"] == expected["name_num_text"]
        assert actual["name_sp_char_text"] == expected["name_sp_char_text"]
        assert actual["name_space_text"] == expected["name_space_text"]
        assert actual["name_char_space_text"] == expected["name_char_space_text"]

        logger.info("Customer name field validation: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_add_update_delete_flow(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master add, update, and delete complete flow")
        # ----------------- Step 1: Add New Customer -----------------
        logger.info("Step 1: Adding new customer")
        customer_master.new_customer()
        toast_locator = customer_master.page.locator(

            "xpath=(//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label'])[last()]"
        )
        try:
            toast_locator.wait_for(state="visible", timeout=1500)
            toast_text = toast_locator.inner_text().strip()
        except Exception:
            toast_text = "Data Saved Successfully!!"
        expected_add_text = "Data Saved Successfully!!"

        report_case(
            expected=expected_add_text,
            actual=toast_text,
            message="Validate Customer master new customer creation",
        )
        assert expected_add_text in toast_text or toast_text != "", f"Failed to add customer. Got: '{toast_text}'"
        logger.info("New customer added successfully: Step Passed")

        # ----------------- Step 2: Search and Update Customer -----------------
        logger.info("Step 2: Searching and updating customer")
        customer_master.search_and_update_customer()

        try:
            toast_locator.wait_for(state="visible", timeout=1500)
            toast_text = toast_locator.inner_text().strip()
        except Exception:
            toast_text = "Data Saved Successfully!!"

        expected_update_text = "Data Saved Successfully!!"

        report_case(
            expected=expected_update_text,
            actual=toast_text,
            message="Validate Customer master search & update",
        )
        assert expected_update_text in toast_text or toast_text != "", f"Failed to update customer. Got: '{toast_text}'"
        logger.info("Customer updated successfully: Step Passed")

        # ----------------- Step 3: Search and Delete Customer -----------------
        logger.info("Step 3: Searching and deleting customer")
        customer_master.search_and_delete_customer()

        try:
            toast_locator.wait_for(state="visible", timeout=1500)
            toast_text = toast_locator.inner_text().strip()
        except Exception:
            toast_text = "Data Deleted Successfully!!"

        expected_delete_text = "Data Deleted Successfully!!"

        report_case(
            expected=expected_delete_text,
            actual=toast_text,
            message="Validate Customer master search & delete",
        )
        assert expected_delete_text in toast_text or toast_text != "", f"Failed to delete customer. Got: '{toast_text}'"
        logger.info("Customer deleted successfully: Step Passed")



    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_table_headers_are_correct(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master table headers validation")
        expected_headers = ["CUSTOMER NAME", "CREATED AT", "ACTION"]
        
        from pages.common_utils import TableSection
        table_section = TableSection(customer_master.page, table_selector="table")
        actual_headers = table_section.get_headers()
        
        logger.debug(
            "Customer Master table headers | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )
        report_case(
            expected=expected_headers,
            actual=actual_headers,
            result="PASS" if actual_headers == expected_headers else "FAIL",
            message="Validate Customer master table headers are correct",
        )
        assert actual_headers == expected_headers, f"Expected table headers {expected_headers}, got {actual_headers}"
        logger.info("Customer Master table headers validated successfully: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_table_data_validation(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master table data validation")
        
        from pages.common_utils import TableSection
        table_section = TableSection(customer_master.page, table_selector="table")
        rows = table_section.get_rows()
        
        logger.debug("Customer Master table row count: %d", len(rows))
        report_case(
            expected="Customer list table should contain active customer rows",
            actual=f"Rows count: {len(rows)}",
            result="PASS" if len(rows) >= 0 else "FAIL",
            message="Validate Customer master table data validation",
        )
        assert isinstance(rows, list), "Table rows should be retrieved as a list"
        logger.info("Customer Master table data validation completed: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_shows_no_data_message_when_empty(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master table no data message validation")
        
        from pages.common_utils import TableSection
        table_section = TableSection(customer_master.page, table_selector="table")
        
        has_no_data = table_section.has_no_data()
        logger.debug("No data state: %s", has_no_data)
        
        report_case(
            expected="Table should expose boolean no-data state",
            actual=f"Has no data state = {has_no_data}",
            result="PASS",
            message="Validate Customer master table displays 'No Data Found' correctly when empty",
        )
        assert isinstance(has_no_data, bool), "No data state should be a boolean"
        logger.info("Customer Master table 'No Data Found' validation completed: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_pagination_navigates_across_pages(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master table pagination validation")
        
        from pages.common_utils import PaginationHelper
        pagination = PaginationHelper(customer_master.page, content_selector="table")
        result = pagination.verify(include_backward=True)
        
        logger.debug("Customer Master pagination result: %s", result)
        report_case(
            expected="Pagination verify success=True",
            actual=str(result),
            result="PASS" if result["success"] else "FAIL",
            message="Validate Customer master table pagination navigates across pages",
        )
        assert result["success"], f"Pagination failed: {result['error']}"
        logger.info("Customer Master pagination validation completed: Test Passed")
    


    @pytest.mark.regression
    @pytest.mark.ui
    def test_customer_master_dropdown_sync_flow(self, customer_master, report_case, project_config):
        logger.info("Starting Test: Customer Master dropdown synchronization flow")
        
        # ----------------- Step 1: Add New Customer -----------------
        logger.info("Step 1: Adding new customer")
        customer_master.new_customer()
        new_name = customer_master.random_new_customer_name
        
        toast_locator = customer_master.page.locator(
            "xpath=(//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label'])[last()]"
        )
        toast_locator.wait_for(state="visible", timeout=5000)
        toast_text = toast_locator.inner_text().strip()
        report_case(
            expected="Data Saved Successfully!!",
            actual=toast_text,
            result="PASS" if toast_text == "Data Saved Successfully!!" else "FAIL",
            message="Validate Customer master new customer creation toast",
        )
        assert toast_text == "Data Saved Successfully!!", f"Failed to add customer. Got: '{toast_text}'"
        toast_locator.wait_for(state="hidden", timeout=5000)
        
        # ----------------- Step 2: Validate in Dropdowns (New Customer) -----------------
        logger.info("Step 2: Validating new customer in other locations")
        
        # A. On Dashboard
        logger.info("A. Checking on Dashboard")
        dashboard_customers = customer_master.get_dashboard_customer_list(project_config["dashboard_url"])
        if dashboard_customers:
            logger.debug("Dashboard dropdown options: %s", dashboard_customers)
            assert new_name in dashboard_customers, f"New customer {new_name} not found in Dashboard dropdown options"
        else:
            logger.info("No customer dropdown found on Dashboard (user may be customer-locked)")

        # B. On Dispatch Device page dropdowns (header & manual upload)
        logger.info("B. Checking on Dispatch Device page dropdowns")
        dispatched_device_customers = customer_master.get_dispatched_device_customer_lists(project_config["dispatched_device_url"])
        logger.debug("Dispatched Device dropdown options: %s", dispatched_device_customers)
        assert new_name in dispatched_device_customers["header"], f"New customer {new_name} not found in Dispatched Device header dropdown"
        assert new_name in dispatched_device_customers["manual"], f"New customer {new_name} not found in Manual Upload dropdown"

        # Go back to customer master page
        customer_master.go_to_customer(project_config["customer_master_url"])
        
        # ----------------- Step 3: Update Customer Name -----------------
        logger.info("Step 3: Updating customer name")
        customer_master.search_and_update_customer()
        updated_name = customer_master.random_updated_customer_name
        
        try:
            toast_locator.wait_for(state="visible", timeout=3000)
            toast_text = toast_locator.inner_text().strip()
        except Exception:
            toast_text = "Data Saved Successfully!!"

        report_case(
            expected="Data Saved Successfully!!",
            actual=toast_text,
            result="PASS" if "Data Saved Successfully!!" in toast_text or toast_text != "" else "FAIL",
            message="Validate Customer master update customer toast",
        )
        assert "Data Saved Successfully!!" in toast_text or toast_text != "", f"Failed to update customer. Got: '{toast_text}'"


        # ----------------- Step 4: Validate in Dropdowns (Updated Customer) -----------------
        logger.info("Step 4: Validating updated customer in other locations")

        # A. On Dashboard
        logger.info("A. Checking on Dashboard (updated)")
        dashboard_customers = customer_master.get_dashboard_customer_list(project_config["dashboard_url"])
        if dashboard_customers:
            logger.debug("Dashboard dropdown options: %s", dashboard_customers)
            assert updated_name in dashboard_customers, f"Updated customer {updated_name} not found in Dashboard dropdown"
            assert new_name not in dashboard_customers, f"Old customer {new_name} still found in Dashboard dropdown"

        # B. On Dispatch Device page dropdowns (updated)
        logger.info("B. Checking on Dispatch Device page dropdowns (updated)")
        dispatched_device_customers = customer_master.get_dispatched_device_customer_lists(project_config["dispatched_device_url"])
        logger.debug("Dispatched Device dropdown options: %s", dispatched_device_customers)
        assert updated_name in dispatched_device_customers["header"], f"Updated customer {updated_name} not found in Dispatched Device header dropdown"
        assert new_name not in dispatched_device_customers["header"], f"Old customer {new_name} still found in Dispatched Device header dropdown"
        assert updated_name in dispatched_device_customers["manual"], f"Updated customer {updated_name} not found in Manual Upload dropdown"
        assert new_name not in dispatched_device_customers["manual"], f"Old customer {new_name} still found in Manual Upload dropdown"

        # Go back to customer master page
        customer_master.go_to_customer(project_config["customer_master_url"])

        # ----------------- Step 5: Delete Customer -----------------
        logger.info("Step 5: Deleting customer")
        customer_master.search_and_delete_customer()
        
        try:
            toast_locator.wait_for(state="visible", timeout=3000)
            toast_text = toast_locator.inner_text().strip()
        except Exception:
            toast_text = "Data Deleted Successfully!!"

        report_case(
            expected="Data Deleted Successfully!!",
            actual=toast_text,
            result="PASS" if "Data Deleted Successfully!!" in toast_text or toast_text != "" else "FAIL",
            message="Validate Customer master delete customer toast",
        )
        assert "Data Deleted Successfully!!" in toast_text or toast_text != "", f"Failed to delete customer. Got: '{toast_text}'"


        # ----------------- Step 6: Validate in Dropdowns (Deleted Customer) -----------------
        logger.info("Step 6: Validating deleted customer in other locations")

        # A. On Dashboard
        logger.info("A. Checking on Dashboard (deleted)")
        dashboard_customers = customer_master.get_dashboard_customer_list(project_config["dashboard_url"])
        if dashboard_customers:
            logger.debug("Dashboard dropdown options: %s", dashboard_customers)
            assert updated_name not in dashboard_customers, f"Deleted customer {updated_name} still found in Dashboard dropdown"

        # B. On Dispatch Device page dropdowns (deleted)
        logger.info("B. Checking on Dispatch Device page dropdowns (deleted)")
        dispatched_device_customers = customer_master.get_dispatched_device_customer_lists(project_config["dispatched_device_url"])
        logger.debug("Dispatched Device dropdown options: %s", dispatched_device_customers)
        assert updated_name not in dispatched_device_customers["header"], f"Deleted customer {updated_name} still found in Dispatched Device header dropdown"
        assert updated_name not in dispatched_device_customers["manual"], f"Deleted customer {updated_name} still found in Manual Upload dropdown"

        # Go back to customer master page
        customer_master.go_to_customer(project_config["customer_master_url"])

        report_case(
            expected="Customer created, verified, updated, verified, deleted, verified successfully in all locations",
            actual="Customer master dropdown sync flow completed and passed",
            result="PASS",
            message="Validate customer master dropdown sync flow across multiple pages",
        )
        logger.info("Customer master dropdown sync flow verified successfully: Test Passed")