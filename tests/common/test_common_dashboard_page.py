from pages.common_base_page import BasePage
from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.dashboard
@pytest.mark.regression
@pytest.mark.usefixtures("project_config")
@pytest.mark.lct
@pytest.mark.sampark
class TestDashboardPage:
    @pytest.fixture(autouse=True)
    def _inject_project_config(self, request, project_config):
        # Make `project_config` accessible as `self.project_config` inside test methods
        request.cls.project_config = project_config

    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dashboard test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Dashboard test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Dashboard test passed: %s", test_name)
        elif report.failed:
            logger.error("Dashboard test failed: %s", test_name)
            logger.debug(
                "Dashboard failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Dashboard test skipped: %s", test_name)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.regression
    def test_dashboard_page_navigates_to_correct_url(
        self, dashboard_page, project_config, report_case
    ):
        logger.info("Validating dashboard landing URL")

        expected_url = project_config["dashboard_url"]
        actual_url = dashboard_page.page.url

        logger.debug(
            "Dashboard URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )
        report_case(expected=expected_url, actual=actual_url, message="Validate Dashboard page navigates to correct URL")

        assert actual_url == expected_url, f"Expected {expected_url}, got {actual_url}"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dashboard_page_title_is_correct(self, dashboard_page, report_case):
        base_page = BasePage(dashboard_page.page)
        logger.info("Validating dashboard page title")
        actual_title = base_page.get_title()
        logger.debug(
            "Dashboard title check | expected=%s | actual=%s",
            "Device Dashboard",
            actual_title,
        )
        report_case(expected="Device Dashboard", actual=actual_title, message="Validate Dashboard page title is correct")

        assert actual_title == "Device Dashboard", "Dashboard title is incorrect"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dashboard_page_all_elements_are_visible(self, dashboard_page, report_case):
        logger.info("Checking all dashboard elements (cards/graph/table)")
        cards_visible = dashboard_page._is_cards_visible()
        cards_count = dashboard_page.get_cards_count()
        graph_visible = dashboard_page._is_graph_visible()
        table_visible = dashboard_page._is_table_visible()
        report_case(
            expected="Cards visible=True, card count=4, graph visible=True, table visible=True",
            actual=(
                f"Cards visible={cards_visible}, card count={cards_count}, "
                f"graph visible={graph_visible}, table visible={table_visible}"
            )
        , message="Validate Dashboard page all elements are visible")
        assert cards_visible, "Dashboard cards are not visible"
        assert cards_count == 4, "Expected 4 cards on the dashboard"
        assert graph_visible, "Dashboard graph is not visible"
        assert table_visible, "Dashboard table is not visible"
        # assert dashboard_page._is_buttons_visible(), "Dashboard buttons are not visible"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dashboard_page_cards_are_visible(self, dashboard_page, report_case):
        logger.info("Confirming dashboard cards are visible")
        cards_visible = dashboard_page._is_cards_visible()
        report_case(expected=True, actual=cards_visible, message="Validate Dashboard page cards are visible")
        assert cards_visible, "Dashboard cards are not visible"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dashboard_page_displays_four_cards(self, dashboard_page, report_case):
        expected_cards_count = 4
        actual_cards_count = dashboard_page.get_cards_count()
        logger.info("Comparing dashboard card counts")
        logger.debug(
            "Dashboard card count check | expected=%s | actual=%s",
            expected_cards_count,
            actual_cards_count,
        )
        report_case(expected=expected_cards_count, actual=actual_cards_count, message="Validate Dashboard page displays four cards")

        assert (
            actual_cards_count == expected_cards_count
        ), f"Expected {expected_cards_count} cards, got {actual_cards_count}"

        for index in range(expected_cards_count):
            card = dashboard_page.get_card_element(index)
            assert card.is_visible(), f"Card {index} is missing or not visible"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_card_titles_are_correct(self, dashboard_page, report_case):
        expected_title = [
            "TOTAL PRODUCTION DEVICES",
            "TOTAL DISPATCHED DEVICES",
            "TOTAL INSTALLED DEVICES",
            "TOTAL DISCARDED DEVICES",
        ]

        actual_titles = []
        for i, title in enumerate(expected_title):
            logger.info("Asserting card %s title", i)
            actual_title = dashboard_page.get_cards_title_text(i)
            actual_titles.append(actual_title)
            logger.debug(
                "Dashboard card title check | index=%s | expected=%s | actual=%s",
                i,
                title,
                actual_title,
            )
            assert actual_title == title, f"Expected '{title}', got '{actual_title}'"
        report_case(expected=expected_title, actual=actual_titles, message="Validate Dashboard page card titles are correct")

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_card_counts_match_api_data(
        self, page, dashboard_page, dashboard_api, report_case
    ):
        logger.info("Verifying dashboard card counts against API")
        api_results = dashboard_api.get_device_counts()
        logger.debug("Dashboard API card counts: %s", api_results)
        actual_results = {}
        for i, title in enumerate(api_results.keys()):
            expected_count = str(api_results[title])
            actual_count = dashboard_page.get_cards_inner_count(i)
            actual_results[title] = actual_count
            logger.debug(
                "Dashboard card count value check | card=%s | expected=%s | actual=%s",
                title,
                expected_count,
                actual_count,
            )
            assert (
                actual_count == expected_count
            ), f"For '{title}', expected count '{expected_count}', got '{actual_count}'"
        report_case(expected=api_results, actual=actual_results, message="Validate Dashboard page card counts match API data")

        logger.info("Checking graph visibility on dashboard")
        graph_visible = dashboard_page._is_graph_visible()
        report_case(expected=True, actual=graph_visible, message="Validate Dashboard page card counts match API data")
        assert graph_visible, "Dashboard graph is not visible"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_graph_title_is_correct(self, dashboard_page, report_case):
        logger.info("Validating each graph title")
        expected_graph_title = ["Device Activity Overview", "Firmware Wise Devices"]

        actual_graph_titles = []
        for title in expected_graph_title:
            actual_graph_title = dashboard_page.get_graph_title(title)
            actual_graph_titles.append(actual_graph_title)
            logger.debug(
                "Dashboard graph title check | expected=%s | actual=%s",
                title,
                actual_graph_title,
            )
            assert (
                actual_graph_title == title
            ), f"Expected graph title '{title}', got '{actual_graph_title}'"
        report_case(expected=expected_graph_title, actual=actual_graph_titles, message="Validate Dashboard page graph title is correct")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_table_is_visible(self, dashboard_page, report_case):
        logger.info("Verifying table visibility")
        table_visible = dashboard_page._is_table_visible()
        report_case(expected=True, actual=table_visible, message="Validate Dashboard page table is visible")
        assert table_visible, "Dashboard table is not visible"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_card_and_graph_clicks_update_table_title(
        self, dashboard_page, report_case
    ):
        logger.info("Ensuring table titles match card/graph clicks")
        expected_table_title = [
            "Total Production Devices",
            "Total Dispatched Devices",
            "Total Installed Devices",
            "Total Discarded Devices",
        ]

        actual_table_titles = []
        for title in expected_table_title:
            actual_table_title = dashboard_page.get_table_title_after_card_click(title)
            actual_table_titles.append(actual_table_title)
            logger.debug(
                "Dashboard clicked table title check | expected=%s | actual=%s",
                title,
                actual_table_title,
            )
            assert (
                actual_table_title == title
            ), f"Expected table title '{title}', got '{actual_table_title}'"
        report_case(expected=expected_table_title, actual=actual_table_titles, message="Validate Dashboard page card and graph clicks update table title")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_export_button_is_visible_and_functional(
        self, dashboard_page, report_case
    ):
        logger.info("Testing export button functionality")
        result = dashboard_page.check_export_button()
        logger.debug("Dashboard export button result: %s", result)
        report_case(
            expected=True, actual=result.get("success"), message=result.get("error", "")
        )

        assert result[
            "success"
        ], f"Export button functionality failed: {result['error']}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_search_filters_table_data(
        self, dashboard_page, project_config, test_data, report_case
    ):
        logger.info("Running search functionality test with query")
        # Prefer project-specific IMEI from test_data; fall back to configured IMEI
        search_query = test_data.get("valid_imei") or project_config.get(
            "imei", "866677075606341"
        )
        result = dashboard_page.search_helper.run_search(search_query)
        logger.debug("Dashboard search result for query %s: %s", search_query, result)
        report_case(
            expected=f"Search results should contain {search_query}",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Search functionality failed: {result['error']}"
        assert (
            result["results_found"] > 0
        ), f"No results found for search query '{search_query}'"
        assert all(
            search_query in item for item in result["results"]
        ), "Search results do not match the query"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_table_headers_are_correct(
        self, dashboard_page, report_case
    ):
        logger.info("Validating table headers")
        expected_headers = ["UIN NO.", "IMEI NO.", "ICCID NO.", "MODEL NAME.", "ACTION"]
        actual_headers = dashboard_page.table_section.get_headers()
        logger.debug(
            "Dashboard table headers | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )
        report_case(expected=expected_headers, actual=actual_headers, message="Validate Dashboard page table headers are correct")
        assert (
            actual_headers == expected_headers
        ), f"Expected table headers {expected_headers}, got {actual_headers}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_dashboard_page_pagination_navigates_across_pages(
        self, dashboard_page, report_case
    ):
        logger.info("Executing pagination workflow")
        result = dashboard_page.pagination_helper.verify()
        logger.debug("Dashboard pagination result: %s", result)
        report_case(
            expected="Pagination success=True and pages visited in order", actual=result
        , message="Validate Dashboard page pagination navigates across pages")
        assert result["success"], f"Pagination failed: {result['error']}"
        # assert result["total_pages"] > 1, "Pagination did not move beyond first page"
        assert result["pages_visited"] == sorted(
            result["pages_visited"]
        ), "Pages not in order"
