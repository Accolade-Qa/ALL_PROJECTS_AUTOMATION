from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuStatusUpdateLogPage(BasePage):
    PAGE_CONTAINER = "div.main-container"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    SEARCH_INPUT = "input[formcontrolname='searchInput']"
    SEARCH_BTN = "button.search-btn"
    TABLE = ".component-body table"
    TABLE_HEADERS = ".component-body table thead th"
    TABLE_ROWS = ".component-body table tbody tr"
    PAGINATION_CONTAINER = "app-common-component-pagination, .pagination-container"
    ROWS_SELECT = "select#rowsSelect"
    BACK_BTN = ".back-button"
    RELOAD_BTN = ".reload-button"
    TOAST_MESSAGE = ".mat-mdc-snack-bar-label, simple-snack-bar, [data-sonner-toast]"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuStatusUpdateLogPage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuStatusUpdateLogPage is loaded")
        self.page.locator(self.PAGE_CONTAINER).wait_for(
            state="visible", timeout=5000
        )
        is_vis = self.page.locator(self.PAGE_CONTAINER).is_visible()
        logger.info("AtcuStatusUpdateLogPage load status: %s", is_vis)
        return is_vis

    def get_title(self):
        logger.info("Retrieving AtcuStatusUpdateLogPage title")
        try:
            title_loc = self.page.locator(self.PAGE_TITLE)
            title_loc.wait_for(state="visible", timeout=5000)
            text = title_loc.text_content().strip()
            logger.info("Page title text: '%s'", text)
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
            logger.info("Component header title: '%s'", text)
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

    def search_status_log(self, search_term):
        logger.info("Searching Status Update Log for term: %s", search_term)
        search_helper = SearchHelper(self.page)
        search_helper.run_search(str(search_term))

    def clear_search_input(self):
        logger.info("Clearing search input field")
        input_loc = self.page.locator(self.SEARCH_INPUT).first
        input_loc.wait_for(state="visible", timeout=5000)
        input_loc.fill("")
        input_loc.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=10000)

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
            logger.debug("Retrieved %s table rows: %s", len(rows_data), rows_data)
        except Exception as e:
            logger.error("Failed to get table rows: %s", e)
        return rows_data

    def get_first_row_data(self):
        rows = self.get_table_rows()
        return rows[0] if rows else {}

    @staticmethod
    def _xpath_literal(value):
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ', "\'", '.join(f"'{part}'" for part in parts) + ")"

    def _row_locator_for_vin(self, vin_no):
        xpath_vin = self._xpath_literal(str(vin_no).strip())
        return self.page.locator(
            f"//tr[td[1][normalize-space(.)={xpath_vin}]]"
        ).first

    def is_vin_present_in_table(self, vin_no, timeout=10000):
        logger.info("Checking if VIN '%s' is present in table", vin_no)
        try:
            row_locator = self._row_locator_for_vin(vin_no)
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("VIN '%s' present in table: %s", vin_no, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("VIN '%s' not found in table within %s ms: %s", vin_no, timeout, e)
            return False

    def get_row_details_by_vin(self, vin_no):
        logger.info("Getting row details for VIN: %s", vin_no)
        try:
            headers = self.get_table_headers()
            row_locator = self._row_locator_for_vin(vin_no)
            cells = [td.text_content().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for VIN '%s': %s", vin_no, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for VIN '%s': %s", vin_no, e)
            return {}

    def get_search_tooltip_text(self):
        try:
            tooltip_el = self.page.locator("app-common-search")
            return tooltip_el.get_attribute("ng-reflect-message") or tooltip_el.get_attribute("mattooltip") or ""
        except Exception:
            return ""

    def is_pagination_visible(self, timeout=10000):
        try:
            loc = self.page.locator(self.PAGINATION_CONTAINER)
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error("Pagination container not visible within %s ms: %s", timeout, e)
            return False

    def get_selected_rows_per_page(self):
        try:
            loc = self.page.locator(self.ROWS_SELECT)
            loc.wait_for(state="visible", timeout=10000)
            val = loc.input_value()
            logger.debug("Current rows per page selected: %s", val)
            return val
        except Exception as e:
            logger.error("Failed to get rows per page: %s", e)
            return ""

    def select_rows_per_page(self, option_value):
        logger.info("Selecting %s rows per page", option_value)
        loc = self.page.locator(self.ROWS_SELECT)
        loc.wait_for(state="visible", timeout=10000)
        loc.select_option(str(option_value))

    def validate_pagination(self):
        logger.info("Validating pagination on Status Update Log page")
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
