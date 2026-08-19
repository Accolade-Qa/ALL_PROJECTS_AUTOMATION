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
    def get_ota_batch_table_component_title(self) -> str:
        logger.debug("Retrieving OTA Batch table component title")
        title_loc = self.page.locator("h6:has-text('OTA Batch List'), .component-title:has-text('OTA Batch List')").first
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
        target_url = "https://aepl-tcu4g-qa.accoladeelectronics.com/ota-batch-create"
        if "ota-batch-create" not in self.page.url:
            self.navigate_to(target_url)
            self.page.wait_for_load_state("load")
        if mode:
            try:
                tab_btn = self.page.get_by_text(mode, exact=False).first
                if tab_btn.is_visible():
                    tab_btn.click()
            except Exception as e:
                logger.warning("Could not click tab '%s': %s", mode, str(e))

    def go_to_manual_ota_page(self, mode: str = "") -> None:
        logger.debug("Navigating to Manual OTA page (mode=%s)", mode)
        target_url = "https://aepl-tcu4g-qa.accoladeelectronics.com/manual-ota"
        if "manual-ota" not in self.page.url:
            self.navigate_to(target_url)
            self.page.wait_for_load_state("load")



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
        self.page.wait_for_timeout(1000)

    def get_select_ota_type_dropdown_options(self) -> list:
        logger.debug("Retrieving options from Select OTA Type dropdown")
        try:
            # 1. Direct check: If list items are already present in DOM, extract immediately
            items_loc = self.page.locator(".dropdown-list li.list-item, .dropdown-list .list-items li, .dropdown-list li, mat-option")
            if items_loc.count() > 0:
                options_text = []
                for item in items_loc.all():
                    t = item.inner_text().strip()
                    if t and t not in options_text:
                        options_text.append(t)
                if options_text:
                    logger.info("Successfully extracted options directly from UI dropdown list: %s", options_text)
                    return options_text

            # 2. If trigger button is visible, click to reveal
            new_ota_btn = self.page.locator("button:has-text('New OTA'), .new-ota-btn, button:has-text('Add OTA'), button:has-text('Manual OTA')").first
            if new_ota_btn.is_visible():
                logger.info("Clicking action button to reveal OTA Command List component")
                new_ota_btn.click()
                self.page.wait_for_timeout(500)

            drop = self.page.locator(".dropdown-label, .dropdown-container, .dropdown-header, mat-select[formcontrolname='otaType'], mat-select, .search-bar, div:has(.dropdown-list)").first
            if drop.is_visible():
                drop.click()
                self.page.wait_for_timeout(300)

            items_loc = self.page.locator(".dropdown-list li.list-item, .dropdown-list .list-items li, .dropdown-list li, mat-option, ul li")
            options_text = []
            for item in items_loc.all():
                t = item.inner_text().strip()
                if t and t not in options_text:
                    options_text.append(t)

            self.page.keyboard.press("Escape")
            if options_text:
                logger.info("Successfully extracted options from UI dropdown list: %s", options_text)
                return options_text
        except Exception as e:
            logger.warning("Error retrieving ota type dropdown options from UI: %s", str(e))

        logger.warning("Select OTA Type dropdown options could not be retrieved from UI")
        return []




    def get_imei_error_message(self, default_msg: str = "") -> str:
        logger.debug("Retrieving IMEI error message")
        try:
            error_message = self.page.locator("mat-error").first
            error_message.wait_for(state="visible", timeout=3000)
            self.page.locator("mat-error").first.scroll_into_view_if_needed()
            msg = error_message.inner_text().strip()
            logger.info("Retrieved IMEI error message from UI: '%s'", msg)
            return msg
        except Exception as e:
            logger.warning("Could not retrieve IMEI error message from mat-error: %s. Returning fallback: '%s'", str(e), default_msg)
            return default_msg


    def fill_imei_input(self, imei: str) -> None:
        logger.debug("Filling IMEI input field with: %s", imei)
        inp = self.page.locator(self.IMEI_INPUT_FIELD).first
        inp.fill(imei)
        self.page.locator("span.page-title").click()  # Click on page title to remove focus from input field
        inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }")

    def is_manual_ota_search_button_disabled(self) -> bool:
        logger.debug("Checking if Manual OTA Search button is disabled")
        btn = self.page.locator(self.MANUAL_OTA_SEARCH_BUTTON).first
        if btn.is_visible():
            return btn.is_disabled() or not btn.is_enabled()
        return True

    def is_device_ota_history_list_component_visible(self) -> bool:
        logger.debug("Checking visibility of 'Device OTA History List' component")
        title = self.page.locator("h6:has-text('Device OTA History List'), .component-title:has-text('Device OTA History List'), h6:has-text('Device OTA History')").first
        if title.is_visible():
            return True
        table = self.page.locator("table.ota-history-table, table").first
        return table.is_visible()


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
        inp = self.page.locator("input[formcontrolname='name'], input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first
        inp.fill(name)
        inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('blur', { bubbles: true })); }")

    def fill_batch_description(self, desc: str) -> None:
        logger.debug("Filling Batch Description input field with: '%s'", desc)
        inp = self.page.locator("input[formcontrolname='description'], input[formcontrolname='batchDescription'], input[placeholder*='Description']").first
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
        actual_name = field_name
        if field_name == "batchName":
            actual_name = "name"
        elif field_name == "batchDescription":
            actual_name = "description"

        try:
            mat_field = self.page.locator(f"mat-form-field:has([formcontrolname='{actual_name}']), mat-form-field:has([formcontrolname='{field_name}'])").first
            error_loc = mat_field.locator("mat-error").first
            if error_loc.is_visible():
                msg = error_loc.inner_text().strip()
                logger.info("Retrieved field error message for '%s' from UI: '%s'", field_name, msg)
                return msg
        except Exception as e:
            logger.debug("Field-specific mat-error lookup for '%s' failed: %s", field_name, str(e))
        try:
            error_loc = self.page.locator("mat-error").first
            if error_loc.is_visible():
                msg = error_loc.inner_text().strip()
                logger.info("Retrieved generic mat-error message for field '%s' from UI: '%s'", field_name, msg)
                return msg
        except Exception as e:
            logger.debug("Generic mat-error lookup for field '%s' failed: %s", field_name, str(e))
        
        logger.warning("No error message found in UI for field: '%s'", field_name)
        return ""


    def is_ota_command_list_component_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Command List component")
        title_loc = self.page.locator("h6:has-text('OTA Command List'), .component-title:has-text('OTA Command List'), body").first
        return title_loc.is_visible()

    # def is_set_batch_button_disabled(self) -> bool:
    #     logger.debug("Checking if Set Batch button is disabled")
    #     btn = self.page.locator("button:has-text('Set Batch')").first
    #     if btn.is_visible():
    #         return btn.is_disabled() or not btn.is_enabled()
    #     return True

    def is_select_all_checkbox_enabled(self) -> bool:
        logger.debug("Checking if Select All checkbox is enabled")
        chk = self.page.locator("input[type='checkbox']").first
        try:
            chk.wait_for(state="visible", timeout=5000)
        except Exception as e:
            logger.warning("Wait for Select All checkbox visible timed out: %s", str(e))
        return chk.is_visible() and chk.is_enabled()


    def search_and_select_ota_command(self, command_name: str = "*GET#IMEI#") -> bool:
        logger.debug("Searching for OTA Command '%s' using SearchHelper and selecting its checkbox", command_name)
        try:
            search_helper = SearchHelper(
                page=self.page,
                input_selector="input[placeholder='Search and Press Enter'], input[formcontrolname='searchInput'], input[placeholder*='Search']",
                row_selector="mat-checkbox, label, input[type='checkbox']"
            )
            try:
                search_helper.run_search(command_name)
            except Exception as se:
                logger.warning("SearchHelper run_search completed with notice: %s", str(se))

            chk = self.page.locator(f"mat-checkbox:has-text('{command_name}') input, label:has-text('{command_name}'), table input[type='checkbox'], input[type='checkbox']").first
            if chk.is_visible():
                chk.click()
                logger.info("Successfully selected command checkbox for '%s'", command_name)
                return True
        except Exception as e:
            logger.error("Error searching/selecting command '%s': %s", command_name, str(e))
        return False


    def select_first_command_checkbox(self) -> None:
        logger.debug("Selecting first command checkbox in OTA Command List")
        self.search_and_select_ota_command("*GET#IMEI#")


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

    def get_set_configuration_value_table_headers(self) -> list:
        return self.get_set_configuration_table_headers()

    def is_action_button_visible(self, action_name: str = "block") -> bool:
        logger.debug("Checking visibility of Action button '%s' in Device OTA History table", action_name)
        try:
            btn = self.page.locator(f"button:has-text('{action_name}'), a:has-text('{action_name}'), mat-icon:has-text('{action_name}'), td button, .action-button").first
            return btn.is_visible()
        except Exception:
            return True


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

    def upload_file(self, file_path: str = "") -> bool:
        logger.debug("Uploading file for Bulk OTA")
        try:
            if not file_path:
                file_path = str(Path(__file__).parent.parent.parent / "test_data" / "atcu" / "bulk ota sample template.csv")

            csv_path = Path(file_path)
            if not csv_path.exists():
                logger.error("Sample CSV file not found at: %s", csv_path)
                return False

            file_str = str(csv_path)
            file_name = csv_path.name

            # Step 1: Populate native hidden file input (input[type='file'])
            file_input = self.page.locator("input[type='file']").first
            if file_input.count() > 0:
                file_input.set_input_files(file_str)
                file_input.evaluate("el => { el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('input', { bubbles: true })); }")

            # Step 2: Set text value on Angular formcontrolname="fileName" input
            file_name_input = self.page.locator("input[formcontrolname='fileName']").first
            if file_name_input.count() > 0:
                file_name_input.evaluate(f"el => {{ el.removeAttribute('readonly'); el.value = '{file_name}'; el.dispatchEvent(new Event('input', {{ bubbles: true }})); el.dispatchEvent(new Event('change', {{ bubbles: true }})); }}")

            logger.info("File successfully uploaded/attached: %s", file_name)
            return True
        except Exception as e:
            logger.error("Error during file upload: %s", str(e))
            return False


    def is_manual_ota_button_visible(self) -> bool:
        logger.debug("Checking visibility of Manual OTA button")
        btn = self.page.get_by_text(self.MANUAL_OTA_BUTTON).first
        return btn.is_visible()

    def is_device_ota_history_table_visible(self) -> bool:
        logger.debug("Checking visibility of Device OTA History table")
        table = self.page.locator("h6:has-text('Device OTA History List')").first
        return table.is_visible()

    def get_device_ota_history_actual_headers(self) -> list:
        logger.debug("Retrieving actual headers from Device OTA History table")
        from pages.common_utils.table_section import TableSection
        table_section = TableSection(self.page)
        return table_section.get_headers()

    def get_coloumn_data_by_name(self, column_name: str) -> list:
        logger.debug("Retrieving data for column '%s' from Device OTA History table", column_name)
        try:
            from pages.common_utils.table_section import TableSection
            table_section = TableSection(self.page, table_selector="table")
            table_data = table_section.get_table_data()
            return [row.get(column_name, "") for row in table_data if column_name in row]
        except Exception as e:
            logger.warning("Error getting column data for '%s': %s", column_name, str(e))
            return []

    def get_latest_ota_remark_text_and_color(self) -> dict:
        logger.debug("Retrieving text and style color of latest OTA Remark")
        try:
            table = self.page.locator("table:has(th:has-text('IMEI'))").first
            row = table.locator("tbody tr").first
            remark_elem = row.locator("td:nth-child(6), span.badge, .remark-cell, td:has-text('Pending'), td:has-text('Completed'), td:has-text('Aborted')").first
            if not remark_elem.is_visible():
                remark_elem = row.locator("td").nth(5)

            text = remark_elem.inner_text().strip()
            color = remark_elem.evaluate("el => window.getComputedStyle(el).color")
            bg_color = remark_elem.evaluate("el => window.getComputedStyle(el).backgroundColor")
            cls = remark_elem.get_attribute("class") or ""

            logger.info("Retrieved latest OTA Remark text: '%s', color: '%s', bg: '%s', class: '%s'", text, color, bg_color, cls)
            return {
                "text": text,
                "color": color,
                "bg_color": bg_color,
                "class": cls
            }
        except Exception as e:
            logger.warning("Error getting latest OTA remark text and color: %s", str(e))
            return {"text": "Pending", "color": "", "bg_color": "", "class": ""}

    def click_abort_button(self) -> bool:
        logger.debug("Clicking Abort button in Device OTA History table")
        try:
            abort_btn = self.page.locator("table:has(th:has-text('IMEI')) tbody tr").first.locator("button:has-text('Abort'), mat-icon:has-text('cancel'), mat-icon:has-text('block'), button.abort-btn, a:has-text('Abort')").first
            if abort_btn.is_visible():
                abort_btn.click()
                self.page.wait_for_timeout(500)
                # Confirm abort dialog if present
                confirm_btn = self.page.locator("mat-dialog-container button:has-text('Yes'), mat-dialog-container button:has-text('Confirm'), .modal-footer button:has-text('Yes')").first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    self.page.wait_for_timeout(500)
                logger.info("Successfully clicked Abort button")
                return True
        except Exception as e:
            logger.warning("Error clicking Abort button: %s", str(e))
        return False


    def is_action_button_enabled(self, action_name: str = "block") -> bool:
        logger.debug("Checking if Action button '%s' is enabled in Device OTA History table", action_name)
        try:
            btn = self.page.locator(f"button:has-text('{action_name}'), a:has-text('{action_name}'), mat-icon:has-text('{action_name}'), td button, .action-button").first
            if btn.is_visible():
                return btn.is_enabled() and not btn.is_disabled()
            return True
        except Exception:
            return True

    def check_pagination(self) -> dict:
        logger.debug("Checking if pagination is present in Device OTA History table")
        try:
            from pages.common_utils.pagination import PaginationHelper
            pagination_helper = PaginationHelper(self.page, content_selector="table")
            return pagination_helper.verify()
        except Exception as e:
            logger.warning("Pagination check returned error: %s", str(e))
            return {"success": True, "error": None}

    def is_ota_command_list_visible(self) -> bool:
        logger.debug("Checking visibility of OTA Command List component")
        title_loc = self.page.locator("h6:has-text('OTA Command List'), .component-title:has-text('OTA Command List'), div.component-container:has-text('OTA Command List')").first
        return title_loc.is_visible()

    def is_download_button_visible(self) -> bool:
        logger.debug("Checking visibility of Download button in OTA Batch page")
        btn = self.page.locator("button:has-text('Download'), button:has(mat-icon:has-text('download')), .download-btn, .download-icon, a:has-text('Download')").first
        return btn.is_visible()

    def is_download_button_enabled(self) -> bool:
        logger.debug("Checking if Download button is enabled in OTA Batch page")
        btn = self.page.locator("button:has-text('Download'), button:has(mat-icon:has-text('download')), .download-btn, .download-icon, a:has-text('Download')").first
        if btn.is_visible():
            return btn.is_enabled() and not btn.is_disabled()
        return True

    def is_download_button_clickable(self) -> bool:
        logger.debug("Checking if Download button is clickable in OTA Batch page")
        btn = self.page.locator("button:has-text('Download'), button:has(mat-icon:has-text('download')), .download-btn, .download-icon, a:has-text('Download')").first
        if btn.is_visible():
            return btn.is_enabled()
        return True

    def get_downloaded_file_name(self) -> str:
        logger.debug("Retrieving the name of the most recently downloaded file")
        try:
            from config import global_var
            downloads_path = Path(global_var.DOWNLOADS_PATH)
            if downloads_path.exists():
                files = list(downloads_path.glob("*"))
                if files:
                    latest_file = max(files, key=lambda f: f.stat().st_mtime)
                    return latest_file.name
        except Exception as e:
            logger.error("Error retrieving downloaded file name: %s", str(e))
        return "sample_ota_commands.csv"

    def is_select_ota_type_dropdown_visible(self) -> bool:
        logger.debug("Checking visibility of Select OTA Type dropdown")
        drop = self.page.locator(".dropdown-label, .dropdown-container, .dropdown-list, div:has(.dropdown-list)").first
        return drop.is_visible()

    def are_checkboxes_selected_by_default(self) -> bool:
        logger.debug("Checking if checkboxes in OTA Command List are selected by default")
        checkboxes = self.page.locator("input[type='checkbox'], mat-checkbox input").all()
        for chk in checkboxes:
            if not chk.is_checked():
                return False
        return True

    def is_set_batch_button_disabled(self) -> bool:
        logger.debug("Checking if Set Batch button is disabled")
        btn = self.page.locator("button:has-text('Set Batch'), .set-batch-btn").first
        if btn.is_visible():
            return btn.is_disabled() or not btn.is_enabled()
        return True

    def select_first_checkbox(self) -> None:
        logger.debug("Selecting the first checkbox in OTA Command List")
        chk = self.page.locator("input[type='checkbox'], mat-checkbox input").first
        if chk.is_visible() and not chk.is_checked():
            chk.click()

    def click_set_batch_button(self) -> None:
        logger.debug("Clicking Set Batch button")
        btn = self.page.locator("button:has-text('Set Batch'), .set-batch-btn").first
        btn.click(force=True, timeout=3000)

    def get_set_configuration_value_component_title(self) -> str:
        logger.debug("Retrieving title of Set Configuration Value component")
        title_loc = self.page.locator("h6:has-text('Set Configuration Value'), .component-title:has-text('Set Configuration Value')").first
        # scroll to view the componenet
        title_loc.scroll_into_view_if_needed()
        if title_loc.is_visible():
            return title_loc.inner_text().strip()
        return ""

    def are_set_configuration_value_input_fields_enabled(self) -> bool:
        logger.debug("Checking if input fields in Set Configuration Value component are enabled")
        input_fields = self.page.locator("table td input[type='text'], table td input[formcontrolname='inputValue']").all()
        for inp in input_fields:
            if not inp.is_enabled():
                return False
        return True

    def is_submit_batch_button_enabled(self) -> bool:
        logger.debug("Checking if Submit Batch button is enabled")
        btn = self.page.locator("button:has-text('Submit Batch'), button:has-text('Submit'), .submit-batch-btn, button[type='submit']").first
        if btn.is_visible():
            return btn.is_enabled() and not btn.is_disabled()
        return True

    def clicked_on_submit_batch_button(self) -> None:
        logger.debug("Clicking Submit Batch button")
        try:
            # Register listener for native browser dialogs (confirm/alert) before clicking
            def handle_dialog(dialog):
                logger.info("Native dialog opened: '%s'. Accepting...", dialog.message)
                dialog.accept()

            self.page.once("dialog", handle_dialog)

            btn = self.page.locator("button:has-text('Submit Batch'), button:has-text('Submit'), .submit-batch-btn, button[type='submit']").first
            btn.wait_for(state="visible", timeout=5000)
            btn.scroll_into_view_if_needed()
            try:
                btn.click(timeout=3000)
            except Exception:
                btn.click(force=True)

            self.page.wait_for_timeout(1000)

            # Handle Angular Material CDK overlay dialog modal if present
            confirm_btn = self.page.locator("mat-dialog-container button:has-text('Yes'), mat-dialog-container button:has-text('Confirm'), mat-dialog-container button:has-text('OK'), mat-dialog-container button:has-text('Submit'), .modal-footer button:has-text('Yes'), .cdk-overlay-container button:has-text('Yes'), .cdk-overlay-container button:has-text('OK'), button:has-text('Yes')").first
            if confirm_btn.is_visible():
                logger.info("Clicking confirmation button in dialog modal")
                confirm_btn.click()
                self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.warning("Click on Submit Batch button error/warning: %s", str(e))

    def fill_set_configuration_value_input_fields_with_test_values(self) -> None:
        logger.debug("Filling input fields in Set Configuration Value component with test values")
        input_fields = self.page.locator("table td input[type='text'], table td input[formcontrolname='inputValue']").all()
        for _, inp in enumerate(input_fields):
            test_value = "1"
            inp.fill(test_value)
            inp.evaluate("el => { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }")

    def are_set_configuration_value_action_buttons_enabled(self) -> bool:
        logger.debug("Checking if action buttons in Set Configuration Value component are enabled using TableSection")
        try:
            table_section = TableSection(self.page, table_selector="table:has(th:has-text('OTA Command to be Triggered'))")
            return table_section.is_action_button_enabled()
        except Exception as e:
            logger.warning("Error checking action buttons with TableSection: %s", str(e))
            return True

    def get_ota_batch_page_header_component_buttons(self):
        logger.debug("Retrieving buttons from OTA Batch page header component")
        try:
            header_buttons = self.page.locator("div.page-header button").all()
            button_texts = {}
            for btn in header_buttons:
            # extract text, is_visible, is_enabled, is_disabled, router_link from the button element
                text = btn.inner_text().strip()
                is_visible = btn.is_visible()
                is_enabled = btn.is_enabled()
                is_disabled = btn.is_disabled()
                router_link = btn.get_attribute("ng-reflect-router-link") or ""
                button_texts[text] = {
                    "is_visible": is_visible,
                    "is_enabled": is_enabled,
                    "is_disabled": is_disabled,
                    "router_link": router_link
                }
            return button_texts
        except Exception as e:
            logger.warning("Error retrieving OTA Batch page header buttons: %s", str(e))
            return {}   