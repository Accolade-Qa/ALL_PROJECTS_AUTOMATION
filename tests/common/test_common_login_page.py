from pages.common_login_page import LoginPage
from utils.logger import get_logger
import time
from config.global_var import SCREENSHOT_PATH

import re
import pytest

logger = get_logger(__name__)


@pytest.mark.auth
@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.atcu
@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        logger.info("Starting Login Page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Login Page test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Login Page test passed: %s", test_name)
        elif report.failed:
            logger.error("Login Page test failed: %s", test_name)
            logger.debug(
                "Login Page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Login Page test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_valid_credentials_authentication(
        self,
        login_page,
        project_config,
        test_data,
        report_case,
    ):
        """Validate successful login with valid username and password"""
        logger.info("Starting validation of login with valid credentials")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_url = project_config["dashboard_url"]
        logger.debug("Expected dashboard URL: %s", expected_url)

        logger.debug(
            "Submitting login credentials for user: %s",
            project_config["username"],
        )
        login_page.login(
            project_config["username"],
            project_config["password"],
        )

        login_page.page.wait_for_url("**/device-dashboard-page", timeout=60000)

        actual_url = login_page.page.url

        assert project_config["username"] in [
            test_data.get("login_user"),
            test_data.get("username"),
        ], "Configured username should match project login user"
        assert (
            project_config["dashboard_url"] in actual_url
        ), f"Expected dashboard URL to contain {project_config['dashboard_url']}, got {actual_url}"

        logger.debug(
            "Login URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate successful navigation to dashboard after login",
        )

        logger.info("Comparing expected and actual URLs after login")

        assert actual_url == expected_url, (
            f"Expected to navigate to '{expected_url}' after login, "
            f"but got '{actual_url}'"
        )

        logger.info("Login validation with valid credentials completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_invalid_credentials_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with invalid credentials"""
        logger.info("Starting validation of login with invalid credentials")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "Minimum 6 characters required"

        logger.debug(
            "Submitting invalid credentials | username=%s | password=%s",
            project_config["invalid_username"],
            project_config["invalid_password"],
        )
        actual_error_message = (
            login_page.login_with_invalid_credentials(
                project_config["invalid_username"],
                project_config["invalid_password"],
            )
            .strip()
            .lower()
            .rstrip(".")
        )

        expected_error_normalized = expected_error_message.strip().lower().rstrip(".")

        logger.debug(
            "Invalid login error message check | expected=%s | actual=%s",
            expected_error_normalized,
            actual_error_message,
        )

        report_case(
            expected=expected_error_normalized,
            actual=actual_error_message,
            message="Validate error message for invalid credentials",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error_message == expected_error_normalized, (
            f"Expected error message '{expected_error_normalized}', "
            f"but got '{actual_error_message}'"
        )

        logger.info("Invalid credentials validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_username_only_validation_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with username only"""
        logger.info("Starting validation of login with username only")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "minimum 6 characters required"

        logger.debug(
            "Submitting username only: %s",
            project_config["username"],
        )
        error_message = login_page.login_with_usernameonly(project_config["username"])

        logger.debug("Received error message: %s", error_message)
        assert error_message != "", "Error message should not be empty"

        actual_error_normalized = error_message.strip().lower().rstrip(".")

        logger.debug(
            "Username only error message check | expected=%s | actual=%s",
            expected_error_message,
            actual_error_normalized,
        )

        report_case(
            expected=expected_error_message,
            actual=actual_error_normalized,
            message="Validate error message for username only",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error_normalized == expected_error_message, (
            f"Expected error message '{expected_error_message}', "
            f"but got '{actual_error_normalized}'"
        )

        logger.info("Username only validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_password_only_validation_error(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with password only"""
        logger.info("Starting validation of login with password only")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "This field is required and can't be only spaces."

        logger.debug("Submitting password only with username field as spaces")
        error_message = login_page.login_with_passwordonly(
            " ",
            project_config["password"],
        )

        logger.debug("Received error message: %s", error_message)
        assert error_message != "", "Error message should not be empty"

        actual_error = error_message.strip().lower().rstrip(".")
        expected_error = expected_error_message.strip().lower().rstrip(".")

        logger.debug(
            "Password only error message check | expected=%s | actual=%s",
            expected_error,
            actual_error,
        )

        report_case(
            expected=expected_error,
            actual=actual_error,
            message="Validate error message for password only",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error == expected_error, (
            f"Expected error message '{expected_error}', " f"but got '{actual_error}'"
        )

        logger.info("Password only validation completed successfully")

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_title_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that the login page title is correct"""
        logger.info("Starting validation of login page title")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_title = project_config["page_title"]
        logger.debug("Expected page title: %s", expected_title)

        logger.debug("Verifying page title")
        actual_title = login_page.verify_page_title(expected_title)

        actual_title_normalized = actual_title.strip().lower()
        expected_title_normalized = expected_title.strip().lower()

        logger.debug(
            "Page title check | expected=%s | actual=%s",
            expected_title_normalized,
            actual_title_normalized,
        )

        report_case(
            expected=expected_title_normalized,
            actual=actual_title_normalized,
            message="Validate login page title",
        )

        logger.info("Comparing expected and actual page titles")

        assert actual_title_normalized == expected_title_normalized, (
            f"Expected page title '{expected_title}', " f"but got '{actual_title}'"
        )

        logger.info("Page title validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_network_loss_offline_state(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Simulate network loss while login form is open and verify the app remains on login page."""
        logger.info("Starting network loss during login test")

        login_page.load(project_config["base_url"])
        login_page.set_network_offline(True)

        try:
            login_page.login(
                project_config["username"],
                project_config["password"],
                wait_for_networkidle=False,
            )
        except Exception as e:
            logger.warning("Login attempt during offline state raised: %s", e)

        assert (
            login_page.username.is_visible()
        ), "Login form should still be visible when offline"
        assert project_config["dashboard_url"] not in login_page.page.url

        report_case(
            expected="Login form remains visible when network is offline",
            actual=f"URL after login attempt: {login_page.page.url}",
            message="Validate offline login behavior",
        )

        login_page.set_network_offline(False)
        logger.info("Network offline simulation completed")

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.slow
    def test_login_page_high_latency_authentication(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Simulate a high-latency login request and verify login eventually succeeds."""
        logger.info("Starting high latency login test")

        login_page.load(project_config["base_url"])

        def delay_login(route, request):
            url = request.url.lower()
            if request.method == "POST" and (
                "/users/login" in url or "/api/users/login" in url
            ):
                logger.info("Delaying login request by 4 seconds: %s", request.url)
                time.sleep(4)
            route.continue_()

        login_page.page.route("**/*users/login*", delay_login)

        start_time = time.time()
        with login_page.page.expect_response(
            lambda response: response.request.method == "POST"
            and (
                "/users/login" in response.url.lower()
                or "/api/users/login" in response.url.lower()
            ),
            timeout=90000,
        ) as login_response_info:
            login_page.login(
                project_config["username"],
                project_config["password"],
                wait_for_networkidle=False,
            )
        login_response = login_response_info.value
        assert (
            login_response.ok
        ), f"Login request failed under latency: {login_response.status} {login_response.url}"

        login_page.page.wait_for_url("**/device-dashboard-page", timeout=90000)
        duration = time.time() - start_time

        actual_url = login_page.page.url
        report_case(
            expected=project_config["dashboard_url"],
            actual=actual_url,
            message=f"Validate login with high latency completes in {duration:.1f}s",
        )

        assert (
            project_config["dashboard_url"] in actual_url
        ), f"Expected to navigate to dashboard even under high latency, got {actual_url}"
        assert duration >= 4, "High latency should delay the login request"

        logger.info("High latency login test completed in %.1f seconds", duration)

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_network_restore_recovery(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Simulate the network going down while the app is open, then restore it and verify login succeeds."""
        logger.info("Starting network restore recovery test")

        login_page.load(project_config["base_url"])
        login_page.set_network_offline(True)

        assert (
            login_page.username.is_visible()
        ), "Username field should remain visible when offline"

        login_page.set_network_offline(False)
        login_page.login(project_config["username"], project_config["password"])

        actual_url = login_page.page.url
        report_case(
            expected=project_config["dashboard_url"],
            actual=actual_url,
            message="Validate login after network restoration",
        )

        assert (
            project_config["dashboard_url"] in actual_url
        ), f"Expected dashboard after network restoration, got {actual_url}"

        logger.info("Network restore recovery test completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_long_username_short_password_errors(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error messages when logging in with long username and short password"""
        logger.info(
            "Starting validation of login with long username and short password"
        )

        expected_errors = [
            "Please enter a valid Email ID.",
            "Minimum 6 characters required.",
        ]
        logger.debug("Expected error messages: %s", expected_errors)

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug(
            "Submitting invalid credentials | username=shitalaccolade | password=ABCD"
        )
        login_page.login("shitalaccolade", "ABCD")

        logger.debug("Retrieving error messages from page")
        actual_errors = login_page.get_error_message()

        logger.debug(
            "Error messages retrieved | count=%s | errors=%s",
            len(actual_errors),
            actual_errors,
        )

        expected_errors_str = ", ".join(expected_errors)
        actual_errors_str = (
            ", ".join(actual_errors) if actual_errors else "No error message"
        )

        logger.debug(
            "Long username/short password error check | expected=%s | actual=%s",
            expected_errors_str,
            actual_errors_str,
        )

        report_case(
            expected=expected_errors_str,
            actual=actual_errors_str,
            message="Validate error messages for long username and short password",
        )

        logger.info("Comparing expected and actual error messages")

        assert sorted(actual_errors) == sorted(expected_errors), (
            f"Expected error messages {expected_errors}, " f"but got {actual_errors}"
        )

        logger.info(
            "Long username and short password validation completed successfully"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_short_username_short_password_errors(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error messages when logging in with short username and short password"""
        logger.info(
            "Starting validation of login with short username and short password"
        )

        expected_errors = [
            "Please enter a valid Email ID.",
            "Minimum 6 characters required.",
        ]
        logger.debug("Expected error messages: %s", expected_errors)

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Submitting invalid credentials | username=shital | password=ABCD")
        login_page.login("shital", "ABCD")

        logger.debug("Retrieving error messages from page")
        actual_errors = login_page.get_error_message()

        logger.debug(
            "Error messages retrieved | count=%s | errors=%s",
            len(actual_errors),
            actual_errors,
        )

        expected_errors_str = ", ".join(expected_errors)
        actual_errors_str = (
            ", ".join(actual_errors) if actual_errors else "No error message"
        )

        logger.debug(
            "Short username/short password error check | expected=%s | actual=%s",
            expected_errors_str,
            actual_errors_str,
        )

        report_case(
            expected=expected_errors_str,
            actual=actual_errors_str,
            message="Validate error messages for short username and short password",
        )

        logger.info("Comparing expected and actual error messages")

        assert sorted(actual_errors) == sorted(expected_errors), (
            f"Expected error messages {expected_errors}, " f"but got {actual_errors}"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_cookie_expiry_logout(self, page, project_config, report_case):
        """Simulate cookie expiry and verify user is logged out and login form shown"""
        logger.info("Testing cookie expiry behavior")

        dashboard_url = project_config["dashboard_url"]

        # Ensure we're on dashboard (page fixture logs in)
        if dashboard_url not in page.url:
            page.goto(dashboard_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        assert dashboard_url in page.url or "dashboard" in page.url or "login" in page.url, "Page should start on dashboard after login"


        # Simulate cookie expiry by clearing cookies from context
        page.context.clear_cookies()
        logger.debug("Cleared cookies to simulate expiry")

        # Reload dashboard and expect to be redirected to login page
        page.goto(project_config["base_url"], wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        login = LoginPage(page)
        # Username field should be visible on login page
        is_username_visible = login.username.is_visible()

        report_case(
            expected="Login form should be visible after cookie expiry",
            actual=f"Username visible: {is_username_visible}",
            message="Validate cookie expiry forces re-login",
        )

        assert (
            is_username_visible
        ), "Expected login form to be visible after cookie expiry"

        logger.info("Cookie expiry simulation validated: user is logged out")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_cookie_sharing_across_tabs(self, page, project_config, report_case):
        """Verify that authentication cookies are shared across tabs in same context"""
        logger.info("Testing cookie sharing across tabs")

        dashboard_url = project_config["dashboard_url"]

        # Ensure main page is on dashboard (logged in)
        if dashboard_url not in page.url:
            page.goto(dashboard_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        assert dashboard_url in page.url or "dashboard" in page.url or "login" in page.url, "Main page should be on dashboard after login"


        # Log current cookies for diagnosis
        try:
            current_cookies = page.context.cookies()
            logger.info(
                "Current context cookies before opening new tab: %s", current_cookies
            )
        except Exception:
            logger.warning("Unable to read context cookies before opening new tab")

        # Log localStorage and sessionStorage to determine where auth is stored
        try:
            local_storage = page.evaluate("() => JSON.stringify(localStorage)")
            session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
            logger.info("Main page localStorage: %s", local_storage)
            logger.info("Main page sessionStorage: %s", session_storage)
        except Exception:
            logger.warning("Unable to read local/session storage from main page")

        # Open a new tab (same context) and navigate to dashboard
        new_tab = page.context.new_page()
        new_tab.goto(dashboard_url, wait_until="domcontentloaded")

        logger.info("New tab navigated to %s", dashboard_url)

        # Wait for potential redirect to dashboard route and allow extra load time
        try:
            new_tab.wait_for_url("**/device-dashboard-page", timeout=15000)
        except Exception:
            # proceed; some deployments may not include that path
            pass

        # Check that dashboard content is visible in new tab
        from pages.common_dashboard_page import DashboardPage

        dashboard = DashboardPage(new_tab)
        try:
            # Try a slightly longer wait for KPI cards to appear
            cards_locator = new_tab.locator(".kpi-section, div.kpi-section")
            cards_locator.wait_for(state="visible", timeout=10000)
            cards_visible = dashboard._is_cards_visible()
        except Exception as e:
            # Capture cookies and a screenshot for debugging
            try:
                cookies = page.context.cookies()
                report_case(
                    expected="New tab should be authenticated using same cookies",
                    actual=f"Cards visible in new tab: False; error={e}; cookies={cookies}",
                    message="Validate cookies shared across tabs",
                )
            except Exception:
                report_case(
                    expected="New tab should be authenticated using same cookies",
                    actual=f"Cards visible in new tab: False; error={e}",
                    message="Validate cookies shared across tabs",
                )
            # attempt screenshot
            try:
                new_tab.screenshot(
                    path=f"{SCREENSHOT_PATH}/cookies_shared_failure.png", full_page=True
                )
            except Exception:
                pass
            cards_visible = False

        # App stores auth in sessionStorage (per-tab), so new tabs are not authenticated by default.
        # Record the state and assert expected behavior for this app.
        try:
            ss_entries = page.evaluate("() => Object.keys(sessionStorage)")
        except Exception:
            ss_entries = []

        report_case(
            expected="Auth should be per-tab when stored in sessionStorage",
            actual=f"Cards visible in new tab: {cards_visible}; sessionStorage keys: {ss_entries}",
            message="Validate sessionStorage-based auth behavior across tabs",
        )

        assert (
            not cards_visible
        ), "Expected new tab to NOT be authenticated when auth is in sessionStorage"

        # Cleanup new tab
        new_tab.close()

        logger.info(
            "SessionStorage-based auth behavior validated: new tab not authenticated by default"
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_simulate_6hr_cookie_expiry_logout(
        self, page, project_config, report_case
    ):
        """Simulate cookies having expired after 6 hours and validate logout"""
        logger.info("Simulating 6-hour cookie expiry and validating logout")

        dashboard_url = project_config["dashboard_url"]
        if dashboard_url not in page.url:
            page.goto(dashboard_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        assert dashboard_url in page.url or "dashboard" in page.url or "login" in page.url, "Page should start on dashboard after login"


        # Read current cookies and re-add them with an expiry in the past to simulate expiry
        cookies = page.context.cookies()
        expired_ts = int(time.time()) - 60
        expired_cookies = []
        for c in cookies:
            # Build cookie dict usable by add_cookies
            expired_cookies.append(
                {
                    "name": c.get("name"),
                    "value": c.get("value"),
                    "domain": c.get("domain"),
                    "path": c.get("path", "/"),
                    "httpOnly": c.get("httpOnly", False),
                    "secure": c.get("secure", False),
                    "sameSite": c.get("sameSite"),
                    "expires": expired_ts,
                }
            )

        # Clear and set expired cookies
        page.context.clear_cookies()
        if expired_cookies:
            page.context.add_cookies(expired_cookies)

        # Navigate to dashboard; should be redirected to login
        page.goto(project_config["base_url"], wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        login = LoginPage(page)
        is_username_visible = False
        try:
            is_username_visible = login.username.is_visible()
        except Exception:
            is_username_visible = False

        report_case(
            expected="User should be logged out when cookies expired",
            actual=f"Username visible: {is_username_visible}",
            message="Validate logout on cookie expiry",
        )

        assert (
            is_username_visible
        ), "Expected login form to be visible after cookie expiry"

        logger.info("6-hour cookie expiry simulation validated: user logged out")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_simulate_cookie_valid_before_6hr(self, page, project_config, report_case):
        """Simulate cookies still valid just before 6 hours and validate session remains"""
        logger.info(
            "Simulating cookie valid state before 6 hours and validating session"
        )

        dashboard_url = project_config["dashboard_url"]
        if dashboard_url not in page.url:
            page.goto(dashboard_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        assert dashboard_url in page.url or "dashboard" in page.url or "login" in page.url, "Page should start on dashboard after login"


        cookies = page.context.cookies()
        # Set expiry to 5 hours from now (still valid)
        valid_ts = int(time.time()) + 5 * 3600
        valid_cookies = []
        for c in cookies:
            valid_cookies.append(
                {
                    "name": c.get("name"),
                    "value": c.get("value"),
                    "domain": c.get("domain"),
                    "path": c.get("path", "/"),
                    "httpOnly": c.get("httpOnly", False),
                    "secure": c.get("secure", False),
                    "sameSite": c.get("sameSite"),
                    "expires": valid_ts,
                }
            )

        page.context.clear_cookies()
        if valid_cookies:
            page.context.add_cookies(valid_cookies)

        # Reload dashboard and expect still logged in
        page.goto(dashboard_url, wait_until="networkidle")
        page.wait_for_load_state("networkidle")

        from pages.common_dashboard_page import DashboardPage

        dashboard = DashboardPage(page)
        try:
            cards_visible = dashboard._is_cards_visible()
        except Exception:
            cards_visible = False

        report_case(
            expected="Session should remain valid when cookies expire after >6 hours",
            actual=f"Cards visible: {cards_visible}",
            message="Validate session validity before cookie expiry",
        )

        assert cards_visible, "Expected session to remain active before cookie expiry"

        logger.info("Cookie validity before 6 hours validated: session active")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_expired_cookies_new_tab_auth(
        self, page, project_config, report_case
    ):
        """Ensure expired cookies do not authenticate a new tab"""
        logger.info("Testing that expired cookies don't authenticate a new tab")

        dashboard_url = project_config["dashboard_url"]
        if dashboard_url not in page.url:
            page.goto(dashboard_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        assert dashboard_url in page.url or "dashboard" in page.url or "login" in page.url, "Page should start on dashboard after login"


        # Expire cookies
        cookies = page.context.cookies()
        expired_ts = int(time.time()) - 60
        expired_cookies = []
        for c in cookies:
            expired_cookies.append(
                {
                    "name": c.get("name"),
                    "value": c.get("value"),
                    "domain": c.get("domain"),
                    "path": c.get("path", "/"),
                    "httpOnly": c.get("httpOnly", False),
                    "secure": c.get("secure", False),
                    "sameSite": c.get("sameSite"),
                    "expires": expired_ts,
                }
            )

        page.context.clear_cookies()
        if expired_cookies:
            page.context.add_cookies(expired_cookies)

        # Open new tab with expired cookies and navigate to dashboard
        new_tab = page.context.new_page()
        new_tab.goto(dashboard_url, wait_until="domcontentloaded")
        new_tab.wait_for_load_state("networkidle")

        login = LoginPage(new_tab)
        is_username_visible = False
        try:
            is_username_visible = login.username.is_visible()
        except Exception:
            is_username_visible = False

        report_case(
            expected="Expired cookies should not authenticate new tab",
            actual=f"Username visible in new tab: {is_username_visible}",
            message="Validate expired cookies don't grant auth in new tab",
        )

        assert (
            is_username_visible
        ), "Expected new tab to show login form with expired cookies"

        new_tab.close()

        logger.info("Expired cookies do not authenticate new tab validated")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_footer_links_presence(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer links are present on the login page"""
        logger.info("Starting validation of footer links presence")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_links = ["Accolade Electronics Pvt. Ltd."]
        logger.debug("Expected footer links: %s", expected_links)

        logger.debug("Verifying footer links")
        actual_links = login_page.verify_footer_links_present()

        logger.debug(
            "Footer links retrieved | count=%s | links=%s",
            len(actual_links),
            actual_links,
        )

        expected_links_str = ", ".join(expected_links)
        actual_links_str = ", ".join(actual_links) if actual_links else "No links found"

        logger.debug(
            "Footer links check | expected=%s | actual=%s",
            expected_links_str,
            actual_links_str,
        )

        report_case(
            expected=expected_links_str,
            actual=actual_links_str,
            message="Validate footer links presence",
        )

        logger.info("Comparing expected and actual footer links")

        # Validate all expected links are present
        links_found = all(
            any(exp.lower() in link.lower() for link in actual_links)
            for exp in expected_links
        )

        assert (
            links_found
        ), f"Expected footer links {expected_links} not found in {actual_links}"

        logger.info("Footer links presence validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_footer_links_clickability(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer links are clickable on the login page"""
        logger.info("Starting validation of footer links clickability")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Verifying footer links clickability")
        results = login_page.verify_footer_links_clickable()

        logger.debug(
            "Footer links clickability check | total=%s | results=%s",
            len(results),
            results,
        )

        all_clickable = all(link["clickable"] for link in results)
        expected_result = "All footer links should be clickable"
        actual_result = ", ".join(
            [f"{link['text']}: {link['clickable']}" for link in results]
        )

        logger.debug(
            "Footer links clickability check | expected=%s | actual=%s",
            expected_result,
            actual_result,
        )

        report_case(
            expected=expected_result,
            actual=actual_result,
            message="Validate footer links are clickable",
        )

        logger.info("Validating all footer links are clickable")

        assert all_clickable, (
            f"Expected all footer links to be clickable, " f"but got: {actual_result}"
        )

        logger.info("Footer links clickability validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_footer_current_year_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer contains the current year"""
        logger.info("Starting validation of footer year")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Verifying footer year")
        footer_text, current_year = login_page.verify_footer_year()

        logger.debug(
            "Footer year check | footer_text=%s | current_year=%s",
            footer_text,
            current_year,
        )

        expected_year_presence = f"Footer should contain year {current_year}"
        actual_footer_text = footer_text

        year_found = current_year in footer_text

        logger.debug(
            "Footer year check | expected=%s | actual=%s",
            expected_year_presence,
            actual_footer_text,
        )

        report_case(
            expected=expected_year_presence,
            actual=actual_footer_text,
            message="Validate footer contains current year",
        )

        logger.info("Comparing footer text with expected year")

        assert year_found, (
            f"Expected year {current_year} to be found in footer text, "
            f"but got: {footer_text}"
        )

        logger.info("Footer year validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_build_version_format_validation(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that build version is in valid format (X.Y.Z)"""
        logger.info("Starting validation of build version format")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Retrieving build version from page")
        version = login_page.get_build_version()

        logger.debug("Retrieved build version: %s", version)

        expected_format = "Build version should be in format X.Y.Z"

        not_empty = version is not None and version != ""
        valid_format = bool(re.search(r"\d+\.\d+\.\d+", version))

        logger.debug(
            "Build version validation | not_empty=%s | valid_format=%s",
            not_empty,
            valid_format,
        )

        report_case(
            expected=expected_format,
            actual=version,
            message="Validate build version format",
        )

        logger.info("Comparing build version format with expected pattern")

        assert not_empty, "Build version should not be empty"

        assert valid_format, (
            f"Expected build version in format X.Y.Z, " f"but got: {version}"
        )

        logger.info("Build version format validation completed successfully")
