from pathlib import Path
from config.config import SIM_DATA_DETAILS_URL
from utils.logger import get_logger
import pytest

logger = get_logger(__name__)

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test_data" / "lct"


@pytest.mark.regression
@pytest.mark.lct
@pytest.mark.sampark
class TestSimBatchDataDetailsPage:
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

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_sim_batch_page_navigates_correctly(
        self, page, sim_data_details_page, report_case
    ):
        logger.info("Navigating to SIM Data Details page")
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        logger.debug(
            "SIM Data Details URL check | expected=%s | actual=%s",
            SIM_DATA_DETAILS_URL,
            page.url,
        )
        report_case(expected=SIM_DATA_DETAILS_URL, actual=page.url, message="Validate SIM batch page navigates correctly")
        assert (
            page.url == SIM_DATA_DETAILS_URL
        ), f"Expected URL to be '{SIM_DATA_DETAILS_URL}', got {page.url}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_title_is_correct(self, sim_data_details_page, report_case):
        logger.info("Asserting SIM Data Details title")
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        expected_title = "Sensorise SIM Data Details"
        actual_title = sim_data_details_page.get_title()
        logger.debug(
            "SIM Data Details title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )
        report_case(expected=expected_title, actual=actual_title, message="Validate SIM batch page title is correct")
        assert (
            actual_title == expected_title
        ), f"Expected title to be '{expected_title}', got '{actual_title}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_manual_upload_and_download_buttons_are_visible(
        self, sim_data_details_page, report_case
    ):
        logger.info("Validating manual upload and download buttons")
        assert (
            sim_data_details_page.is_manual_upload_button_visible()
        ), "Manual Upload button should be visible"
        assert (
            sim_data_details_page.is_download_sample_button_visible()
        ), "Download Sample button should be visible"
        manual_button_text = sim_data_details_page.get_manual_upload_button_text()
        download_button_text = sim_data_details_page.get_download_sample_button_text()
        logger.debug(
            "SIM action button text | manual=%s | download=%s",
            manual_button_text,
            download_button_text,
        )
        report_case(
            expected="Manual Upload and Download Sample buttons should be visible with correct text",
            actual=f"Manual='{manual_button_text}', Download='{download_button_text}'"
        , message="Validate SIM batch page manual upload and download buttons are visible")
        assert (
            "Manual Upload" in manual_button_text
        ), "Manual Upload button text mismatch"
        assert (
            "Download Sample" in download_button_text
        ), "Download Sample button text mismatch"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_manual_upload_form_shows_instructions(
        self, sim_data_details_page, report_case
    ):
        logger.info("Checking upload instruction and placeholder copy")
        expected_instruction = "Upload ICCID's to get SIM Data Details"
        actual_instruction = sim_data_details_page.get_upload_instruction_text()
        logger.debug(
            "SIM upload instruction check | expected=%s | actual=%s",
            expected_instruction,
            actual_instruction,
        )
        report_case(expected=expected_instruction, actual=actual_instruction, message="Validate SIM batch page manual upload form shows instructions")
        assert (
            actual_instruction == expected_instruction
        ), "Upload instruction text mismatch"
        # placeholder = sim_data_details_page.get_iccid_upload_placeholder()
        # assert "ICCID" in (placeholder or ""), "ICCID placeholder should mention ICCID"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_submit_button_is_disabled_initially(
        self, sim_data_details_page, report_case
    ):
        logger.info("Verifying submit button is disabled before upload")
        is_disabled = sim_data_details_page.is_submit_button_disabled()
        report_case(expected=True, actual=is_disabled, message="Validate SIM batch page submit button is disabled initially")
        assert is_disabled, "Submit button should be disabled before upload"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_manual_button_opens_upload_form(
        self, sim_data_details_page, report_case
    ):
        logger.info("Opening manual upload page")
        sim_data_details_page.click_manual_upload_button()
        logger.debug("Manual upload page URL: %s", sim_data_details_page.page.url)
        report_case(
            expected="URL should contain sensorise-sim-manual-upload",
            actual=sim_data_details_page.page.url
        , message="Validate SIM batch page manual button opens upload form")
        assert (
            "sensorise-sim-manual-upload" in sim_data_details_page.page.url
        ), f"Expected manual upload URL fragment in '{sim_data_details_page.page.url}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_manual_upload_form_shows_error_for_blank_input(
        self, sim_data_details_page, report_case
    ):
        logger.info("Validating blank input error message on manual upload form")
        expected_error_message = "This field is required and can't be only spaces."
        sim_data_details_page.click_manual_upload_button()
        actual_error_message = (
            sim_data_details_page.validate_blank_input_error_message()
        )
        logger.debug(
            "Blank ICCID error check | expected=%s | actual=%s",
            expected_error_message,
            actual_error_message,
        )
        report_case(expected=expected_error_message, actual=actual_error_message, message="Validate SIM batch page manual upload form shows error for blank input")
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_manual_upload_form_shows_error_for_20_character_input(
        self, sim_data_details_page, report_case
    ):
        """this error is for the less than 20 and more thann 20 characters"""
        logger.info("Checking error message for input exceeding 20 characters")
        expected_error_message = "Value must be exactly 20 characters long."
        sim_data_details_page.click_manual_upload_button()
        actual_error_message = (
            sim_data_details_page.validate_20_characters_error_message()
        )
        logger.debug(
            "ICCID length error check | expected=%s | actual=%s",
            expected_error_message,
            actual_error_message,
        )
        report_case(expected=expected_error_message, actual=actual_error_message, message="Validate SIM batch page manual upload form shows error for 20 character input")
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_submit_button_is_enabled_with_valid_input(
        self, sim_data_details_page, report_case
    ):
        logger.info("Ensuring submit button is enabled after valid input")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid(
            "89916450244842405755"
        )  # Example valid ICCID
        logger.debug("Entered valid ICCID for submit button enablement check")
        is_disabled = sim_data_details_page.is_submit_button_disabled()
        report_case(expected=False, actual=is_disabled, message="Validate SIM batch page submit button is enabled with valid input")
        assert not is_disabled, "Submit button should be enabled after valid input"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_submit_button_displays_table_results(
        self, sim_data_details_page, report_case
    ):
        logger.info("Testing that clicking submit opens the results table")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid(
            "89916450244842405755"
        )  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        logger.debug("Submitted valid ICCID and checking results table visibility")
        is_visible = sim_data_details_page.is_results_table_visible()
        report_case(expected=True, actual=is_visible, message="Validate SIM batch page submit button displays table results")
        assert (
            is_visible
        ), "Results table should be visible after submitting valid ICCID"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_table_header_is_visible_and_correct(
        self, sim_data_details_page, report_case
    ):
        logger.info("Verifying results table header is visible and correct")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid(
            "89916450244842405755"
        )  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        expected_header = (
            "Uploaded ICCID's Sensorise SIM Details List"  # Example expected headers
        )
        actual_headers = sim_data_details_page.get_results_table_component_header()
        logger.debug(
            "SIM results component header | expected=%s | actual=%s",
            expected_header,
            actual_headers,
        )
        report_case(expected=expected_header, actual=actual_headers, message="Validate SIM batch page table header is visible and correct")
        assert (
            actual_headers == expected_header
        ), f"Expected table headers to be {expected_header}, got {actual_headers}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_table_headers_are_correct(
        self, sim_data_details_page, report_case
    ):
        logger.info("Validating table headers")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid(
            "89916450244842405755"
        )  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        # ['ICCID', 'CARD STATE', 'CARD STATUS', 'PRIMARY TSP', 'FALLBACK TSP', 'PRIMARY STATUS', 'PRIMARY MSISDN', 'FALLBACK STATUS', 'FALLBACK MSISDN', 'ACTIVE PROFILES', 'CARD EXPIRY DATE', 'PRODUCT NAME', 'IS RSU REQUIRED', 'IS IMSI REQUIRED', 'ACTIVE SR NUMBER']
        expected_headers = [
            "ICCID",
            "CARD STATE",
            "CARD STATUS",
            "PRIMARY TSP",
            "FALLBACK TSP",
            "PRIMARY STATUS",
            "PRIMARY MSISDN",
            "FALLBACK STATUS",
            "FALLBACK MSISDN",
            "ACTIVE PROFILES",
            "CARD EXPIRY DATE",
            "PRODUCT NAME",
            "IS RSU REQUIRED",
            "IS IMSI REQUIRED",
            "ACTIVE SR NUMBER",
        ]
        actual_headers = sim_data_details_page.table_section.get_headers()
        logger.debug(
            "SIM results table headers | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )
        report_case(expected=expected_headers, actual=actual_headers, message="Validate SIM batch page table headers are correct")
        assert (
            actual_headers == expected_headers
        ), f"Expected table headers {expected_headers}, got {actual_headers}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_table_pagination_navigates_across_pages(
        self, sim_data_details_page, report_case
    ):
        logger.info("Executing pagination workflow")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid(
            "89916450244842405755"
        )  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        sim_data_details_page.table_section.wait_for_table()
        result = sim_data_details_page.pagination_helper.verify(include_backward=True)
        logger.debug("SIM results pagination result: %s", result)
        report_case(
            expected="Pagination success=True and pages visited in order",
            actual=result,
            message=result.get("error", ""),
        )
        assert result["success"], f"Pagination failed: {result['error']}"
        # assert result["total_pages"] > 1, "Pagination did not move beyond first page"
        assert result["pages_visited"] == sorted(
            result["pages_visited"]
        ), "Pages not in order"

    ## Batch upload test cases

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_batch_upload_validates_file_input(
        self, sim_data_details_page, report_case
    ):
        logger.info("Validating batch upload input")
        expected_error_message = "This field is mandatory."
        actual_error_message = (
            sim_data_details_page.validate_batch_upload_input_error_message()
        )
        logger.debug(
            "Batch upload input error check | expected=%s | actual=%s",
            expected_error_message,
            actual_error_message,
        )
        report_case(expected=expected_error_message, actual=actual_error_message, message="Validate SIM batch page batch upload validates file input")
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_download_sample_button_is_functional(
        self, sim_data_details_page, report_case
    ):
        logger.info("Testing Download Sample button functionality")

        download = sim_data_details_page.click_download_sample_button()
        logger.debug(
            "Sample download suggested filename: %s", download.suggested_filename
        )
        is_downloaded = sim_data_details_page.is_sample_file_downloaded(
            download=download, expected_filename="Sensorise_SIM_data_Details.xlsx"
        )
        report_case(
            expected="Sensorise_SIM_data_Details.xlsx should download successfully",
            actual=f"filename={download.suggested_filename}, downloaded={is_downloaded}"
        , message="Validate SIM batch page download sample button is functional")

        assert is_downloaded, "Sample file validation failed"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_submit_button_is_disabled_when_input_cleared(
        self, sim_data_details_page, report_case
    ):
        logger.info("Testing the submit button is disabled if no input")
        is_disabled = sim_data_details_page.is_submit_button_disabled_on_no_input()
        report_case(expected=True, actual=is_disabled, message="Validate SIM batch page submit button is disabled when input cleared")
        assert is_disabled, "Submit button should not be enabled"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sim_batch_page_submit_button_is_enabled_after_valid_file_upload(
        self, sim_data_details_page, report_case
    ):
        logger.info("Testing submit button enabled after valid file upload")
        file_path = str(TEST_DATA_DIR / "Sensorise_SIM_data_Details.xlsx")
        logger.debug("Uploading SIM data details file: %s", file_path)
        sim_data_details_page.upload_valid_file(file_path)  # Example valid file
        is_disabled = sim_data_details_page.is_submit_button_disabled_on_no_input()
        report_case(expected=False, actual=is_disabled, message="Validate SIM batch page submit button is enabled after valid file upload")
        assert (
            not is_disabled
        ), "Submit button should be enabled after valid file upload"

        if not sim_data_details_page.is_submit_button_disabled_on_no_input():
            sim_data_details_page.click_submit_button()
            assert (
                sim_data_details_page.is_results_table_visible()
            ), "Results table should be visible after submitting valid file"
