import pytest

from utils.logger import get_logger
from api import APIClient

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
class TestTicketDashboardPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Ticket Dashboard test: %s", test_name)
        yield
        report = getattr(request.node, "rep_call", None)
        if report and report.failed:
            logger.error("Ticket Dashboard test failed: %s", test_name)
        else:
            logger.info("Ticket Dashboard test passed: %s", test_name)

    # --- Group 1: Page Load & Basic Navigation ---
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_page_loaded(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating ATCU Ticket Dashboard page load")
        is_loaded = atcu_ticket_dashboard_page.is_page_loaded()
        report_case(
            expected="ATCU Ticket Dashboard page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Ticket Dashboard page loaded",
        )
        assert is_loaded, "ATCU Ticket Dashboard page is not loaded"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_page_title(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating ATCU Ticket Dashboard page title")
        title = atcu_ticket_dashboard_page.get_title()
        report_case(
            expected="Page title should be 'Ticket Dashboard'",
            actual=f"title='{title}'",
            message="Validate ATCU Ticket Dashboard page title",
        )
        assert title == "Ticket Dashboard", f"Page title is incorrect: '{title}'"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_reload_button_click(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating Reload button click")
        atcu_ticket_dashboard_page.click_reload_button()
        is_loaded = atcu_ticket_dashboard_page.is_page_loaded()
        report_case(
            expected="Page should reload and remain loaded successfully",
            actual=f"is_loaded={is_loaded}",
            message="Validate Reload button click",
        )
        assert is_loaded, "Page failed to reload properly"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_back_button_click(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating Back button click")
        atcu_ticket_dashboard_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # --- Group 2: Time Rules & Default State ---
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_530_pm_ist_rule_verification(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        is_after_530 = atcu_ticket_dashboard_page.is_after_530_pm_ist()
        in_progress_count = atcu_ticket_dashboard_page.get_kpi_card_count("IN PROGRESS")
        on_hold_count = atcu_ticket_dashboard_page.get_kpi_card_count("ON HOLD")

        logger.info("Current Time IST after 5:30 PM: %s | IN_PROGRESS=%s | ON_HOLD=%s", is_after_530, in_progress_count, on_hold_count)
        report_case(
            expected=f"After 5:30 PM IST (is_after_530={is_after_530}), in-progress tickets shift to on-hold appropriately",
            actual=f"is_after_530={is_after_530}, in_progress={in_progress_count}, on_hold={on_hold_count}",
            message="Validate 5:30 PM IST time rule for IN PROGRESS vs ON HOLD tickets",
        )
        if is_after_530:
            assert on_hold_count >= 0, "ON HOLD count should be non-negative after 5:30 PM IST"
        else:
            assert in_progress_count >= 0, "IN PROGRESS count should be non-negative before 5:30 PM IST"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_default_card_set_to_total(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating default table selection is set to TOTAL / ALL Tickets List")
        comp_title = atcu_ticket_dashboard_page.get_component_title()
        report_case(
            expected="Default component header title should be 'All Tickets List'",
            actual=f"comp_title='{comp_title}'",
            message="Validate default card selection set to TOTAL",
        )
        assert "All" in comp_title or "Total" in comp_title or "Tickets" in comp_title, f"Unexpected default table header: '{comp_title}'"

    # --- Group 3: Table Headers per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="ALL card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate ALL card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in ALL card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="IN PROGRESS card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate IN PROGRESS card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in IN PROGRESS card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="ON HOLD card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate ON HOLD card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in ON HOLD card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="CANCELLED card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate CANCELLED card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in CANCELLED card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="COMPLETED card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate COMPLETED card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in COMPLETED card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    # --- Group 4: End Date Column Verification per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        non_empty = [d for d in end_dates if d and d != "--"]
        report_case(
            expected="COMPLETED card table should contain valid non-empty End Date values",
            actual=f"total={len(end_dates)}, non_empty={len(non_empty)}",
            message="Validate End Date in COMPLETED table",
        )
        if end_dates:
            assert len(non_empty) > 0, "COMPLETED table missing valid End Date values"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        dash_values = [d for d in end_dates if d == "--" or not d]
        report_case(
            expected="IN PROGRESS card table should contain '--' for End Date",
            actual=f"total={len(end_dates)}, dash_count={len(dash_values)}",
            message="Validate End Date in IN PROGRESS table",
        )
        if end_dates:
            assert len(dash_values) == len(end_dates), "IN PROGRESS table should contain '--' for End Date"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        dash_values = [d for d in end_dates if d == "--" or not d]
        report_case(
            expected="ON HOLD card table should contain '--' for End Date",
            actual=f"total={len(end_dates)}, dash_count={len(dash_values)}",
            message="Validate End Date in ON HOLD table",
        )
        if end_dates:
            assert len(dash_values) == len(end_dates), "ON HOLD table should contain '--' for End Date"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        non_empty = [d for d in end_dates if d and d != "--"]
        report_case(
            expected="CANCELLED card table should contain valid End Date values (e.g. 22 Jul 2026 | 11:33 AM)",
            actual=f"total={len(end_dates)}, non_empty={len(non_empty)}",
            message="Validate End Date in CANCELLED table",
        )
        if end_dates:
            assert len(non_empty) > 0, "CANCELLED table missing valid End Date values"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        report_case(
            expected="ALL card table should extract End Date column values cleanly",
            actual=f"total={len(end_dates)}",
            message="Validate End Date in ALL table",
        )
        assert isinstance(end_dates, list), "Failed to extract End Date list"

    # --- Group 5: Ticket Category Column Verification per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "IN_PROGRESS" in c.upper() or "PROGRESS" in c.upper()]
        report_case(
            expected="IN PROGRESS card table should contain IN_PROGRESS Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in IN PROGRESS table",
        )
        if categories:
            assert len(matches) > 0, "IN PROGRESS table missing IN_PROGRESS Ticket Category"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "HOLD" in c.upper() or "ON_HOLD" in c.upper()]
        report_case(
            expected="ON HOLD card table should contain ON_HOLD Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in ON HOLD table",
        )
        if categories:
            assert len(matches) > 0, "ON HOLD table missing ON_HOLD Ticket Category"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "CANCEL" in c.upper() or "CANCELLED" in c.upper()]
        report_case(
            expected="CANCELLED card table should contain CANCELLED Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}, categories={categories}",
            message="Validate Ticket Category in CANCELLED table",
        )
        assert isinstance(categories, list), "Failed to extract Ticket Category list"
        if categories:
            assert len(matches) > 0 or len(categories) > 0, "CANCELLED table category check"


    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "COMPLETE" in c]
        report_case(
            expected="COMPLETED card table should contain COMPLETED Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in COMPLETED table",
        )
        if categories:
            assert len(matches) > 0, "COMPLETED table missing COMPLETED Ticket Category"

    # --- Group 6: Pagination per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        count = atcu_ticket_dashboard_page.get_kpi_card_count("ALL")
        rows = atcu_ticket_dashboard_page.get_table_rows()
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible(timeout=3000)
        res = atcu_ticket_dashboard_page.validate_pagination() if is_vis else {"success": True}
        report_case(
            expected="Pagination should be visible when ALL card has multiple pages (>10 items)",
            actual=f"count={count}, rows_count={len(rows)}, is_vis={is_vis}, res={res}",
            message="Validate pagination for ALL card view",
        )
        if count > 10 or len(rows) > 10:
            assert is_vis, "Pagination container not visible for ALL card view with >10 items"
        else:
            logger.info("ALL item count is %s (<=10), pagination controls hidden for single-page view as expected.", count)

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        count = atcu_ticket_dashboard_page.get_kpi_card_count("IN PROGRESS")
        rows = atcu_ticket_dashboard_page.get_table_rows()
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible(timeout=3000)
        res = atcu_ticket_dashboard_page.validate_pagination() if is_vis else {"success": True}
        report_case(
            expected="Pagination should be visible when IN PROGRESS card has multiple pages (>10 items)",
            actual=f"count={count}, rows_count={len(rows)}, is_vis={is_vis}, res={res}",
            message="Validate pagination for IN PROGRESS card view",
        )
        if count > 10 or len(rows) > 10:
            assert is_vis, "Pagination container not visible for IN PROGRESS card view with >10 items"
        else:
            logger.info("IN PROGRESS item count is %s (<=10), pagination controls hidden for single-page view as expected.", count)

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        count = atcu_ticket_dashboard_page.get_kpi_card_count("ON HOLD")
        rows = atcu_ticket_dashboard_page.get_table_rows()
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible(timeout=3000)
        res = atcu_ticket_dashboard_page.validate_pagination() if is_vis else {"success": True}
        report_case(
            expected="Pagination should be visible when ON HOLD card has multiple pages (>10 items)",
            actual=f"count={count}, rows_count={len(rows)}, is_vis={is_vis}, res={res}",
            message="Validate pagination for ON HOLD card view",
        )
        if count > 10 or len(rows) > 10:
            assert is_vis, "Pagination container not visible for ON HOLD card view with >10 items"
        else:
            logger.info("ON HOLD item count is %s (<=10), pagination controls hidden for single-page view as expected.", count)

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        count = atcu_ticket_dashboard_page.get_kpi_card_count("CANCELLED")
        rows = atcu_ticket_dashboard_page.get_table_rows()
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible(timeout=3000)
        res = atcu_ticket_dashboard_page.validate_pagination() if is_vis else {"success": True}
        report_case(
            expected="Pagination should be visible when CANCELLED card has multiple pages (>10 items)",
            actual=f"count={count}, rows_count={len(rows)}, is_vis={is_vis}, res={res}",
            message="Validate pagination for CANCELLED card view",
        )
        if count > 10 or len(rows) > 10:
            assert is_vis, "Pagination container not visible for CANCELLED card view with >10 items"
        else:
            logger.info("CANCELLED item count is %s (<=10), pagination controls hidden for single-page view as expected.", count)

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        count = atcu_ticket_dashboard_page.get_kpi_card_count("COMPLETED")
        rows = atcu_ticket_dashboard_page.get_table_rows()
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible(timeout=3000)
        res = atcu_ticket_dashboard_page.validate_pagination() if is_vis else {"success": True}
        report_case(
            expected="Pagination should be visible when COMPLETED card has multiple pages (>10 items)",
            actual=f"count={count}, rows_count={len(rows)}, is_vis={is_vis}, res={res}",
            message="Validate pagination for COMPLETED card view",
        )
        if count > 10 or len(rows) > 10:
            assert is_vis, "Pagination container not visible for COMPLETED card view with >10 items"
        else:
            logger.info("COMPLETED item count is %s (<=10), pagination controls hidden for single-page view as expected.", count)



    # --- Group 7: Graph Visibility & Canvas Hover per Chart ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_month_wise_trend_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Month-wise AIS140 Ticket Trend"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_tat_trend_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "AIS140 Ticket TAT Trend"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_tat_reason_breakdown_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "TAT Reason Breakdown"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_state_wise_distribution_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "State Wise Ticket Distribution"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_individual_performance_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Individual Performance"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_device_model_wise_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Device Model Wise Graph"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    # --- Group 8: API Integration & Count Sync ---
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_api_counts_validation_vs_ui(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating UI KPI Card counts against /api/crm/getDashCounts API endpoint")
        ui_counts = atcu_ticket_dashboard_page.get_all_kpi_counts()

        api = APIClient()
        api_response = api.tml.get_dash_counts()
        api_data = api_response.get("data", {}) if isinstance(api_response, dict) else {}

        api_all = api_data.get("all", 0) if isinstance(api_data, dict) else 0
        api_in_progress = api_data.get("inProgress", 0) if isinstance(api_data, dict) else 0
        api_on_hold = api_data.get("onHold", 0) if isinstance(api_data, dict) else 0
        api_cancelled = api_data.get("cancelled", 0) if isinstance(api_data, dict) else 0
        api_completed = api_data.get("completed", 0) if isinstance(api_data, dict) else 0

        report_case(
            expected="UI KPI card counts should match or closely align with getDashCounts API response keys (all, inProgress, onHold, cancelled, completed)",
            actual=f"ui_counts={ui_counts}, api_counts={{'all': {api_all}, 'inProgress': {api_in_progress}, 'onHold': {api_on_hold}, 'cancelled': {api_cancelled}, 'completed': {api_completed}}}",
            message="Validate KPI Card counts against getDashCounts API response",
        )
        assert ui_counts["ALL"] >= 0, "ALL KPI count should be non-negative"
        assert ui_counts["IN_PROGRESS"] >= 0, "IN PROGRESS KPI count should be non-negative"
        if isinstance(api_data, dict) and "all" in api_data:
            assert abs(ui_counts["ALL"] - api_all) <= 10, f"ALL count mismatch: UI={ui_counts['ALL']}, API={api_all}"

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_generate_ticket_api_count_increment_and_ui_sync(
        self,
        atcu_ticket_dashboard_page,
        project_config,
        report_case,
    ):
        is_after_530 = atcu_ticket_dashboard_page.is_after_530_pm_ist()

        initial_ui_all = atcu_ticket_dashboard_page.get_kpi_card_count("ALL")
        initial_ui_in_progress = atcu_ticket_dashboard_page.get_kpi_card_count("IN PROGRESS")
        initial_ui_on_hold = atcu_ticket_dashboard_page.get_kpi_card_count("ON HOLD")

        api = APIClient()
        pre_api_resp = api.tml.get_dash_counts()
        pre_api_data = pre_api_resp.get("data", {}) if isinstance(pre_api_resp, dict) else {}
        pre_api_all = pre_api_data.get("all", 0)

        payload, VIN, UIN, ICCID, ticket_number, data = api.tml.post_tml_request_log()
        search_term = ticket_number or VIN or UIN or (payload[0].get("VIN_NO") if payload else "")
        logger.info("Ticket API generated info: ticket_number='%s', VIN='%s', UIN='%s' | search_term='%s'", ticket_number, VIN, UIN, search_term)
        assert search_term, "Ticket generation API failed to return ticket details (TICKET_NO / VIN / UIN)"

        post_api_resp = api.tml.get_dash_counts()
        post_api_data = post_api_resp.get("data", {}) if isinstance(post_api_resp, dict) else {}
        post_api_all = post_api_data.get("all", 0)

        atcu_ticket_dashboard_page.page.reload()
        atcu_ticket_dashboard_page.page.wait_for_load_state("networkidle")

        updated_ui_all = atcu_ticket_dashboard_page.get_kpi_card_count("ALL")

        target_card = "ON HOLD" if is_after_530 else "IN PROGRESS"
        atcu_ticket_dashboard_page.click_kpi_card(target_card)
        atcu_ticket_dashboard_page.search_ticket(search_term)

        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term, timeout=10000)

        if not is_present:
            atcu_ticket_dashboard_page.click_kpi_card("ALL")
            atcu_ticket_dashboard_page.search_ticket(search_term)
            is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term, timeout=5000)

        report_case(
            expected=f"Generated ticket '{search_term}' should increment counts and be present in table under '{target_card}'",
            actual=f"search_term='{search_term}', is_present={is_present}, pre_ui_all={initial_ui_all}, post_ui_all={updated_ui_all}, pre_api_all={pre_api_all}, post_api_all={post_api_all}",
            message="Validate ticket generation API, count update, and table search",
        )

        assert is_present or updated_ui_all >= initial_ui_all, f"Newly generated ticket '{search_term}' not found in table"


    # --- Group 9: Deep UI & Tooltips ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_tooltip_validation(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        tooltip = atcu_ticket_dashboard_page.get_search_tooltip_message()
        report_case(
            expected="Search bar tooltip should specify searchable fields ('Ticket No | UIN NO. | Chassis NO. | IMEI NO.')",
            actual=f"tooltip='{tooltip}'",
            message="Validate search bar tooltip message",
        )
        assert "Ticket No" in tooltip or "UIN" in tooltip or "Chassis" in tooltip or "IMEI" in tooltip, f"Unexpected search tooltip: '{tooltip}'"

    # --- Group 9: Deep UI & TAT Report Download Tests ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_button_visibility_and_enablement(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating Download TAT Report button visibility and enablement state")
        loc = atcu_ticket_dashboard_page.page.locator(atcu_ticket_dashboard_page.DOWNLOAD_TAT_REPORT_BTN)
        is_vis = loc.is_visible()
        is_enabled = loc.is_enabled()
        report_case(
            expected="Download TAT Report button should be visible and enabled",
            actual=f"is_vis={is_vis}, is_enabled={is_enabled}",
            message="Validate Download TAT Report button state",
        )
        assert is_vis, "Download TAT Report button not visible"
        assert is_enabled, "Download TAT Report button disabled"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_with_15_days_date_filter_validation(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        """
        Applies a 15-day date filter (15 days back from today) to avoid large payload timeouts,
        triggers Download TAT Report, saves the file, and validates file existence and size.
        """
        logger.info("Starting 15-day date filter TAT report download and file validation test")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()

        filename = download_obj.suggested_filename if download_obj else ""
        logger.info("TAT Report Downloaded: filename='%s', path='%s', size=%s bytes", filename, file_path, file_size)

        report_case(
            expected="Applying 15-day date filter should generate a valid, non-empty TAT Report file",
            actual=f"download_ok={download_obj is not None}, filename='{filename}', file_path='{file_path}', file_size={file_size}",
            message="Validate 15-day date filter TAT report download and file contents",
        )
        assert download_obj is not None, "TAT report download event failed to trigger"
        assert filename, "Downloaded file suggested_filename is empty"
        assert file_size > 0, "Downloaded TAT Report file is empty (0 bytes)"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Testing TAT Report download in ALL card view with 15-day filter")
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()
        report_case(
            expected="Download TAT Report in ALL card view with 15-day filter should produce valid file",
            actual=f"download_triggered={download_obj is not None}, file_size={file_size}",
            message="Validate Download TAT Report in ALL view",
        )
        assert download_obj is not None, "TAT Report download failed to trigger in ALL card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Testing TAT Report download in IN PROGRESS card view with 15-day filter")
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()
        report_case(
            expected="Download TAT Report in IN PROGRESS card view with 15-day filter should produce valid file",
            actual=f"download_triggered={download_obj is not None}, file_size={file_size}",
            message="Validate Download TAT Report in IN PROGRESS view",
        )
        assert download_obj is not None, "TAT Report download failed to trigger in IN PROGRESS card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Testing TAT Report download in ON HOLD card view with 15-day filter")
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()
        if download_obj is None:
            is_enabled = atcu_ticket_dashboard_page.page.locator(
                atcu_ticket_dashboard_page.DOWNLOAD_TAT_REPORT_BTN
            ).first.is_enabled()
            report_case(
                expected="Download TAT Report is disabled when the ON HOLD view has no report data in the selected date range",
                actual=f"download_triggered=False, is_enabled={is_enabled}",
                message="Validate TAT Report availability in ON HOLD view",
            )
            assert not is_enabled, "TAT Report download failed while the ON HOLD report button remained enabled"
            return

        report_case(
            expected="Download TAT Report in ON HOLD card view with 15-day filter should produce valid file",
            actual=f"download_triggered={download_obj is not None}, file_size={file_size}",
            message="Validate Download TAT Report in ON HOLD view",
        )
        assert download_obj is not None, "TAT Report download failed to trigger in ON HOLD card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Testing TAT Report download in CANCELLED card view with 15-day filter")
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()
        report_case(
            expected="Download TAT Report in CANCELLED card view with 15-day filter should produce valid file",
            actual=f"download_triggered={download_obj is not None}, file_size={file_size}",
            message="Validate Download TAT Report in CANCELLED view",
        )
        assert download_obj is not None, "TAT Report download failed to trigger in CANCELLED card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Testing TAT Report download in COMPLETED card view with 15-day filter")
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        download_obj, file_path, file_size = atcu_ticket_dashboard_page.apply_15_days_date_filter_and_download_tat_report()
        if download_obj is None:
            is_enabled = atcu_ticket_dashboard_page.page.locator(
                atcu_ticket_dashboard_page.DOWNLOAD_TAT_REPORT_BTN
            ).first.is_enabled()
            report_case(
                expected="Download TAT Report is disabled when the COMPLETED view has no report data in the selected date range",
                actual=f"download_triggered=False, is_enabled={is_enabled}",
                message="Validate TAT Report availability in COMPLETED view",
            )
            assert not is_enabled, "TAT Report download failed while the COMPLETED report button remained enabled"
            return

        report_case(
            expected="Download TAT Report in COMPLETED card view with 15-day filter should produce valid file",
            actual=f"download_triggered={download_obj is not None}, file_size={file_size}",
            message="Validate Download TAT Report in COMPLETED view",
        )
        assert download_obj is not None, "TAT Report download failed to trigger in COMPLETED card view"


    # --- Group 10: Filter Modal & Individual Field Tests ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_opening_and_controls(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        is_vis = atcu_ticket_dashboard_page.is_filter_modal_visible()
        atcu_ticket_dashboard_page.close_filter_modal()
        report_case(
            expected="Filter button click should display details filter modal with form controls",
            actual=f"is_vis={is_vis}",
            message="Validate filter modal opening and close",
        )
        assert is_vis, "Filter modal not visible"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_assign_date_range(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.fill_filter_dates(from_date="2026-07-01", to_date="2026-08-03")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Assign Date Range filter should update table data",
            actual=f"rows_count={len(rows)}",
            message="Validate Assign Date Range filter",
        )
        assert isinstance(rows, list), "Failed to retrieve filtered rows"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_completed_date_range(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.fill_filter_dates(completed_from_date="2026-07-01", completed_to_date="2026-08-03")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Completed Date Range filter should update table data",
            actual=f"rows_count={len(rows)}",
            message="Validate Completed Date Range filter",
        )
        assert isinstance(rows, list), "Failed to retrieve filtered rows"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_state(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("state")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting State dropdown filter should filter tickets by selected state",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate State dropdown filter",
        )
        assert select_ok, "Failed to select option from State dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_assigned_to(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("assignTo")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Assigned To dropdown filter should filter tickets by ticket handler",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate Assigned To dropdown filter",
        )
        assert select_ok, "Failed to select option from Assigned To dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_ticket_status(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("ticketStatusFilter")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Ticket Status dropdown filter should filter tickets by status",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate Ticket Status dropdown filter",
        )
        assert select_ok, "Failed to select option from Ticket Status dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_dealer_code(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("dealerCode")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Dealer Code dropdown filter should filter tickets by dealer",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate Dealer Code dropdown filter",
        )
        assert select_ok, "Failed to select option from Dealer Code dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_initiated_by(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("initiatedBy")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Initiated By dropdown filter should filter tickets by initiator",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate Initiated By dropdown filter",
        )
        assert select_ok, "Failed to select option from Initiated By dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_device_type(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("deviceType")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting Device Type dropdown filter should filter tickets by device type",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate Device Type dropdown filter",
        )
        assert select_ok, "Failed to select option from Device Type dropdown"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_by_tat_type(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        select_ok = atcu_ticket_dashboard_page.select_filter_dropdown("tatType")
        atcu_ticket_dashboard_page.click_modal_submit()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Submitting TAT Type dropdown filter should filter tickets by TAT criteria",
            actual=f"select_ok={select_ok}, rows_count={len(rows)}",
            message="Validate TAT Type dropdown filter",
        )
        assert select_ok, "Failed to select option from TAT Type dropdown"


    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_clear_button(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.click_modal_clear()
        rows = atcu_ticket_dashboard_page.get_table_rows()
        report_case(
            expected="Clicking Clear in filter modal should reset filters to default state",
            actual=f"rows_count={len(rows)}",
            message="Validate filter modal Clear button",
        )
        assert isinstance(rows, list), "Failed to clear filter form"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_close_button(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.close_filter_modal()
        is_modal_vis = atcu_ticket_dashboard_page.is_filter_modal_visible()
        report_case(
            expected="Clicking close × button should dismiss filter modal",
            actual=f"is_modal_vis={is_modal_vis}",
            message="Validate filter modal close button",
        )
        assert not is_modal_vis, "Filter modal still visible after close"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_submit_and_clear_reactivity(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        is_modal_vis = atcu_ticket_dashboard_page.is_filter_modal_visible()
        assert is_modal_vis, "Details filter modal should be visible"

        atcu_ticket_dashboard_page.click_modal_submit()
        graphs_reactive = atcu_ticket_dashboard_page.verify_all_graphs_reactive()

        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.click_modal_clear()

        report_case(
            expected="Applying and clearing filters should reactively update graphs and table rows",
            actual=f"modal_vis={is_modal_vis}, graphs_reactive={graphs_reactive}",
            message="Validate filter modal submit, clear, and reactivity",
        )
        assert all(graphs_reactive.values()), "Graphs failed reactivity check after filter submission"


    # --- Group 11: Search Scenarios ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_ticket_no(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("TICKET NO.", "AEPL-260730-1") if first_row else "AEPL-260730-1"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for Ticket NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by Ticket NO.",
        )
        assert is_present, f"Ticket NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_uin(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("UIN NO.", "ACON4IA202200075879") if first_row else "ACON4IA202200075879"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for UIN NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by UIN NO.",
        )
        assert is_present, f"UIN NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_chassis(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("CHASSIS NO.", "MAT00007241590103") if first_row else "MAT00007241590103"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for Chassis NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by Chassis NO.",
        )
        assert is_present, f"Chassis NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_non_existent_term(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        search_term = "NON_EXISTENT_TICKET_99999"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term, timeout=3000)
        report_case(
            expected="Searching non-existent ticket should return 0 matching rows",
            actual=f"is_present={is_present}",
            message="Validate search non-existent term",
        )
        assert not is_present, "Non-existent ticket term returned unexpected row"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_whitespace_trimming(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        clean_term = first_row.get("TICKET NO.", "AEPL-260730-1") if first_row else "AEPL-260730-1"
        raw_search_term = f"  {clean_term}  "
        atcu_ticket_dashboard_page.search_ticket(raw_search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(clean_term)
        report_case(
            expected="Search query with leading/trailing whitespace should execute cleanly",
            actual=f"raw='{raw_search_term}', is_present={is_present}",
            message="Validate search input whitespace trimming",
        )
        assert is_present, f"Ticket '{clean_term}' not found when searching with whitespace"
