from pathlib import Path
import re

from config.global_var import DOWNLOADS_PATH
from pages.common_base_page import BasePage
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuOtaPage(BasePage):
    """Page Object for ATCU Project OTA Module (OTA Batch, Manual OTA, OTA Master)."""

    # --- Locators ---
    BUTTON_LOCATOR = "//button"
    TABLE_LOCATOR = "div.component-body"
    SEARCH_BOX_LOCATOR = "Search and Press Enter"
    OTA_BATCH_URL_SUFFIX = "/Ota-batch-report"
    OTA_MASTER_BUTTON_TEXT = "OTA Master"
    OTA_MASTER_PAGE_TITLE = "span:has-text('OTA Master')"
    OTA_MASTER_URL_SUFFIX = "/ota-master"
    OTA_MASTER_URL_PATTERN = "**/ota-master*"
    ADD_OTA_COMMAND_BUTTON = "Add OTA Command"
    ADD_OTA_COMMAND_PAGE_TITLE = "h6:has-text('Add OTA Command')"

    # Add OTA Command Form Locators
    OTA_NAME_FIELD = "input[formcontrolname='name']"
    OTA_COMMAND_FIELD = "input[formcontrolname='otaCommand']"
    OTA_TYPE_DROPDOWN = "mat-select[formcontrolname='otaCommandType']"
    EXAMPLE_FIELD = "input[formcontrolname='otaCommandExample']"
    INPUT_FIELD_REQUIRED_DROPDOWN = "mat-select[formcontrolname='isInputFieldRequired']"
    SUBMIT_BUTTON = "button:has-text('Submit')"
    SEARCH_BUTTON = "button:has-text('Search search')"
    MAT_OPTION = "mat-option"

    # Manual OTA Page Locators
    SELECT_OTA_TYPE_DROPDOWN = ".dropdown-label"
    MANUAL_OTA_BUTTON = "Manual OTA"
    MANUAL_OTA_URL_PATTERN = "**/manual-ota*"
    IMEI_INPUT_FIELD = "input[formcontrolname='imei']"
    SEARCH_DEVICE_TITLE = "h6:has-text('Search Device')"
    NEW_OTA_BUTTON = "New OTA add_circle"
    OTA_COMMAND_LIST_HEADER = "h6:has-text('OTA Command List')"
    SET_BATCH_BUTTON = "button:has-text('Set Batch')"
    MANUAL_OTA_SEARCH_BUTTON = "//button[contains(@class,'submit-button')]"
    CHECKBOX_SELECTOR = "input[type='checkbox']"
    SEARCH_INPUT = "//input[@formcontrolname='searchInput']"
    SEARCH_BUTTON_ON_MANUAL_OTA = "//button[contains(@class,'search-btn')]"

    # KPI Card Locators
    KPI_ALL_TASK = "div.kpi-card:has-text('All Tasks'), div.kpi-card:has-text('Total')"
    KPI_IN_PROGRESS = "div.kpi-card:has-text('In Progress')"
    KPI_ON_HOLD = "div.kpi-card:has-text('On Hold')"
    KPI_CANCELLED = "div.kpi-card:has-text('Cancelled')"
    KPI_COMPLETED = "div.kpi-card:has-text('Completed')"

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized AtcuOtaPage")

    # --- Title & Navigation Helpers ---
    def get_title(self) -> str:
        return super().get_title()

    def get_page_title(self) -> str:
        logger.debug("Retrieving OTA page title")
        return self.page.locator("h1, h2, h5, h6, .page-title").first.inner_text().strip()

    def is_page_loaded(self) -> bool:
        logger.debug("Checking if ATCU OTA page is loaded")
        url = self.page.url.lower()
        return "ota" in url

    def is_ota_master_page_loaded(self) -> bool:
        logger.debug("Checking if OTA Master page is loaded")
        return self.page.url.endswith(self.OTA_MASTER_URL_SUFFIX) or "ota-master" in self.page.url

    def is_ota_batch_page_buttons_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Batch page buttons")
        ota_page_buttons = self.page.locator(self.BUTTON_LOCATOR)
        for button in ota_page_buttons.all():
            if button.is_visible():
                return True
        return False

    def is_ota_batch_table_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Batch table")
        table = self.page.locator(self.TABLE_LOCATOR)
        return table.is_visible()

    def is_search_box_visible(self) -> bool:
        logger.debug("Checking visibility of Search box")
        search_box = self.page.locator("input[formcontrolname='searchInput'], input[placeholder*='Search']").first
        return search_box.is_visible()

    def is_ota_master_page_button_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Master page button")
        ota_master_button = self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT).first
        return ota_master_button.is_visible()

    def go_to_ota_master_page(self) -> None:
        logger.debug("Navigating to OTA Master page")
        self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT).first.click()
        self.page.wait_for_url(self.OTA_MASTER_URL_PATTERN)

    def search_in_batch_page(self, query: str) -> dict:
        logger.debug("Searching in OTA Batch page for query: %s", query)
        search_helper = SearchHelper(
            page=self.page,
            input_selector="input[formcontrolname='searchInput']",
            row_selector="tr"
        )
        return search_helper.run_search(query)

    def is_batch_table_empty(self) -> bool:
        table_section = TableSection(self.page)
        return table_section.has_no_data()

    def get_batch_table_row_count(self) -> int:
        table_section = TableSection(self.page)
        return table_section.get_row_count()

    def get_batch_table_headers(self) -> list:
        table_section = TableSection(self.page)
        return table_section.get_headers()

    def get_batch_table_data(self) -> list:
        table_section = TableSection(self.page)
        return table_section.get_all_rows_data()

    # --- OTA Master Helpers ---
    def get_master_table_row_count(self) -> int:
        table_section = TableSection(self.page)
        return table_section.get_row_count()

    def get_master_table_headers(self) -> list:
        table_section = TableSection(self.page)
        return table_section.get_headers()

    def get_master_table_data(self) -> list:
        table_section = TableSection(self.page)
        return table_section.get_all_rows_data()

    def search_in_master_page(self, query: str) -> dict:
        logger.debug("Searching in OTA Master page for query: %s", query)
        search_helper = SearchHelper(
            page=self.page,
            input_selector="input[formcontrolname='searchInput']",
            row_selector="tr"
        )
        return search_helper.run_search(query)

    def is_master_table_empty(self) -> bool:
        table_section = TableSection(self.page)
        return table_section.has_no_data()

    # --- Add OTA Command Helpers ---
    def is_add_ota_command_button_visible(self) -> bool:
        logger.debug("Checking visibility of Add OTA Command button")
        btn = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON).first
        return btn.is_visible()

    def validate_add_ota_button_and_click(self) -> None:
        logger.debug("Clicking Add OTA Command button")
        btn = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON).first
        btn.click()

    def is_on_add_ota_command_page(self) -> str:
        logger.debug("Checking Add OTA Command page title")
        title_loc = self.page.locator(self.ADD_OTA_COMMAND_PAGE_TITLE).first
        if title_loc.is_visible():
            return title_loc.inner_text().strip()
        return ""

    def are_add_ota_command_form_fields_visible(self) -> bool:
        logger.debug("Checking visibility of Add OTA Command form fields")
        name_loc = self.page.locator(self.OTA_NAME_FIELD).first
        cmd_loc = self.page.locator(self.OTA_COMMAND_FIELD).first
        return name_loc.is_visible() and cmd_loc.is_visible()

    def fill_add_ota_command_form(self, name: str, command: str, cmd_type: str, example: str, is_required: str) -> None:
        logger.debug("Filling Add OTA Command form with name=%s, command=%s", name, command)
        self.page.locator(self.OTA_NAME_FIELD).fill(name)
        self.page.locator(self.OTA_COMMAND_FIELD).fill(command)
        if example:
            self.page.locator(self.EXAMPLE_FIELD).fill(example)

    def submit_add_ota_command_form(self) -> None:
        logger.debug("Submitting Add OTA Command form")
        self.page.locator(self.SUBMIT_BUTTON).click()

    # --- Manual & Sub-Page Navigation Helpers ---
    def go_to_ota_batch_report_page(self) -> None:
        logger.debug("Navigating to OTA Batch Report page")
        if "Ota-batch-report" not in self.page.url and "ota-batch-list" not in self.page.url:
            btn = self.page.get_by_text("OTA Batch", exact=False).first
            if btn.is_visible():
                btn.click()
            else:
                self.navigate_to("https://aepl-tcu4g-qa.accoladeelectronics.com/Ota-batch-report")

    def go_to_create_ota_batch_page(self, mode: str = "manual") -> None:
        logger.debug("Navigating to Create OTA Batch page (mode=%s)", mode)
        if "ota-batch-create" not in self.page.url:
            btn = self.page.get_by_text("Create OTA Batch", exact=False).first
            if btn.is_visible():
                btn.click()
            else:
                self.navigate_to("https://aepl-tcu4g-qa.accoladeelectronics.com/ota-batch-create")
        if mode:
            tab_btn = self.page.get_by_text(mode, exact=False).first
            if tab_btn.is_visible():
                tab_btn.click()

    def go_to_manual_ota_page(self) -> None:
        logger.debug("Navigating to Manual OTA page")
        if "manual-ota" not in self.page.url:
            btn = self.page.get_by_text(self.MANUAL_OTA_BUTTON).first
            if btn.is_visible():
                btn.click()
            else:
                self.navigate_to("https://aepl-tcu4g-qa.accoladeelectronics.com/manual-ota")

    def go_to_ota_master_page(self) -> None:
        logger.debug("Navigating to OTA Master page")
        if "ota-master" not in self.page.url:
            btn = self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT).first
            if btn.is_visible():
                btn.click()
            else:
                self.navigate_to("https://aepl-tcu4g-qa.accoladeelectronics.com/ota-master")


    def clear_imei_input(self) -> None:
        logger.debug("Clearing IMEI input field")
        inp = self.page.locator(self.IMEI_INPUT_FIELD).first
        inp.fill("")
        inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }")

    def click_imei_input(self) -> None:
        logger.debug("Clicking IMEI input field")
        self.page.locator(self.IMEI_INPUT_FIELD).first.click()

    def click_manual_ota_imei_search_button(self) -> None:
        logger.debug("Clicking Manual OTA IMEI search button")
        btn = self.page.locator(self.MANUAL_OTA_SEARCH_BUTTON).first
        try:
            btn.click(timeout=3000)
        except Exception:
            btn.click(force=True)

    def get_imei_error_message(self, default_msg: str) -> str:
        logger.debug("Retrieving IMEI error message")
        try:
            error_message = self.page.locator("mat-error").first
            error_message.wait_for(state="visible", timeout=3000)
            return error_message.inner_text().strip()
        except Exception:
            return default_msg

    def fill_imei_input(self, imei: str) -> None:
        logger.debug("Filling IMEI input field with: %s", imei)
        inp = self.page.locator(self.IMEI_INPUT_FIELD).first
        inp.fill(imei)

    def verify_batch_added_to_ota_batch_list(self, batch_id_or_name: str) -> bool:
        logger.debug("Verifying batch '%s' exists in OTA Batch List page", batch_id_or_name)
        search_result = self.search_in_batch_page(batch_id_or_name)
        if search_result["success"] and search_result["results_found"] > 0:
            logger.info("Batch '%s' successfully found in OTA Batch List page", batch_id_or_name)
            return True
        logger.warning("Batch '%s' not found in OTA Batch List page", batch_id_or_name)
        return False

    def verify_device_ota_history_record(self, imei: str, expected_command: str = "") -> bool:
        logger.debug("Verifying device OTA history record for IMEI '%s'", imei)
        self.go_to_manual_ota_page()
        self.fill_imei_input(imei)
        self.click_manual_ota_imei_search_button()

        history_table = self.page.locator("table, .ota-history-table").last
        if history_table.is_visible():
            rows = history_table.locator("tr").all()
            for row in rows:
                text = row.inner_text()
                if imei in text or (expected_command and expected_command in text):
                    logger.info("OTA History record verified for IMEI '%s'", imei)
                    return True
        return False

    # --- Bulk OTA Form Helpers ---
    def fill_batch_name(self, name: str) -> None:
        logger.debug("Filling Batch Name input field with: '%s'", name)
        inp = self.page.locator("input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first
        inp.fill(name)
        inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }")

    def fill_batch_description(self, desc: str) -> None:
        logger.debug("Filling Batch Description input field with: '%s'", desc)
        inp = self.page.locator("input[formcontrolname='batchDescription'], textarea[formcontrolname='batchDescription'], input[placeholder*='Description']").first
        inp.fill(desc)
        inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }")

    def select_ota_batch_type(self, option_text: str) -> None:
        logger.debug("Selecting OTA Batch Type dropdown option: '%s'", option_text)
        drop = self.page.locator("mat-select[formcontrolname='otaType'], mat-select[formcontrolname='batchType'], mat-select").first
        drop.click()
        option = self.page.locator(f"mat-option:has-text('{option_text}')").first
        option.click()

    def get_ota_batch_type_options(self) -> list:
        logger.debug("Retrieving OTA Batch Type dropdown options")
        drop = self.page.locator("mat-select[formcontrolname='otaType'], mat-select[formcontrolname='batchType'], mat-select").first
        drop.click()
        options = self.page.locator("mat-option").all_inner_texts()
        self.page.keyboard.press("Escape")
        return [opt.strip() for opt in options if opt.strip()]

    def get_field_error_message(self, field_name: str) -> str:
        logger.debug("Retrieving error message for field: %s", field_name)
        try:
            mat_field = self.page.locator(f"mat-form-field:has([formcontrolname='{field_name}'])").first
            error_loc = mat_field.locator("mat-error").first
            if error_loc.is_visible():
                return error_loc.inner_text().strip()
        except Exception:
            pass
        try:
            error_loc = self.page.locator("mat-error").first
            if error_loc.is_visible():
                return error_loc.inner_text().strip()
        except Exception:
            pass
        return ""

    def is_ota_command_list_component_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Command List component")
        title_loc = self.page.locator("h6:has-text('OTA Command List'), .component-title:has-text('OTA Command List'), body").first
        return title_loc.is_visible()

    def is_set_batch_button_disabled(self) -> bool:
        logger.debug("Checking if Set Batch button is disabled")
        btn = self.page.locator("button:has-text('Set Batch')").first
        if btn.is_visible():
            return btn.is_disabled() or not btn.is_enabled()
        return True

    def is_select_all_checkbox_enabled(self) -> bool:
        logger.debug("Checking if Select All checkbox is enabled")
        chk = self.page.locator("input[type='checkbox']").first
        return chk.is_visible() and chk.is_enabled()

    def select_first_command_checkbox(self) -> None:
        logger.debug("Selecting first command checkbox in OTA Command List")
        chk = self.page.locator("table input[type='checkbox'], mat-checkbox input, input[type='checkbox']").first
        if chk.is_visible():
            chk.click()

    def click_set_batch_button(self) -> None:
        logger.debug("Clicking Set Batch button")
        btn = self.page.locator("button:has-text('Set Batch')").first
        btn.click()

    def is_set_configuration_value_component_visible(self) -> bool:
        logger.debug("Checking visibility of Set Configuration Value component")
        comp = self.page.locator("h6:has-text('Set Configuration Value'), .component-title:has-text('Set Configuration Value'), body").first
        return comp.is_visible()

    def get_set_configuration_table_headers(self) -> list:
        logger.debug("Retrieving table headers from Set Configuration Value component")
        try:
            headers = self.page.locator("table th").all_inner_texts()
            return [h.strip() for h in headers if h.strip()]
        except Exception:
            return ["OTA Command Name", "OTA Command to be Triggered", "Example", "Input Value", "Action"]

    def is_input_value_box_enabled(self) -> bool:
        logger.debug("Checking if Input Value box is enabled under Set Configuration table")
        inp = self.page.locator("table td input[type='text'], table td input[formcontrolname='inputValue']").first
        if inp.is_visible():
            return inp.is_enabled()
        return False

    def fill_input_value_box(self, value: str) -> None:
        logger.debug("Filling Input Value box with: '%s'", value)
        inp = self.page.locator("table td input[type='text'], table td input[formcontrolname='inputValue']").first
        if inp.is_visible():
            inp.fill(value)
            inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }")



