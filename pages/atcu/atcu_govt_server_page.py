from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuGovtServerPage(BasePage):
    # Main Page Locators (/govt-servers)
    PAGE_CONTAINER = "app-govt-servers-page"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    ADD_GOVT_SERVER_BTN = "button.primary-button:has-text('Add Government server')"
    DOWNLOAD_REPORT_BTN = "button.primary-button:has-text('Download Report')"
    SEARCH_INPUT = "input[formcontrolname='searchInput']"
    SEARCH_BTN = "button.search-btn"
    TABLE = ".component-body table"
    TABLE_HEADERS = ".component-body table thead th"
    TABLE_ROWS = ".component-body table tbody tr"
    PAGINATION_CONTAINER = "app-common-component-pagination, .pagination-container"
    ROWS_SELECT = "select#rowsSelect"
    BACK_BTN = ".back-button"
    RELOAD_BTN = ".reload-button"
    COMPONENT_HEADER = ".component-header"
    TOAST_MESSAGE = ".mat-mdc-snack-bar-label, simple-snack-bar, [data-sonner-toast]"

    # Details/Add Page Locators (/govt-servers-add)
    ADD_PAGE_CONTAINER = "app-govt-servers-add-page"
    STATE_INPUT = "input[formcontrolname='state']"
    STATE_ABBR_INPUT = "input[formcontrolname='stateAbbreviation']"
    STATE_ENABLE_INPUT = "input[formcontrolname='stateEnable']"
    GOVT_IP1_INPUT = "input[formcontrolname='govtIp1']"
    PORT1_INPUT = "input[formcontrolname='port1']"
    GOVT_IP2_INPUT = "input[formcontrolname='govtIp2']"
    PORT2_INPUT = "input[formcontrolname='port2']"
    SUBMIT_BTN = "button.submit-button"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuGovtServerPage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuGovtServerPage is loaded")
        try:
            self.page.locator(self.PAGE_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            is_vis = self.page.locator(self.PAGE_CONTAINER).is_visible()
            logger.info("AtcuGovtServerPage load status: %s", is_vis)
            return is_vis
        except Exception as e:
            logger.error("AtcuGovtServerPage load check failed: %s", e)
            return False

    def get_title(self):
        logger.info("Retrieving AtcuGovtServerPage title")
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

    def is_add_govt_server_button_visible(self):
        logger.info("Checking visibility of Add Government server button")
        try:
            btn = self.page.locator(self.ADD_GOVT_SERVER_BTN)
            return btn.is_visible() and "Add Government server" in btn.text_content()
        except Exception:
            return False

    def click_add_govt_server_button(self):
        logger.info("Clicking Add Government server button")
        btn = self.page.locator(self.ADD_GOVT_SERVER_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle")

    def is_download_report_button_visible(self):
        logger.info("Checking visibility of Download Report button")
        try:
            btn = self.page.locator(self.DOWNLOAD_REPORT_BTN)
            return btn.is_visible() and "Download Report" in btn.text_content()
        except Exception:
            return False

    def click_download_report_button(self):
        logger.info("Clicking Download Report button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_REPORT_BTN).click()
        download = download_info.value
        logger.info("Downloaded report file: %s", download.suggested_filename)
        return download

    def search_govt_server_list(self, search_term):
        logger.info("Searching Government Servers list for term: %s", search_term)
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

    def is_state_present_in_table(self, state_name_or_abbr, timeout=10000):
        logger.info("Checking if state '%s' is present in table", state_name_or_abbr)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name_or_abbr}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.first.is_visible()
            logger.info("State '%s' present in table: %s", state_name_or_abbr, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("State '%s' not found in table within %s ms: %s", state_name_or_abbr, timeout, e)
            return False

    def is_view_button_visible_for_row(self, state_name):
        logger.info("Checking View button visibility for state: %s", state_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name}')]]")
            view_btn = row_locator.locator("button.view-button, button:has(mat-icon:has-text('visibility'))").first
            return view_btn.is_visible()
        except Exception as e:
            logger.error("Failed to check View button visibility for '%s': %s", state_name, e)
            return False

    def click_view_button_for_row(self, state_name):
        logger.info("Clicking View button for state: %s", state_name)
        row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name}')]]")
        view_btn = row_locator.locator("button.view-button, button:has(mat-icon:has-text('visibility'))").first
        view_btn.wait_for(state="visible", timeout=5000)
        view_btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def is_delete_button_visible_for_row(self, state_name):
        logger.info("Checking Delete button visibility for state: %s", state_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name}')]]")
            delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
            return delete_btn.is_visible()
        except Exception as e:
            logger.error("Failed to check Delete button visibility for '%s': %s", state_name, e)
            return False

    def click_delete_button_for_row(self, state_name):
        logger.info("Clicking Delete button for state: %s", state_name)
        row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name}')]]")
        delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
        delete_btn.wait_for(state="visible", timeout=5000)
        self.page.on("dialog", lambda dialog: dialog.accept())
        delete_btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

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
        logger.info("Validating pagination on Government Servers page")
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

    # --- Add/Update Government Servers Details Methods (/govt-servers-add) ---

    def is_add_page_loaded(self):
        logger.info("Checking if Add Government Servers page is loaded")
        try:
            add_page = self.page.locator(self.ADD_PAGE_CONTAINER)
            add_page.wait_for(
                state="visible", timeout=10000
            )
            is_visible = add_page.is_visible()
            logger.info("Add Government Servers page load status: %s", is_visible)
            return is_visible
        except Exception as e:
            logger.error("Add Government Servers page load check failed: %s", e)
            return False

    def is_view_page_loaded(self):
        logger.info("Checking if View Government Servers page is loaded")
        page_header = self.page.locator(self.COMPONENT_HEADER)
        page_header.wait_for(state="visible", timeout=10000)
        is_visible = page_header.is_visible()
        logger.info("View Government Servers page load status: %s", is_visible)
        return is_visible

    def get_add_page_title(self):
        try:
            loc = self.page.locator(self.PAGE_TITLE)
            loc.wait_for(state="visible", timeout=5000)
            return loc.text_content().strip()
        except Exception as e:
            logger.error("Failed to get Add Government Servers page title: %s", e)
            return ""

    def get_add_component_title(self):
        try:
            loc = self.page.locator(self.COMPONENT_TITLE).first
            loc.wait_for(state="visible", timeout=5000)
            return loc.text_content().strip()
        except Exception as e:
            logger.error("Failed to get Add Government Servers component title: %s", e)
            return ""

    def fill_add_govt_server_form(
        self,
        state=None,
        state_abbr=None,
        state_enable=None,
        govt_ip1=None,
        port1=None,
        govt_ip2=None,
        port2=None,
    ):
        logger.info("Filling Add Government Server form: State='%s', Abbr='%s'", state, state_abbr)
        if state is not None:
            self.page.locator(self.STATE_INPUT).fill(state)
        if state_abbr is not None:
            self.page.locator(self.STATE_ABBR_INPUT).fill(state_abbr)
        if state_enable is not None:
            self.page.locator(self.STATE_ENABLE_INPUT).fill(state_enable)
        if govt_ip1 is not None:
            self.page.locator(self.GOVT_IP1_INPUT).fill(govt_ip1)
        if port1 is not None:
            self.page.locator(self.PORT1_INPUT).fill(port1)
        if govt_ip2 is not None:
            self.page.locator(self.GOVT_IP2_INPUT).fill(govt_ip2)
        if port2 is not None:
            self.page.locator(self.PORT2_INPUT).fill(port2)

    def is_submit_button_enabled(self):
        try:
            btn = self.page.locator(self.SUBMIT_BTN)
            return btn.is_enabled()
        except Exception:
            return False

    def click_submit_button(self):
        logger.info("Clicking Submit button on Add Government Server form")
        btn = self.page.locator(self.SUBMIT_BTN)
        btn.wait_for(state="visible", timeout=5000)
        self.is_submit_button_enabled()  # Ensure the button is enabled before clicking
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def get_input_fields_locators(self):
        return {
            "state": self.page.locator(self.STATE_INPUT),
            "stateAbbreviation": self.page.locator(self.STATE_ABBR_INPUT),
            "stateEnable": self.page.locator(self.STATE_ENABLE_INPUT),
            "govtIp1": self.page.locator(self.GOVT_IP1_INPUT),
            "port1": self.page.locator(self.PORT1_INPUT),
            "govtIp2": self.page.locator(self.GOVT_IP2_INPUT),
            "port2": self.page.locator(self.PORT2_INPUT),
        }

    def get_input_field_values(self):
        fields = self.get_input_fields_locators()
        return {name: loc.input_value() for name, loc in fields.items()}

    def get_search_tooltip_text(self):
        try:
            tooltip_el = self.page.locator("app-common-search")
            return tooltip_el.get_attribute("ng-reflect-message") or tooltip_el.get_attribute("mattooltip") or ""
        except Exception:
            return ""

    def get_row_details_by_state(self, state_name):
        logger.info("Getting row details for state: %s", state_name)
        try:
            headers = self.get_table_headers()
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{state_name}')]]").first
            cells = [td.text_content().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for state '%s': %s", state_name, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for state '%s': %s", state_name, e)
            return {}
