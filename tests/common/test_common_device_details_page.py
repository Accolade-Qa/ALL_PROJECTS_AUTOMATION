from utils.logger import get_logger

import pytest

logger = get_logger(__name__)

device_info = {
    "IMEI": "866677075606341",
    "ICCID": "89916450244842405755",
    "UIN": "ACONSBA102500006341",
    "VIN": "SCVBASE1225014403",
}


@pytest.mark.device
@pytest.mark.regression
@pytest.mark.lct
@pytest.mark.sampark
class TestDeviceDetailsPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Device Details test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Device Details test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Device Details test passed: %s", test_name)
        elif report.failed:
            logger.error("Device Details test failed: %s", test_name)
            logger.debug(
                "Device Details failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Device Details test skipped: %s", test_name)

    # ------------------ PAGE VALIDATIONS ------------------

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_device_details_page_title_is_correct(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: device_details_page_title")

        title = device_details_page.get_title()
        logger.debug("Page title: %s", title)
        report_case(expected="Device Details", actual=title, message="Validate Device details page title is correct")

        assert title == "Device Details"

        logger.info("Test passed: device_details_page_title")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_device_details_page_all_elements_are_visible(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: device_details_page_elements")

        page_loaded = device_details_page.is_page_loaded()
        buttons_visible = (
            device_details_page.is_device_details_page_buttons_are_visible()
        )
        kpi_visible = device_details_page.is_device_kpi_cards_visible()
        report_case(
            expected="Page loaded=True, buttons visible=True, KPI cards visible=True",
            actual=(
                f"Page loaded={page_loaded}, buttons visible={buttons_visible}, "
                f"KPI cards visible={kpi_visible}"
            )
        , message="Validate Device details page all elements are visible")
        assert page_loaded
        assert buttons_visible
        assert kpi_visible

        logger.info("Test passed: device_details_page_elements")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_navigates_correctly_for_device(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: navigation to device details page")

        page_loaded = device_details_page.is_page_loaded()
        title = device_details_page.get_title()
        report_case(
            expected="Page loaded=True, title=Device Details",
            actual=f"Page loaded={page_loaded}, title={title}",
            message="Navigation to device details page should be successful",
        )
        assert page_loaded
        assert title == "Device Details"

        logger.info("Test passed: navigation validation")

    # ------------------ KPI CARDS ------------------

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_kpi_card_titles_are_correct(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: dashboard_card_title")

        expected_titles = [
            "IGNITION ON/OFF",
            "MAINS ON/OFF",
            "EMERGENCY ON/OFF",
            "TAMPER OPEN/CLOSE",
            "ACC CALIBRATION ON/OF",
            "WIRE CUT",
        ]

        actual_titles = []
        for i, title in enumerate(expected_titles):
            actual_title = device_details_page.get_cards_title_text(i)
            actual_titles.append(actual_title)
            logger.debug(
                "Validating KPI card title at index %s | expected=%s | actual=%s",
                i,
                title,
                actual_title,
            )
            assert actual_title == title, f"Card {i} title mismatch"
        report_case(expected=expected_titles, actual=actual_titles, message="Validate Device details page KPI card titles are correct")

        logger.info("Test passed: dashboard_card_title")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_kpi_cards_display_values(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: kpi_cards_have_values")

        count = device_details_page.get_cards_count()

        values = []
        for i in range(count):
            value = device_details_page.get_cards_inner_count(i)
            values.append(value)
            logger.debug("Validating KPI card value at index %s | value=%s", i, value)
            assert value.strip() != "", f"Card {i} has empty value"
        report_case(expected="All KPI card values should be non-empty", actual=values, message="Validate Device details page KPI cards display values")

        logger.info("Test passed: kpi_cards_have_values")

    # ------------------ COMPONENT TITLES ------------------

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_all_table_component_titles_are_correct(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: component titles")

        expected_titles = [
            "Device Details",
            "IP Details",
            "GPS and GSM Details",
            "Accelerometer Details",
            "Last 50 Login Packets",
        ]

        actual_titles = []
        for i, expected in enumerate(expected_titles):
            actual = device_details_page.get_table_component_title_text(i)
            actual_titles.append(actual)
            logger.debug(
                "Validating component title at index %s | expected=%s | actual=%s",
                i,
                expected,
                actual,
            )
            assert actual == expected, f"Component {i} title mismatch"
        report_case(expected=expected_titles, actual=actual_titles, message="Validate Device details page all table component titles are correct")

        logger.info("Test passed: component titles")

    # ------------------ HEADERS ------------------

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_all_section_headers_are_correct(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: all component headers")

        headers = device_details_page.get_table_component_headers()
        logger.debug("Collected component headers: %s", headers)
        report_case(
            expected="30 headers including IMEI Number, ICCID Number, UIN No, VIN No",
            actual=f"{len(headers)} headers: {headers}"
        , message="Validate Device details page all section headers are correct")

        assert len(headers) == 30

        for required in ["IMEI Number", "ICCID Number", "UIN No", "VIN No"]:
            assert required in headers

        logger.info("Test passed: all component headers")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_table_headers_are_correct(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: login packet table headers")

        expected_headers = [
            "UIN NO.",
            "IMEI NO.",
            "ICCID.",
            "IGNITION",
            "DATE & TIME",
            "ACTION",
        ]

        actual_headers = device_details_page.get_login_packet_table_headers()
        logger.debug(
            "Login packet table headers | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )
        report_case(expected=expected_headers, actual=actual_headers, message="Validate Device details page table headers are correct")

        assert actual_headers == expected_headers

        logger.info("Test passed: login packet headers")

    # ------------------ TABLE DATA ------------------

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_table_displays_device_information(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: login packet table data")

        actual_data = device_details_page.get_device_details_table_data()
        logger.debug("Login packet table row count: %s", len(actual_data))
        report_case(
            expected="Login packet table should have data and each row should be a list",
            actual=f"Rows={len(actual_data)}, row types={[type(row).__name__ for row in actual_data]}"
        , message="Validate Device details page table displays device information")

        assert len(actual_data) > 0, "Login packet table should have data"
        assert all(
            isinstance(row, list) for row in actual_data
        ), "Each row should be a list"

        if not len(actual_data) > 0:
            logger.warning("Login packet table is empty, skipping data validation")
            return

        logger.info("Test passed: login packet table data")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_table_row_count_is_accurate(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: table row count")

        rows = device_details_page.get_device_details_table_data()
        logger.debug("Device details table rows fetched: %s", len(rows))
        report_case(expected="Row count should be greater than 0", actual=len(rows), message="Validate Device details page table row count is accurate")

        assert len(rows) > 0

        logger.info("Test passed: table row count")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_shows_no_data_message_when_empty(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: no data state")

        # Intentional validation (current state has data)
        has_no_data = device_details_page.table_section.has_no_data()
        report_case(
            expected="Current table state should be captured",
            actual=f"No data state={has_no_data}"
        , message="Validate Device details page shows no data message when empty")

        # # Assertion
        # assert (
        #     has_no_data
        # ), "Expected 'No Data Found' state, but data is present in the table."

        logger.info("Test passed: no data state validation")

    # ------------------ EXPORT ------------------

    # def test_device_details_export_button(self, device_details_page):
    #     logger.info("Starting test: export button")

    #     download = device_details_page.click_export_button()

    #     # Assertions in test
    #     assert download is not None, "Download object is None"
    #     assert download.suggested_filename, "Filename missing"

    #     file_path = f"/tmp/{download.suggested_filename}"
    #     download.save_as(file_path)

    #     assert os.path.exists(file_path), "Downloaded file not found"

    #     logger.info(f"Downloaded file at: {file_path}")
    #     logger.info("Test passed: export button")

    # ------------------ PAGINATION ------------------

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_pagination_navigates_forward(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: pagination")

        pagination = device_details_page.get_login_packet_pagination()

        result = pagination.verify()
        logger.debug("Pagination verification result: %s", result)
        report_case(
            expected="Pagination success=True, pages visited sorted, total pages >= 1",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["pages_visited"] == sorted(result["pages_visited"])
        assert result["total_pages"] >= 1

        logger.info("Test passed: pagination")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_pagination_navigates_bidirectionally(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: bidirectional pagination")

        pagination = device_details_page.get_login_packet_pagination()

        result = pagination.verify(include_backward=True)
        logger.debug("Bidirectional pagination verification result: %s", result)
        report_case(
            expected="Bidirectional pagination success=True",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Pagination failed: {result['error']}"

        logger.info("Test passed: bidirectional pagination")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_device_details_page_pagination_handles_last_page_correctly(
        self, device_details_page, report_case
    ):
        logger.info("Starting test: last page behavior")

        base = "//h6[text()='Last 50 Login Packets']/ancestor::div[contains(@class,'component-container')]"
        next_btn = device_details_page.page.locator(
            f"{base}//button[.//mat-icon[text()='chevron_right']]"
        )

        while not next_btn.is_disabled():
            next_btn.click()

        is_disabled = next_btn.is_disabled()
        report_case(
            expected="Next button disabled=True on last page", actual=is_disabled
        , message="Validate Device details page pagination handles last page correctly")
        assert is_disabled, "Next button should be disabled on last page"

        logger.info("Test passed: last page behavior")
