import os
from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDispatchedDevicePage(BasePage):
    PAGE_CONTAINER = "app-dispatch-device-list, app-dispatch-device, .main-container"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    ADD_DISPATCH_BTN = "button.primary-button:has-text('Add'), button:has-text('Add Dispatch Device'), button:has-text('Add Dispatched Device')"
    SEARCH_INPUT = "input[formcontrolname='searchInput']"
    SEARCH_BTN = "button.search-btn"
    TABLE = ".component-body table"
    TABLE_HEADERS = ".component-body table tr th"
    TABLE_ROWS = ".component-body table tbody tr"
    PAGINATION_CONTAINER = "app-common-component-pagination, .pagination-container"
    ROWS_SELECT = "select#rowsSelect"
    BACK_BTN = ".back-button"
    RELOAD_BTN = ".reload-button"
    TOAST_MESSAGE = ".mat-mdc-snack-bar-label, simple-snack-bar, [data-sonner-toast]"

    # Add/Upload Page Locators
    FILE_INPUT = "input[type='file']"
    UPLOAD_SUBMIT_BTN = "button.edit-button:has-text('Upload'), button:has-text('Upload')"
    DOWNLOAD_SAMPLE_BTN = "button.primary-button:has-text('Download Sample Template')"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuDispatchedDevicePage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuDispatchedDevicePage is loaded")
        try:
            self.page.locator(self.PAGE_CONTAINER).first.wait_for(
                state="visible", timeout=10000
            )
            is_vis = self.page.locator(self.PAGE_CONTAINER).first.is_visible()
            logger.info("AtcuDispatchedDevicePage load status: %s", is_vis)
            return is_vis
        except Exception as e:
            logger.error("AtcuDispatchedDevicePage load check failed: %s", e)
            return False

    def get_title(self):
        logger.info("Retrieving AtcuDispatchedDevicePage title")
        try:
            title_loc = self.page.locator(self.PAGE_TITLE).first
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

    def click_add_dispatched_device_button(self):
        logger.info("Clicking Add Dispatched Device button")
        btn = self.page.locator(self.ADD_DISPATCH_BTN).first
        btn.wait_for(state="visible", timeout=10000)
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def click_back_button(self):
        logger.info("Clicking Back button")
        self.page.locator(self.BACK_BTN).first.click()

    def click_reload_button(self):
        logger.info("Clicking Reload button")
        self.page.locator(self.RELOAD_BTN).first.click()
        self.page.wait_for_load_state("networkidle")

    def search_dispatched_device(self, search_term):
        logger.info("Searching Dispatched Devices for term: %s", search_term)
        try:
            input_loc = self.page.locator(self.SEARCH_INPUT).first
            input_loc.wait_for(state="visible", timeout=10000)
            input_loc.fill(str(search_term))
            input_loc.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
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

    def is_device_present_in_table(self, search_term, timeout=10000):
        logger.info("Checking if device '%s' is present in Dispatched Devices table", search_term)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{search_term}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("Device '%s' present in table: %s", search_term, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("Device '%s' not found in table within %s ms: %s", search_term, timeout, e)
            return False

    def get_row_details_by_device(self, search_term):
        logger.info("Getting row details for device: %s", search_term)
        try:
            headers = self.get_table_headers()
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{search_term}')]]").first
            cells = [td.text_content().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for device '%s': %s", search_term, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for device '%s': %s", search_term, e)
            return {}

    def get_search_tooltip_text(self):
        try:
            tooltip_el = self.page.locator("app-common-search")
            return tooltip_el.get_attribute("ng-reflect-message") or tooltip_el.get_attribute("mattooltip") or ""
        except Exception:
            return ""

    def upload_dispatch_file(self, file_path):
        logger.info("Uploading dispatch file: %s", file_path)
        file_input = self.page.locator(self.FILE_INPUT).first
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(500)

    def is_upload_submit_button_enabled(self):
        try:
            btn = self.page.locator(self.UPLOAD_SUBMIT_BTN).first
            return btn.is_enabled()
        except Exception:
            return False

    def click_upload_submit_button(self):
        logger.info("Clicking Upload button on Add Dispatched Device page")
        btn = self.page.locator(self.UPLOAD_SUBMIT_BTN).first
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def download_sample_template(self):
        logger.info("Clicking Download Sample Template button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_SAMPLE_BTN).first.click()
        download = download_info.value
        logger.info("Downloaded sample dispatch template file: %s", download.suggested_filename)
        return download

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
        logger.info("Validating pagination on Dispatched Devices page")
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
