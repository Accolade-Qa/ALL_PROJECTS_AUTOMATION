import pytest
import json

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
class TestTmlRequestLogPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting TML Request Log test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "TML Request Log test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("TML Request Log test passed: %s", test_name)
        elif report.failed:
            logger.error("TML Request Log test failed: %s", test_name)
            logger.debug(
                "TML Request Log failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("TML Request Log test skipped: %s", test_name)


    # test that the page is loaded successfully
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_loaded(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page load")

        is_loaded = tml_request_log_page.is_page_loaded()

        report_case(
            expected="TML Request Log page should load successfully",
            actual=f"page_loaded={is_loaded}"
        , message="Validate TML request log page loaded")

        assert is_loaded, "TML Request Log page is not loaded"

    # test that the page title is correct when page is loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_title(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page title")

        title = tml_request_log_page.get_title()

        report_case(
            expected="TML Request Log page title should be correct",
            actual=f"page_title={title}"
        , message="Validate TML request log page title")

        assert (
            title == "AIS140 Ticket TML Request Logs"
        ), f"TML Request Log page title is incorrect: {title}"

    # test that the first data in the table is equal with the sent request payload
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_tml_request_log_page_payload_validation_on_ui(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log payload on UI")

        # Trigger API and fetch request payload
        (
            api_payload,
            expected_vin,
            expected_uin,
            expected_iccid,
            ticket_number,
            _ ,
        ) = tml_request_log_page.get_tml_request_payload_by_api()

        # API payload is returned as list[dict]
        expected_dict = (
            api_payload[0]
            if isinstance(api_payload, list) and len(api_payload) > 0
            else api_payload
        )

        payload_found = False
        ui_payloads = []

        # Attempt to find the payload on the UI, reloading up to 3 times with a short sleep
        import time

        for attempt in range(4):
            if attempt > 0:
                logger.info(
                    "Payload not found on attempt %s. Reloading page and retrying...",
                    attempt,
                )
                tml_request_log_page.page.reload()
                tml_request_log_page.is_page_loaded()
                time.sleep(2)

            # Read latest UI payloads
            ui_payloads = tml_request_log_page.get_tml_request_payload_by_ui()

            logger.debug(
                "UI Payload Count: %s | Ticket No: %s (Attempt %s)",
                len(ui_payloads),
                ticket_number,
                attempt + 1,
            )

            for payload in ui_payloads:
                try:
                    ui_json = json.loads(payload)
                    if isinstance(ui_json, list) and len(ui_json) > 0:
                        ui_json = ui_json[0]

                    if ui_json == expected_dict:
                        payload_found = True
                        logger.info("Matching payload found in UI.")
                        break
                    else:
                        # Log discrepancy for debugging
                        logger.debug("Payload mismatch details:")
                        logger.debug("Expected: %s", expected_dict)
                        logger.debug("Actual: %s", ui_json)

                except Exception as exc:
                    logger.warning("Unable to parse UI payload: %s", exc)

            if payload_found:
                break

        report_case(
            expected="Latest UI payload should match the API request payload",
            actual=f"ui_payload_count={len(ui_payloads)}, ticket_number={ticket_number}"
        , message="Validate TML request log page payload validation on ui")

        assert ui_payloads, "No payloads found in the TML Request Log table."

        assert (
            payload_found
        ), "The API request payload was not found in the UI payload column."

        logger.info(
            "Payload validation completed successfully. VIN=%s, UIN=%s, ICCID=%s",
            expected_vin,
            expected_uin,
            expected_iccid,
        )

    # test that the search functionality is working as expected
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_search(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page search functionality")

        (
            _,
            expected_vin,
            _,
            _,
            _,
            _,
        ) = tml_request_log_page.get_tml_request_payload_by_api()

        search_result = tml_request_log_page.search_logs(expected_vin)

        logger.debug(
            "Search Result: success=%s, results_found=%s",
            search_result["success"],
            search_result["results_found"],
        )

        report_case(
            expected=f"Search should return records for VIN '{expected_vin}'",
            actual=(
                f"success={search_result['success']}, "
                f"results_found={search_result['results_found']}"
            )
        , message="Validate TML request log page search")

        assert search_result[
            "success"
        ], f"Search operation failed: {search_result['error']}"

        assert (
            search_result["results_found"] > 0
        ), f"No records found for VIN '{expected_vin}'."

        assert any(
            expected_vin.lower() in row.lower() for row in search_result["results"]
        ), f"VIN '{expected_vin}' not found in search results."

        logger.info("Search validation completed successfully.")

    # test that the table headers are showned is correct
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tml_request_log_page_table_headers(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page table headers")

        expected_headers = [
            "VIN NO.",
            "ICCID NO.",
            "UIN NO.",
            "SENT BY",
            "RESPONSE",
            "PAYLOAD",
            "SENT AT",
        ]

        actual_headers = tml_request_log_page.get_table_headers()

        logger.debug("Expected headers: %s", expected_headers)
        logger.debug("Actual headers: %s", actual_headers)

        report_case(
            expected=f"Table headers should match: {expected_headers}",
            actual=f"headers={actual_headers}"
        , message="Validate TML request log page table headers")

        # Validate the number of headers
        assert len(actual_headers) == len(expected_headers), (
            f"Expected {len(expected_headers)} headers, "
            f"but found {len(actual_headers)}."
        )

        # Validate the exact headers
        assert actual_headers == expected_headers, (
            f"Table headers do not match.\n"
            f"Expected: {expected_headers}\n"
            f"Actual: {actual_headers}"
        )

        logger.info("TML Request Log table headers validated successfully.")


    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tml_request_log_page_table_data(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page table data")

        sent_by, institutional_sale = tml_request_log_page.get_table_data()

        logger.debug("SENT_BY: %s", sent_by)
        logger.debug("INSTITUTIONAL_SALE_FROM: %s", institutional_sale)

        if institutional_sale == "Y":
            expected_sent_by = "Institutional Sales"

        else:
            expected_sent_by = "Generate Tickets API"
    

        report_case(
            expected=f"SENT_BY should be '{expected_sent_by}' based on INSTITUTIONAL_SALE_FROM value '{institutional_sale}'",
            actual=f"SENT_BY={sent_by}, INSTITUTIONAL_SALE_FROM={institutional_sale}"
        , message="Validate TML request log page table data")

        assert (
            sent_by == expected_sent_by
        ), f"SENT_BY value does not match. Expected: {expected_sent_by}, Actual: {sent_by}"

        logger.info("TML Request Log table data validated successfully.")


    # test that the pagination is working as expected
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_pagination(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating pagination on the TML Request Log page")

        pagination_result = tml_request_log_page.validate_pagination()

        logger.debug(
            "Pagination Result: success=%s, pages_visited=%s, total_pages=%s, error=%s",
            pagination_result["success"],
            pagination_result["pages_visited"],
            pagination_result["total_pages"],
            pagination_result["error"],
        )

        report_case(
            expected="Pagination should navigate correctly across all available pages",
            actual=(
                f"success={pagination_result['success']}, "
                f"pages_visited={pagination_result['pages_visited']}, "
                f"total_pages={pagination_result['total_pages']}, "
                f"error={pagination_result['error']}"
            )
        , message="Validate TML request log page pagination")

        # Pagination verification should succeed
        assert pagination_result[
            "success"
        ], f"Pagination validation failed: {pagination_result['error']}"

        # At least one page should always be visited
        assert (
            len(pagination_result["pages_visited"]) > 0
        ), "No pages were visited during pagination validation."

        # The first visited page should always be page 1
        assert pagination_result["pages_visited"][0] == 1, (
            f"Pagination should start from page 1, but started from "
            f"{pagination_result['pages_visited'][0]}."
        )

        # The number of visited pages should never exceed the total pages
        assert (
            len(pagination_result["pages_visited"]) <= pagination_result["total_pages"]
        ), "Visited pages exceed the total page count."

        logger.info("Pagination validated successfully.")

    # after all these test cases validate that the by rto state and vehicle owner state is in the given state array then check does it add the fota batch on the ui or not.
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_tml_request_log_page_fota_batch_addition(
        self,
        tml_request_log_page,
        project_config,
        report_case,
    ):
        logger.info("Validating Auto FOTA batch creation")

        (
            api_payload,
            _,
            _,
            _,
            ticket_number,
            _,
        ) = tml_request_log_page.get_tml_request_payload_by_api()

        expected_payload = (
            api_payload[0] if isinstance(api_payload, list) else api_payload
        )

        state_name = expected_payload.get("VEHICLE_OWNER_STATE", "").strip()

        vehicle_owner_states = {
            "Haryana",
            "Assam",
            "Andhra Pradesh",
            "Jammu & Kashmir",
            "Punjab",
            "Nagaland",
            "Gujarat",
            "Daman and Diu",
            "Dadra and Nagar Haveli",
            "Jharkhand",
        }

        conditions_met = state_name in vehicle_owner_states

        if conditions_met:
            batch_added = tml_request_log_page.check_fota_batch_on_ui(
                project_config=project_config,
                ticket_number=ticket_number,
                state_name=state_name,
            )
        else:
            batch_added = False

        report_case(
            expected="FOTA batch should be created only for eligible states",
            actual=(
                f"state={state_name}, "
                f"conditions_met={conditions_met}, "
                f"batch_added={batch_added}"
            )
        , message="Validate TML request log page FOTA batch addition")

        if conditions_met:
            assert batch_added, f"Auto FOTA batch not created for state '{state_name}'."
        else:
            assert (
                not batch_added
            ), f"Batch should not be created for state '{state_name}'."

        logger.info("Auto FOTA batch validation completed successfully.")

    @pytest.mark.smoke
    @pytest.mark.skip(
        reason="This test is currently skipped due to it being resource-intensive and may cause instability in the test environment. "
        "It can be enabled for dedicated performance testing."
    )
    @pytest.mark.api
    @pytest.mark.regression
    def test_tml_request_log_page_concurrent_ticket_generation_uniqueness(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating simultaneous ticket generation")

        result = tml_request_log_page.create_multiple_tickets_concurrently()

        report_case(
            expected="All concurrent requests should generate unique ticket numbers",
            actual=(
                f"Generated={len(result['tickets'])}, "
                f"Failed={len(result['failed_requests'])}, "
                f"Duplicates={len(result['duplicates'])}"
            )
        , message="Validate Concurrent multiple ticket generation uniqueness")

        assert not result[
            "failed_requests"
        ], f"Failed Requests: {result['failed_requests']}"

        assert not result["duplicates"], f"Duplicate Tickets: {result['duplicates']}"

        assert result["tickets"], "No tickets were generated."
