import re
from utils.logger import get_logger
from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper

logger = get_logger(__name__)


class AtcuTicketDashboardPage(BasePage):
    """
    Page Object Model for ATCU Ticket Dashboard page (/ticket-dashboard-page).
    Contains locators and interaction methods for:
    - Page load, title, routing buttons (back/reload)
    - KPI Cards (ALL, IN PROGRESS, ON HOLD, CANCELLED, COMPLETED)
    - Reactive Charts (Month-wise Trend, TAT Trend, TAT Reason, State Wise, Individual, Model Wise)
    - Filter Modal, Table data, Search bar, Report download, and Pagination
    """

    # --- Locators ---
    CONTAINER = "app-ticket-dashboard-page"
    PAGE_TITLE = ".page-title"
    COMPONENT_TITLE = ".component-title"
    BACK_BTN = ".action-button.back-button"
    RELOAD_BTN = ".action-button.reload-button"

    # KPI Section Locators
    KPI_CARDS = ".kpi-section .kpi-card"
    KPI_ALL_CARD = ".kpi-card:has(.kpi-content:has-text('ALL'))"
    KPI_IN_PROGRESS_CARD = ".kpi-card:has(.kpi-content:has-text('IN PROGRESS'))"
    KPI_ON_HOLD_CARD = ".kpi-card:has(.kpi-content:has-text('ON HOLD'))"
    KPI_CANCELLED_CARD = ".kpi-card:has(.kpi-content:has-text('CANCELLED'))"
    KPI_COMPLETED_CARD = ".kpi-card:has(.kpi-content:has-text('COMPLETED'))"

    # Graph Section Locators
    GRAPH_CARDS = ".graph-section .graph-card"
    GRAPH_TITLES = ".graph-section .graph-title"
    GRAPH_CANVASES = ".graph-section canvas"

    # Table Locators
    TABLE_HEADERS = "table thead th"
    TABLE_ROWS = "table tbody tr"
    SEARCH_INPUT = "input[formcontrolname='searchInput']"
    SEARCH_BTN = "button.search-btn"
    FILTER_BTN = "button:has-text('Filter')"
    DOWNLOAD_TAT_REPORT_BTN = "button:has-text('Download TAT Report')"

    PAGINATION_CONTAINER = "app-common-component-pagination, .pagination-container"
    ROWS_SELECT = "#rowsSelect"

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    # --- Page & Header Verification ---
    def is_page_loaded(self, timeout=10000):
        logger.info("Checking if ATCU Ticket Dashboard page is loaded")
        try:
            self.page.locator(self.CONTAINER).wait_for(state="visible", timeout=timeout)
            return self.page.locator(self.CONTAINER).is_visible()
        except Exception as e:
            logger.error("ATCU Ticket Dashboard page failed to load within %s ms: %s", timeout, e)
            return False

    def get_title(self):
        logger.info("Retrieving ATCU Ticket Dashboard page title")
        try:
            title_loc = self.page.locator(self.PAGE_TITLE)
            title_loc.wait_for(state="visible", timeout=5000)
            text = title_loc.text_content().strip()
            logger.info("Page title: '%s'", text)
            return text
        except Exception as e:
            logger.error("Failed to get page title: %s", e)
            return ""

    def get_component_title(self):
        logger.info("Retrieving component header title")
        try:
            loc = self.page.locator(self.COMPONENT_TITLE).first
            loc.wait_for(state="visible", timeout=5000)
            text = loc.text_content().strip()
            logger.info("Component title: '%s'", text)
            return text
        except Exception as e:
            logger.error("Failed to get component title: %s", e)
            return ""

    def click_back_button(self):
        logger.info("Clicking Back button")
        self.page.locator(self.BACK_BTN).click()

    def click_reload_button(self):
        logger.info("Clicking Reload button")
        self.page.locator(self.RELOAD_BTN).click()
        self.page.wait_for_load_state("networkidle")

    # --- KPI Cards Helpers ---
    def _parse_card_count(self, text):
        if not text:
            return 0
        cleaned = re.sub(r"[^\d]", "", text)
        return int(cleaned) if cleaned else 0

    def get_kpi_card_count(self, card_name):
        name_upper = str(card_name).upper().strip()
        logger.info("Getting count for KPI card: '%s'", name_upper)
        try:
            card_loc = self.page.locator(f".kpi-card:has(.kpi-content:has-text('{name_upper}'))")
            card_loc.wait_for(state="visible", timeout=5000)
            val_text = card_loc.locator(".kpi-value").text_content().strip()
            count = self._parse_card_count(val_text)
            logger.info("KPI Card '%s' raw value: '%s', parsed count: %s", name_upper, val_text, count)
            return count
        except Exception as e:
            logger.error("Failed to get count for KPI card '%s': %s", name_upper, e)
            return 0

    def click_kpi_card(self, card_name):
        name_upper = str(card_name).upper().strip()
        logger.info("Clicking KPI card: '%s'", name_upper)
        card_loc = self.page.locator(f".kpi-card:has(.kpi-content:has-text('{name_upper}'))")
        card_loc.wait_for(state="visible", timeout=5000)
        card_loc.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def get_all_kpi_counts(self):
        counts = {
            "ALL": self.get_kpi_card_count("ALL"),
            "IN_PROGRESS": self.get_kpi_card_count("IN PROGRESS"),
            "ON_HOLD": self.get_kpi_card_count("ON HOLD"),
            "CANCELLED": self.get_kpi_card_count("CANCELLED"),
            "COMPLETED": self.get_kpi_card_count("COMPLETED"),
        }
        logger.info("Retrieved all KPI counts: %s", counts)
        return counts

    # --- Reactive Graph Methods ---
    def get_all_graph_titles(self):
        logger.info("Retrieving all graph titles on Ticket Dashboard")
        titles = []
        try:
            locs = self.page.locator(self.GRAPH_TITLES).all()
            titles = [loc.text_content().strip() for loc in locs]
            logger.info("Found %s graph titles: %s", len(titles), titles)
        except Exception as e:
            logger.error("Failed to get graph titles: %s", e)
        return titles

    def is_graph_visible(self, graph_title):
        logger.info("Checking visibility for graph: '%s'", graph_title)
        try:
            card_loc = self.page.locator(f".graph-card:has(.graph-title:has-text('{graph_title}'))")
            card_loc.wait_for(state="visible", timeout=5000)
            canvas_loc = card_loc.locator("canvas")
            return canvas_loc.is_visible()
        except Exception as e:
            logger.error("Graph '%s' canvas not visible: %s", graph_title, e)
            return False

    def verify_all_graphs_reactive(self):
        logger.info("Verifying all graphs are rendered and reactive")
        results = {}
        expected_graphs = [
            "Month-wise AIS140 Ticket Trend",
            "AIS140 Ticket TAT Trend",
            "TAT Reason Breakdown",
            "State Wise Ticket Distribution",
            "Individual Performance",
            "Device Model Wise Graph",
        ]

        titles = self.get_all_graph_titles()

        for exp in expected_graphs:
            matching_title = next((t for t in titles if exp.lower() in t.lower()), None)
            if matching_title:
                is_vis = self.is_graph_visible(matching_title)
                results[matching_title] = is_vis
            else:
                logger.warning("Expected graph title containing '%s' not found", exp)
                results[exp] = False

        logger.info("Graphs reactivity verification results: %s", results)
        return results

    # --- Table & Filter Methods ---
    def get_table_headers(self):
        headers = []
        try:
            locators = self.page.locator(self.TABLE_HEADERS).all()
            headers = [loc.text_content().strip().upper() for loc in locators]
            logger.debug("Retrieved table headers: %s", headers)
        except Exception as e:
            logger.error("Failed to get table headers: %s", e)
        return headers

    def get_table_rows(self):
        rows_data = []
        try:
            headers = self.get_table_headers()
            row_elements = self.page.locator(self.TABLE_ROWS).all()
            for row in row_elements:
                cells = [cell.text_content().strip() for cell in row.locator("td").all()]
                if cells:
                    row_dict = dict(zip(headers, cells)) if headers else cells
                    rows_data.append(row_dict)
            logger.debug("Retrieved %s table rows", len(rows_data))
        except Exception as e:
            logger.error("Failed to get table rows: %s", e)
        return rows_data

    def get_search_tooltip_message(self):
        logger.info("Getting search bar tooltip message")
        try:
            search_component = self.page.locator("app-common-search").first
            tooltip = search_component.get_attribute("ng-reflect-message") or search_component.get_attribute("mattooltip") or ""
            logger.info("Search tooltip: '%s'", tooltip)
            return tooltip.strip()
        except Exception as e:
            logger.error("Failed to get search tooltip: %s", e)
            return ""

    def hover_over_graph(self, graph_title):
        logger.info("Hovering over graph canvas: '%s'", graph_title)
        try:
            card_loc = self.page.locator(f".graph-card:has(.graph-title:has-text('{graph_title}'))")
            canvas_loc = card_loc.locator("canvas")
            canvas_loc.scroll_into_view_if_needed()
            box = canvas_loc.bounding_box()
            if box:
                self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                self.page.wait_for_timeout(300)
            return True
        except Exception as e:
            logger.error("Failed to hover over graph '%s': %s", graph_title, e)
            return False

    def get_column_values(self, column_header_name):
        header_upper = column_header_name.strip().upper()
        logger.info("Extracting column values for header: '%s'", header_upper)
        values = []
        try:
            headers = self.get_table_headers()
            if header_upper not in headers:
                logger.warning("Header '%s' not found in headers: %s", header_upper, headers)
                return values
            col_index = headers.index(header_upper)
            row_elements = self.page.locator(self.TABLE_ROWS).all()
            for row in row_elements:
                cells = row.locator("td").all()
                if len(cells) > col_index:
                    val = cells[col_index].text_content().strip()
                    values.append(val)
        except Exception as e:
            logger.error("Failed to extract column values for '%s': %s", header_upper, e)
        return values

    def get_first_row_data(self):
        rows = self.get_table_rows()
        return rows[0] if rows else {}


    def search_ticket(self, search_term):
        logger.info("Searching tickets table for term: %s", search_term)
        try:
            input_loc = self.page.locator(self.SEARCH_INPUT).first
            input_loc.wait_for(state="visible", timeout=10000)
            input_loc.fill(str(search_term))
            input_loc.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.page.wait_for_timeout(500)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
            search_helper = SearchHelper(self.page)
            search_helper.run_search(str(search_term))

    def clear_search_input(self):
        logger.info("Clearing ticket search input field")
        input_loc = self.page.locator(self.SEARCH_INPUT).first
        input_loc.wait_for(state="visible", timeout=5000)
        input_loc.fill("")
        input_loc.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def is_ticket_present_in_table(self, ticket_no_or_uin, timeout=10000):
        logger.info("Checking if ticket '%s' is present in table", ticket_no_or_uin)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{ticket_no_or_uin}')]]").first
            row_locator.wait_for(state="visible", timeout=timeout)
            return row_locator.is_visible()
        except Exception as e:
            logger.warning("Ticket '%s' not found in table within %s ms: %s", ticket_no_or_uin, timeout, e)
            return False

    @staticmethod
    def is_after_530_pm_ist():
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_tz)
        return (now_ist.hour > 17) or (now_ist.hour == 17 and now_ist.minute >= 30)

    def click_filter_button(self):
        logger.info("Clicking Filter button to open details filter modal")
        self.page.locator(self.FILTER_BTN).click()
        self.page.locator("#filterDetails, .custom-modal").wait_for(state="visible", timeout=5000)

    def is_filter_modal_visible(self):
        try:
            modal = self.page.locator("#filterDetails, .custom-modal").first
            return modal.is_visible()
        except Exception:
            return False

    def close_filter_modal(self):
        logger.info("Closing details filter modal")
        try:
            self.page.locator(".custom-close-btn, button:has-text('×')").first.click()
            self.page.wait_for_timeout(300)
        except Exception as e:
            logger.warning("Failed to close filter modal: %s", e)

    def click_modal_submit(self):
        logger.info("Clicking Submit in filter modal")
        try:
            backdrop = self.page.locator(".cdk-overlay-backdrop")
            if backdrop.is_visible():
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(200)
        except Exception:
            pass

        btn = self.page.locator("#filterDetails button.submit-button, .custom-modal button.submit-button").first
        try:
            btn.click(timeout=5000)
        except Exception as e:
            logger.info("Submit click intercepted by overlay backdrop (%s), performing force click", e)
            btn.click(force=True)

        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(500)

    def click_modal_clear(self):
        logger.info("Clicking Clear in filter modal")
        btn = self.page.locator("#filterDetails button.clear-button, .custom-modal button.clear-button").first
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.click(force=True)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(500)

    def fill_filter_dates(self, from_date="", to_date="", completed_from_date="", completed_to_date=""):
        logger.info("Filling filter dates in modal: from='%s', to='%s', completed_from='%s', completed_to='%s'", from_date, to_date, completed_from_date, completed_to_date)
        try:
            date_map = [
                ("#fromDate, input[formcontrolname='fromDate']", from_date),
                ("#toDate, input[formcontrolname='toDate']", to_date),
                ("#ticketCompletedAtFromDate, input[formcontrolname='ticketCompletedAtFromDate']", completed_from_date),
                ("#ticketCompletedAtToDate, input[formcontrolname='ticketCompletedAtToDate']", completed_to_date),
            ]
            for selector, val in date_map:
                if val:
                    loc = self.page.locator(selector).first
                    loc.wait_for(state="attached", timeout=3000)
                    loc.evaluate("el => el.removeAttribute('readonly')")
                    loc.fill(str(val))
                    loc.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }")
                    logger.info("Filled filter date for '%s' -> '%s'", selector, val)
                    self.page.wait_for_timeout(200)
        except Exception as e:
            logger.warning("Filling filter dates exception: %s", e)

    def select_filter_dropdown(self, control_name, option_text=""):
        logger.info("Selecting option '%s' for filter dropdown '%s'", option_text, control_name)
        try:
            mat_select = self.page.locator(f"mat-select[formcontrolname='{control_name}']").first
            mat_select.wait_for(state="visible", timeout=5000)
            mat_select.click()
            self.page.wait_for_timeout(300)

            overlay_options = self.page.locator(".cdk-overlay-container mat-option, mat-option")
            overlay_options.first.wait_for(state="visible", timeout=5000)

            if option_text:
                target_option = overlay_options.filter(has_text=option_text).first
                target_option.click()
            else:
                overlay_options.first.click()
            self.page.wait_for_timeout(300)

            # Dismiss overlay backdrop if still visible
            try:
                backdrop = self.page.locator(".cdk-overlay-backdrop")
                if backdrop.is_visible():
                    self.page.keyboard.press("Escape")
                    self.page.wait_for_timeout(200)
            except Exception:
                pass

            return True
        except Exception as e:
            logger.error("Failed to select option for filter dropdown '%s': %s", control_name, e)
            return False

    def click_download_tat_report_button(self):
        logger.info("Clicking Download TAT Report button")
        if self.is_filter_modal_visible():
            logger.info("Filter modal is open on screen, closing modal before clicking Download TAT Report")
            self.close_filter_modal()
            self.page.wait_for_timeout(300)

        btn = self.page.locator(self.DOWNLOAD_TAT_REPORT_BTN).first
        btn.wait_for(state="visible", timeout=5000)
        if not btn.is_enabled():
            logger.info("TAT report download is disabled for the current dashboard view")
            return None

        def accept_confirmation(dialog):
            logger.info("Accepting TAT report confirmation: %s", dialog.message)
            dialog.accept()

        self.page.once("dialog", accept_confirmation)
        try:
            with self.page.expect_download(timeout=60000) as download_info:
                btn.click()
            download = download_info.value
            logger.info("Report download triggered successfully: %s", download.suggested_filename)
            return download
        except Exception as e:
            logger.warning("Download TAT report trigger exception: %s", e)
            return None



    def apply_15_days_date_filter_and_download_tat_report(self):

        """
        Applies a 15-day date filter (from 15 days ago to today) to avoid large report download timeouts,
        submits the filter modal, and triggers the TAT Report download event.
        Returns (download_object, saved_filepath, file_size_bytes).
        """
        from datetime import datetime, timedelta
        import os

        today_str = datetime.now().strftime("%Y-%m-%d")
        fifteen_days_ago_str = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

        logger.info("Applying 15-day date filter for TAT Report download: from '%s' to '%s'", fifteen_days_ago_str, today_str)

        self.click_filter_button()
        self.fill_filter_dates(from_date=fifteen_days_ago_str, to_date=today_str)
        self.click_modal_submit()
        self.page.wait_for_load_state("networkidle", timeout=10000)

        logger.info("Triggering Download TAT Report with 15-day date filter applied")
        download_obj = self.click_download_tat_report_button()

        file_path = ""
        file_size = 0
        if download_obj:
            try:
                temp_dir = os.path.join(os.getcwd(), "downloads")
                os.makedirs(temp_dir, exist_ok=True)
                file_path = os.path.join(temp_dir, download_obj.suggested_filename)
                download_obj.save_as(file_path)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                logger.info("Downloaded TAT Report saved to '%s' (Size: %s bytes)", file_path, file_size)
            except Exception as e:
                logger.warning("Error saving downloaded file: %s", e)

        return download_obj, file_path, file_size


    def is_pagination_visible(self, timeout=3000):
        try:
            loc = self.page.locator(self.PAGINATION_CONTAINER)
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.debug("Pagination container not visible within %s ms: %s", timeout, e)
            return False


    def get_selected_rows_per_page(self):
        try:
            loc = self.page.locator(self.ROWS_SELECT)
            loc.wait_for(state="visible", timeout=10000)
            return loc.input_value()
        except Exception as e:
            logger.error("Failed to get rows per page: %s", e)
            return ""

    def select_rows_per_page(self, option_value):
        logger.info("Selecting %s rows per page", option_value)
        loc = self.page.locator(self.ROWS_SELECT)
        loc.wait_for(state="visible", timeout=10000)
        loc.select_option(str(option_value))

    def validate_pagination(self):
        logger.info("Validating pagination on Ticket Dashboard page")
        pagination = PaginationHelper(
            self.page,
            page_input="input.page-input",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            content_selector="table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Pagination validation result: %s", result)
        return result
