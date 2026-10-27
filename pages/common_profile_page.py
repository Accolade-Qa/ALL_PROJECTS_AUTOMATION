from .common_base_page import BasePage
from api import APIClient
from utils.logger import get_logger
from config.config import PASSWORD, USERNAME

logger = get_logger(__name__)


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def get_login_data(self, api):
        """Fetch login data using APIClient."""
        logger.info("Fetching login data using APIClient")
        try:
            api = api or APIClient(
                username=USERNAME,
                password=PASSWORD,
            )
            login_data = api.login()
            logger.info("Successfully fetched login data")
            return login_data
        except Exception as e:
            logger.error("Failed to fetch login data: %s", str(e))
            raise

    def get_page_title(self):
        """Get the title of the profile page."""
        logger.info("Getting profile page title")
        try:
            title = super().get_title()
            logger.info("Profile page title retrieved: %s", title)
            return title
        except Exception as e:
            logger.error("Failed to get profile page title: %s", str(e))
            raise

    def get_component_title(self):
        """Get the title of the profile page component."""
        logger.info("Getting profile page component title")
        try:
            component_title = super().get_component_title()
            logger.info("Profile page component title retrieved: %s", component_title)
            return component_title
        except Exception as e:
            logger.error("Failed to get profile page component title: %s", str(e))
            raise

    def get_input_fields(self):
        """Get the input fields on the profile page."""

        logger.info("Getting input fields on the profile page")

        return {
            "admin": self.page.locator("input[formcontrolname='adminName']"),
            "name": self.page.locator("input[formcontrolname='firstName']"),
            "surname": self.page.locator("input[formcontrolname='lastName']"),
            "email": self.page.locator("input[formcontrolname='userEmail']"),
            "mobile": self.page.locator("input[formcontrolname='mobileNumber']"),
            "country": self.page.locator("input[formcontrolname='country']"),
            "state": self.page.locator("input[formcontrolname='state']"),
            "user_role": self.page.locator("input[formcontrolname='userRole']"),
            "image": self.page.locator("img[alt='Profile Picture']"),
        }
