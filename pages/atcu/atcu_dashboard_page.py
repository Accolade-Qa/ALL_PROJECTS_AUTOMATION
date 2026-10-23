from pages.common_dashboard_page import DashboardPage
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDashboardPage(DashboardPage):
    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuDashboardPage initialized")

    def go_to_atcu_dashboard(self, url):
        logger.info("Navigating to ATCU device dashboard URL %s", url)
        try:
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            logger.warning("page.goto direct navigation failed/timed out: %s. Trying header navbar navigation.", e)

        # Wait for loading spinner overlay to detach if present
        try:
            self.page.locator(".ngx-spinner-overlay").wait_for(state="detached", timeout=10000)
        except Exception:
            pass

        # If page is still not on dashboard or graph section is not visible, click navbar dropdown link
        if "device-dashboard" not in self.page.url or not self.page.locator(".graph-section, .graph-card").first.is_visible():
            logger.info("Using navbar navigation to switch to Device Dashboard")
            try:
                self.page.locator("a.dropdown-toggle:has-text('Dashboard')").first.click()
                self.page.locator("a:has-text('Device Dashboard')").first.click()
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception as nav_err:
                logger.error("Navbar navigation failed: %s", nav_err)

        # Wait for graphs and cards to be visible
        try:
            self.page.locator(".graph-section, .kpi-section, .graph-card").first.wait_for(state="visible", timeout=15000)
        except Exception as vis_err:
            logger.warning("Graph/KPI section visibility wait: %s", vis_err)

        current_url = self.page.url
        logger.info("Successfully navigated to ATCU dashboard. Current URL: %s", current_url)
        return current_url

    def click_state_wise_graph_card(self, graph_title="State Wise Details"):
        logger.info("Clicking graph card with title: %s", graph_title)
        graph_locator = self.page.locator(
            f".graph-card:has-text('{graph_title}'), "
            f"h3.graph-title:has-text('{graph_title}'), "
            f".graph-title:has-text('{graph_title}')"
        ).first
        graph_locator.wait_for(state="visible", timeout=15000)
        graph_locator.scroll_into_view_if_needed()
        graph_locator.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.info("Successfully clicked graph card: %s", graph_title)

    def get_state_wise_table_title(self, graph_title="State Wise Details"):
        logger.info("Retrieving component table title after graph card click")
        title_locator = self.page.locator(".component-title").first
        title_locator.wait_for(state="visible", timeout=10000)
        title = title_locator.inner_text().strip()
        logger.info("Component table title: %s", title)
        return title

    def search_imei_in_state_wise_table(self, imei):
        logger.info("Searching State Wise Details table for IMEI: %s", imei)
        try:
            search_input = self.page.locator(
                "input[formcontrolname='searchInput'], input[placeholder*='Search'], .search-bar input"
            ).first
            search_input.wait_for(state="visible", timeout=10000)
            search_input.fill(str(imei))
            search_input.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
            self.search_helper.run_search(str(imei))

    def is_imei_present_in_state_wise_table(self, imei, timeout=10000):
        logger.info("Checking if IMEI '%s' is present in State Wise Details table", imei)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{imei}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("IMEI '%s' present in table: %s", imei, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("IMEI '%s' not found in table within %s ms: %s", imei, timeout, e)
            return False

    def get_imei_row_state_details(self, imei):
        logger.info("Getting State Wise Details row for IMEI '%s'", imei)
        row = self.page.locator("table tbody tr").filter(has_text=str(imei)).first
        row.wait_for(state="visible", timeout=10000)

        headers = [
            header.inner_text().strip()
            for header in self.page.locator("table thead th").all()
        ]
        values = [cell.inner_text().strip() for cell in row.locator("td").all()]
        if len(headers) != len(values):
            raise ValueError(
                f"State Wise Details row has {len(values)} cells but "
                f"{len(headers)} column headers"
            )

        row_details = dict(zip(headers, values))
        logger.info("State Wise Details row for IMEI '%s': %s", imei, row_details)
        return row_details

    def click_installed_device_card(self, card_title="Installed"):
        logger.info("Clicking KPI card with title: %s", card_title)
        try:
            self.page.locator(".kpi-section").first.wait_for(state="visible", timeout=15000)
        except Exception:
            pass

        card_locator = (
            self.page.locator("div.kpi-section > div, div.kpi-details, span.kpi-content")
            .filter(has_text=card_title)
            .first
        )
        card_locator.wait_for(state="visible", timeout=15000)
        card_locator.scroll_into_view_if_needed()
        card_locator.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.info("Successfully clicked KPI card: %s", card_title)

    def get_installed_devices_table_title(self):
        logger.info("Retrieving component table title after KPI card click")
        title_locator = self.page.locator(".component-title, h6.component-title").first
        title_locator.wait_for(state="visible", timeout=10000)
        title = title_locator.inner_text().strip()
        logger.info("Component table title: %s", title)
        return title


    def search_imei_or_vin_in_installed_table(self, search_term):
        logger.info("Searching Installed Devices table for term: %s", search_term)
        try:
            search_input = self.page.locator(
                "input[formcontrolname='searchInput'], input[placeholder*='Search'], .search-bar input"
            ).first
            search_input.wait_for(state="visible", timeout=10000)
            search_input.fill(str(search_term))
            search_input.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
            self.search_helper.run_search(str(search_term))

    def is_device_present_in_installed_table(self, search_term, timeout=10000):
        logger.info("Checking if device '%s' is present in Installed Devices table", search_term)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{search_term}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("Device '%s' present in table: %s", search_term, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("Device '%s' not found in table within %s ms: %s", search_term, timeout, e)
            return False

    def get_installed_device_row_details(self, search_term):
        logger.info("Getting row details for device '%s'", search_term)
        try:
            headers = [th.inner_text().strip() for th in self.page.locator("table thead th").all()]
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{search_term}')]]").first
            cells = [td.inner_text().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for device '%s': %s", search_term, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for device '%s': %s", search_term, e)
            return {}

    def get_dispatched_device_card_count(self, card_title="Dispatched Devices"):
        logger.info("Retrieving count for KPI card with title: %s", card_title)
        try:
            card_locator = (
                self.page.locator("div.kpi-section > div, div.kpi-details, span.kpi-content, .kpi-card")
                .filter(has_text=card_title)
                .first
            )
            card_locator.wait_for(state="visible", timeout=15000)
            count_loc = card_locator.locator(".card-count, .kpi-count, h2, h3, span.count").first
            count_text = count_loc.inner_text().strip()
            logger.info("Dispatched Devices card count: %s", count_text)
            return count_text
        except Exception as e:
            logger.error("Failed to get Dispatched Devices card count: %s", e)
            return "0"

    def click_dispatched_device_card(self, card_title="Dispatched Devices"):
        logger.info("Clicking Dispatched Devices KPI card with title: %s", card_title)
        try:
            card_locator = (
                self.page.locator("div.kpi-section > div, div.kpi-details, span.kpi-content, .kpi-card")
                .filter(has_text=card_title)
                .first
            )
            card_locator.wait_for(state="visible", timeout=15000)
            card_locator.scroll_into_view_if_needed()
            card_locator.click()
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.info("Successfully clicked Dispatched Devices KPI card")
        except Exception as e:
            logger.error("Failed to click Dispatched Devices KPI card: %s", e)
