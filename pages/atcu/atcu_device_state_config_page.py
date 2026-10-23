from utils.helpers import Helpers
from pages.common_base_page import BasePage
from pages.common_utils import SearchHelper, TableSection, PaginationHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDeviceStateConfigPage(BasePage):
    """
    This page object represents the ATCU Device State Config page (/device-state-config).
    """

    # Locators
    PAGE_TITLE = ".page-title"
    BACK_BUTTON = ".action-button.back-button"
    RELOAD_BUTTON = ".action-button.reload-button"
    COMPONENT_TITLE = ".component-title"
    DOWNLOAD_SAMPLE_BTN = "button.primary-button"
    FILE_LABEL = "label.form-label"
    FILE_NAME_INPUT = 'input[formcontrolname="fileName"]'
    FILE_INPUT = 'input[type="file"][accept=".csv"]'
    ATTACH_FILE_BTN = "button.upload-btn"
    UPLOAD_SUBMIT_BTN = "button.edit-button"
    TOAST_MESSAGE = '[data-sonner-toast], .toast-message, .alert, mat-snack-bar-container'

    # Upload Response Table Locators
    DOWNLOAD_REPORT_BTN = "button.primary-button"
    RESPONSE_TABLE = "table"
    RESPONSE_TABLE_HEADERS = "table thead th"
    RESPONSE_TABLE_ROWS = "table tbody tr"

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized AtcuDeviceStateConfigPage with page: %s", page)

    def get_title(self):
        """Returns the page title text."""
        try:
            if self.page.locator(self.PAGE_TITLE).is_visible(timeout=5000):
                title = self.page.locator(self.PAGE_TITLE).text_content().strip()
                logger.debug("AtcuDeviceStateConfigPage title: %s", title)
                return title
        except Exception:
            pass
        return super().get_title()

    def is_page_loaded(self):
        """Checks if the AtcuDeviceStateConfigPage is loaded successfully."""
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            is_title_visible = self.page.locator(self.PAGE_TITLE).is_visible()
            logger.debug("AtcuDeviceStateConfigPage loaded successfully. Title visible=%s", is_title_visible)
            return True
        except Exception as e:
            logger.error("AtcuDeviceStateConfigPage page failed to load: %s", e)
            return False

    def get_component_title(self):
        """Returns the component title text (e.g. 'Add Device State' or 'Device State Uploaded Files Response')."""
        try:
            title = self.page.locator(self.COMPONENT_TITLE).text_content().strip()
            logger.debug("Retrieved component title: %s", title)
            return title
        except Exception as e:
            logger.error("Failed to get component title: %s", e)
            return ""

    def get_file_upload_label(self):
        """Returns the file upload label text."""
        try:
            label = self.page.locator(self.FILE_LABEL).text_content().strip()
            logger.debug("Retrieved file upload label: %s", label)
            return label
        except Exception as e:
            logger.error("Failed to get file upload label: %s", e)
            return ""

    def click_back_button(self):
        """Clicks the back navigation button."""
        logger.info("Clicking back button on Device State Config page")
        self.page.locator(self.BACK_BUTTON).click()

    def click_reload_button(self):
        """Clicks the reload/refresh button."""
        logger.info("Clicking reload button on Device State Config page")
        self.page.locator(self.RELOAD_BUTTON).click()

    def is_download_sample_button_visible(self):
        """Checks if the Download Sample Excel Template button is visible."""
        visible = self.page.locator(self.DOWNLOAD_SAMPLE_BTN).is_visible()
        logger.debug("Download sample template button visible=%s", visible)
        return visible

    def click_download_sample_template(self):
        """Clicks the Download Sample Excel Template button and returns the download object."""
        logger.info("Clicking Download Sample Excel Template button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_SAMPLE_BTN).click()
        download = download_info.value
        logger.info("Downloaded file: %s", download.suggested_filename)
        return download

    def get_uploaded_file_name(self):
        """Gets the value displayed in the file name input field."""
        value = self.page.locator(self.FILE_NAME_INPUT).input_value()
        logger.debug("Current uploaded file name input value: '%s'", value)
        return value

    def get_file_input_accept_attribute(self):
        """Gets the accept attribute value of the hidden file input."""
        accept_attr = self.page.locator(self.FILE_INPUT).get_attribute("accept")
        logger.debug("File input accept attribute: '%s'", accept_attr)
        return accept_attr

    def is_upload_submit_button_enabled(self):
        """Checks whether the Upload submit button is enabled."""
        enabled = self.page.locator(self.UPLOAD_SUBMIT_BTN).is_enabled()
        logger.debug("Upload submit button enabled=%s", enabled)
        return enabled

    def upload_csv_file(self, file_path):
        """Sets the file on the hidden file input element."""
        logger.info("Uploading CSV file: %s", file_path)
        self.page.locator(self.FILE_INPUT).set_input_files(file_path)

    def click_upload_submit_button(self):
        """Clicks the Upload submit button."""
        logger.info("Clicking Upload submit button")
        self.page.locator(self.UPLOAD_SUBMIT_BTN).click()

    def get_toast_message(self, timeout=5000):
        """Gets text content of toast/alert notification if visible."""
        try:
            toast = self.page.locator(self.TOAST_MESSAGE)
            toast.wait_for(state="visible", timeout=timeout)
            text = toast.text_content().strip()
            logger.info("Toast notification text: '%s'", text)
            return text
        except Exception as e:
            logger.debug("No toast message displayed within %s ms: %s", timeout, e)
            return ""

    def is_response_table_visible(self, timeout=15000):
        """Checks if the uploaded files response table is visible."""
        try:
            self.page.locator(self.RESPONSE_TABLE).wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.debug("Response table not visible within %s ms: %s", timeout, e)
            return False

    def get_response_table_headers(self):
        """Returns list of column header names from the response table."""
        headers = []
        try:
            locators = self.page.locator(self.RESPONSE_TABLE_HEADERS).all()
            headers = [loc.text_content().strip() for loc in locators]
            logger.debug("Retrieved response table headers: %s", headers)
        except Exception as e:
            logger.error("Failed to get response table headers: %s", e)
        return headers

    def get_response_table_rows(self):
        """Returns list of row data dicts from response table."""
        rows_data = []
        try:
            headers = self.get_response_table_headers()
            row_elements = self.page.locator(self.RESPONSE_TABLE_ROWS).all()
            for row in row_elements:
                cells = [cell.text_content().strip() for cell in row.locator("td").all()]
                if cells:
                    row_dict = dict(zip(headers, cells)) if headers else cells
                    rows_data.append(row_dict)
            logger.debug("Retrieved %s response table rows: %s", len(rows_data), rows_data)
        except Exception as e:
            logger.error("Failed to get response table rows: %s", e)
        return rows_data

    def get_response_table_first_row(self):
        """Returns the first row dictionary from response table."""
        rows = self.get_response_table_rows()
        return rows[0] if rows else {}

    def is_download_report_button_visible(self):
        """Checks if the Download Report button is visible on response view."""
        try:
            btn = self.page.locator(self.DOWNLOAD_REPORT_BTN)
            return btn.is_visible() and "Download Report" in btn.text_content()
        except Exception:
            return False

    def click_download_report_button(self):
        """Clicks Download Report button and returns download object."""
        logger.info("Clicking Download Report button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_REPORT_BTN).click()
        download = download_info.value
        logger.info("Downloaded report file: %s", download.suggested_filename)
        return download

    def is_pagination_visible(self, timeout=15000):
        """Checks if pagination container is visible."""
        try:
            self.is_response_table_visible(timeout=timeout)
            loc = self.page.locator("app-common-component-pagination, .pagination-container, .rows-per-page")
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error("Pagination container not visible within %s ms: %s", timeout, e)
            return False

    def get_selected_rows_per_page(self):
        """Gets current selected rows per page value from dropdown."""
        try:
            loc = self.page.locator("select#rowsSelect")
            loc.wait_for(state="visible", timeout=15000)
            val = loc.input_value()
            logger.debug("Current rows per page selected: %s", val)
            return val
        except Exception as e:
            logger.error("Failed to get rows per page: %s", e)
            return ""

    def select_rows_per_page(self, option_value):
        """Selects a value (e.g. '10', '25', '50', '100') in rows per page select."""
        logger.info("Selecting %s rows per page", option_value)
        loc = self.page.locator("select#rowsSelect")
        loc.wait_for(state="visible", timeout=15000)
        loc.select_option(str(option_value))

    def validate_response_table_pagination(self):
        """Validates pagination controls on response view table."""
        logger.info("Validating response table pagination")
        self.is_response_table_visible(timeout=15000)
        pagination = PaginationHelper(
            self.page,
            page_input="input.page-input",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            content_selector="table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Response table pagination validation result: %s", result)
        return result
