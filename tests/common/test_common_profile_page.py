from utils.logger import get_logger
from api.user_api import UserAPI
from config.config import EXPECTED_PERMISSION_COUNT

import pytest

logger = get_logger(__name__)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.critical
@pytest.mark.atcu
@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestProfilePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting profile page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Profile page test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Profile page test passed: %s", test_name)
        elif report.failed:
            logger.error("Profile page test failed: %s", test_name)
            logger.debug(
                "Profile page failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Profile page test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_login_data_for_validation(self, profile_page, report_case):
        """Test fetching login data using API client."""
        logger.info("Testing login data retrieval from ProfilePage")
        try:
            login_data = profile_page.get_login_data()
            logger.debug("Login data fetched from profile page: %s", login_data)
            report_case(
                expected="Login data with all required fields and 16 permissions",
                actual=str(login_data)
            , message="Validate Profile page login data for validation")

            # login data should not be none
            assert login_data is not None, "Login data should not be None"

            # login data should be a dict and contain expected keys
            assert isinstance(login_data, dict), "Login data should be a dictionary"

            # basic assertions on login data keys
            ## id should be int type and not empty
            assert isinstance(
                login_data.get("id"), int
            ), "Login data 'id' should be an integer"
            assert (
                login_data.get("id") != 0
            ), "Login data 'id' should not be empty or zero"
            assert "id" in login_data, "Login data should contain 'id'"

            ## full name should be string type and not empty
            assert isinstance(
                login_data.get("fullName"), str
            ), "Login data 'fullName' should be a string"
            assert login_data.get(
                "fullName"
            ), "Login data 'fullName' should not be empty"
            assert "fullName" in login_data, "Login data should contain 'fullName'"

            assert "leadName" in login_data, "Login data should contain 'leadName'"
            assert "roleType" in login_data, "Login data should contain 'roleType'"
            assert "userRole" in login_data, "Login data should contain 'userRole'"
            assert (
                "userPermission" in login_data
            ), "Login data should contain 'permissions'"

            ## assert on permission obj count should match project config
            assert (
                len(login_data["userPermission"]) == EXPECTED_PERMISSION_COUNT
            ), f"Permissions should contain {EXPECTED_PERMISSION_COUNT} items"

            # assert on if roletyp is super admin then user have all permission with view, create, update, delete and count should be 16
            if login_data.get("roleType") == "SUPER_ADMIN":
                permissions = login_data.get("userPermission", [])
                assert (
                    len(permissions) == EXPECTED_PERMISSION_COUNT
                ), f"SUPER_ADMIN should have {EXPECTED_PERMISSION_COUNT} permissions"
                for perm in permissions:
                    assert (
                        perm.get("view") is True
                    ), "SUPER_ADMIN should have view permission"
                    assert (
                        perm.get("create") is True
                    ), "SUPER_ADMIN should have create permission"
                    assert (
                        perm.get("update") is True
                    ), "SUPER_ADMIN should have update permission"
                    assert (
                        perm.get("delete") is True
                    ), "SUPER_ADMIN should have delete permission"

            logger.info("Login data retrieval test passed")
        except AssertionError as e:
            logger.error("Assertion error during login data test: %s", str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error during login data test: %s", str(e))
            raise

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_profile_page_validate_page_title(self, profile_page, report_case):
        """Test validating the profile page title."""
        logger.info("Testing profile page title validation")
        try:
            title = profile_page.get_page_title()
            logger.debug(
                "Page title check | expected=%s | actual=%s", "User Profile", title
            )
            report_case(expected="User Profile", actual=title, message="Validate Profile page validate page title")
            assert (
                title.strip() == "User Profile"
            ), f"Expected page title to be 'User Profile' but got '{title}'"

            logger.info("Profile page title validation test passed")
        except AssertionError as e:
            logger.error("Assertion error during profile page title test: %s", str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error during profile page title test: %s", str(e))
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_validate_component_title(self, profile_page, report_case):
        """Test validating the profile page component title."""
        logger.info("Testing profile page component title validation")
        try:
            component_title = profile_page.get_component_title()
            logger.debug(
                "Component title check | expected=%s | actual=%s",
                "User Details",
                component_title,
            )
            report_case(expected="User Details", actual=component_title, message="Validate Profile page validate component title")
            assert (
                component_title == "User Details"
            ), f"Expected component title to be 'User Details' but got '{component_title}'"
            logger.info("Profile page component title validation test passed")
        except AssertionError as e:
            logger.error(
                "Assertion error during profile page component title test: %s", str(e)
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during profile page component title test: %s", str(e)
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_validate_admin_and_role_input_fields_not_editable(
        self, profile_page, report_case
    ):
        """
        Test validating that input fields on the profile page
        are not editable.
        """

        logger.info("Testing profile page input fields non-editable validation")

        try:
            input_fields = profile_page.get_input_fields()
            readonly_fields_status = {}
            editable_fields_status = {}

            for field_name, field in input_fields.items():
                readonly = field.get_attribute("ng-reflect-readonly")

                if field_name in ["admin", "user_role"]:
                    is_readonly = readonly is not None
                    readonly_fields_status[field_name] = is_readonly
                    report_case(
                        expected=True,
                        actual=is_readonly,
                        message=f"Validate '{field_name}' field is readonly",
                    )
                    assert is_readonly, (
                        f"Expected input field '{field_name}' "
                        f"to be readonly but it is editable"
                    )

                    logger.info(
                        "Validated '%s' field is readonly",
                        field_name,
                    )

                else:
                    is_editable = readonly is None
                    editable_fields_status[field_name] = is_editable
                    report_case(
                        expected=True,
                        actual=is_editable,
                        message=f"Validate '{field_name}' field is editable",
                    )
                    assert is_editable, (
                        f"Expected input field '{field_name}' "
                        f"to be editable but it is readonly"
                    )

                    logger.info(
                        "Validated '%s' field is editable",
                        field_name,
                    )

            logger.debug(
                "Input fields status | readonly_fields=%s | editable_fields=%s",
                readonly_fields_status,
                editable_fields_status,
            )
            report_case(
                expected="admin and user_role readonly; others editable",
                actual=f"readonly_fields={readonly_fields_status}, editable_fields={editable_fields_status}"
            , message="Validate Profile page validate admin and role input fields not editable")
            logger.info("Profile page input fields non-editable validation test passed")

        except AssertionError as e:
            logger.error(
                "Assertion error during profile page input fields test: %s",
                str(e),
            )
            raise

        except Exception as e:
            logger.error(
                "Unexpected error during profile page input fields test: %s",
                str(e),
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_validate_input_fields_values_with_actual_data(
        self, profile_page, report_case
    ):
        """
        Test validating that input fields on the profile page
        have correct values matching the actual data from API.
        """

        user_api = UserAPI()

        logger.info("Testing profile page input fields values validation")

        try:
            # Fetch user data from API
            user_data = user_api.get_user_data_by_id(profile_page.page)
            logger.debug("Fetched user data from API: %s", user_data)

            # Get input fields from profile page
            input_fields = profile_page.get_input_fields()

            # Log field values before assertions
            role_type = (user_data.get("roleType") or "").upper()
            user_role = (user_data.get("userRole") or "").upper()
            admin_name_value = user_data.get("adminName")
            expected_admin_name = (
                "--"
                if (
                    role_type in {"SUPER_ADMIN", "ADMIN"}
                    or user_role in {"ADMIN", "SUPER_ADMIN"}
                    or not admin_name_value
                )
                else admin_name_value
            )
            field_values_comparison = {
                "admin": {
                    "expected": expected_admin_name,
                    "actual": input_fields["admin"].input_value(),
                },
                "name": {
                    "expected": user_data.get("firstName"),
                    "actual": input_fields["name"].input_value(),
                },
                "surname": {
                    "expected": user_data.get("lastName"),
                    "actual": input_fields["surname"].input_value(),
                },
                "email": {
                    "expected": user_data.get("userEmail"),
                    "actual": input_fields["email"].input_value(),
                },
            }
            logger.debug("Field values comparison: %s", field_values_comparison)
            report_case(expected=str(user_data), actual=str(field_values_comparison), message="Validate Profile page validate input fields values with actual data")

            # Validate each input field value against API data
            admin_name_value = user_data.get("adminName")
            expected_admin_name = (
                "--"
                if (
                    role_type in {"SUPER_ADMIN", "ADMIN"}
                    or user_role in {"ADMIN", "SUPER_ADMIN"}
                    or not admin_name_value
                )
                else admin_name_value
            )

            assert (
                input_fields["admin"].input_value() == expected_admin_name
            ), f"Expected admin name to be '{expected_admin_name}' but got '{input_fields['admin'].input_value()}'"

            assert input_fields["name"].input_value() == user_data.get(
                "firstName"
            ), f"Expected first name to be '{user_data.get('firstName')}' but got '{input_fields['name'].input_value()}'"

            assert input_fields["surname"].input_value() == user_data.get(
                "lastName"
            ), f"Expected last name to be '{user_data.get('lastName')}' but got '{input_fields['surname'].input_value()}'"

            assert input_fields["email"].input_value() == user_data.get(
                "userEmail"
            ), f"Expected email to be '{user_data.get('userEmail')}' but got '{input_fields['email'].input_value()}'"

            assert int(input_fields["mobile"].input_value().strip()) == user_data.get(
                "mobileNumber"
            ), f"Expected mobile number to be '{user_data.get('mobileNumber')}' but got '{input_fields['mobile'].input_value()}'"

            assert input_fields["country"].input_value() == user_data.get(
                "country"
            ), f"Expected country to be '{user_data.get('country')}' but got '{input_fields['country'].input_value()}'"

            assert input_fields["state"].input_value() == user_data.get(
                "state"
            ), f"Expected state to be '{user_data.get('state')}' but got '{input_fields['state'].input_value()}'"

            assert input_fields["user_role"].input_value() == user_data.get(
                "roleName"
            ), f"Expected user role to be '{user_data.get('roleName')}' but got '{input_fields['user_role'].input_value()}'"

            assert input_fields[
                "image"
            ].is_visible(), "Expected profile image to be visible"
            assert input_fields["image"].get_attribute("src") == user_data.get(
                "image"
            ), f"Expected profile image src to be '{user_data.get('image')}' but got '{input_fields['image'].get_attribute('src')}'"

            logger.info("Profile page input fields values validation test passed")

        except AssertionError as e:
            logger.error(
                "Assertion error during profile page input fields values test: %s",
                str(e),
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during profile page input fields values test: %s",
                str(e),
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_validate_buttons_are_visible_and_enabled(
        self, profile_page, report_case
    ):
        """
        Test validating that buttons on the profile page are visible and enabled.
        """

        logger.info("Testing profile page buttons visibility and enabled state")

        try:
            # Get buttons from profile page
            update_button = profile_page.page.locator("button:has-text('Update')")
            upload_profile_icon_button = profile_page.page.locator(
                "button:has-text('Upload Profile Icon')"
            )
            change_password_button = (
                profile_page.page.locator("div.image-section").locator("button").nth(1)
            )

            # Check button states
            update_visible = update_button.is_visible()
            update_enabled = update_button.is_enabled()
            upload_visible = upload_profile_icon_button.is_visible()
            upload_enabled = upload_profile_icon_button.is_enabled()
            change_pwd_visible = change_password_button.is_visible()
            change_pwd_enabled = change_password_button.is_enabled()

            expected_status = "Update(visible,enabled), Upload Profile Icon(visible,enabled), Change Password(visible,enabled)"
            actual_status = f"Update({update_visible},{update_enabled}), Upload Profile Icon({upload_visible},{upload_enabled}), Change Password({change_pwd_visible},{change_pwd_enabled})"
            logger.debug(
                "Buttons status | expected=%s | actual=%s",
                expected_status,
                actual_status,
            )
            report_case(expected=expected_status, actual=actual_status, message="Validate Profile page validate buttons are visible and enabled")

            # Validate Save button is visible and enabled
            assert update_visible, "Expected 'Save' button to be visible"
            assert update_enabled, "Expected 'Save' button to be enabled"

            # Validate Upload Profile Icon button is visible and enabled
            assert upload_visible, "Expected 'Upload Profile Icon' button to be visible"
            assert upload_enabled, "Expected 'Upload Profile Icon' button to be enabled"

            # Validate Change Password button is visible and enabled
            assert change_pwd_visible, "Expected 'Change Password' button to be visible"
            assert change_pwd_enabled, "Expected 'Change Password' button to be enabled"

            logger.info("Profile page buttons visibility and enabled state test passed")

        except AssertionError as e:
            logger.error("Assertion error during profile page buttons test: %s", str(e))
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during profile page buttons test: %s", str(e)
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_click_update_button_without_changes(
        self, profile_page, report_case
    ):
        """
        Test clicking the Update button on the profile page without making any changes.
        """

        logger.info("Testing clicking Update button without changes on profile page")

        try:
            # Get Update button from profile page
            update_button = profile_page.page.locator("button:has-text('Update')")

            # Click the Update button
            update_button.click()

            # Validate that a success message is displayed
            success_message = profile_page.page.locator(
                "simple-snack-bar:has-text('User Details Updated Successfully!!')"
            )
            message_text = success_message.text_content().strip()
            message_visible = success_message.is_visible()

            logger.debug(
                "Update message check | expected=%s | actual=%s | visible=%s",
                "User Details Updated Successfully!!",
                message_text,
                message_visible,
            )
            report_case(
                expected="User Details Updated Successfully!!", actual=message_text
            , message="Validate Profile page click update button without changes")

            assert "User Details Updated Successfully!!" in message_text, (
                f"Expected success message to contain "
                f"'User Details Updated Successfully!!' "
                f"but got '{message_text}'"
            )
            assert (
                success_message.is_visible()
            ), "Expected success message to be visible after clicking Update button"

            logger.info("Profile page Update button click without changes test passed")

        except AssertionError as e:
            logger.error(
                "Assertion error during profile page Update button test: %s", str(e)
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during profile page Update button test: %s", str(e)
            )
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_profile_page_update_state_and_validate_update_message(
        self, profile_page, report_case
    ):
        """
        Test updating the state field on the profile page and validating the update message.
        """

        logger.info(
            "Testing updating state field and validating update message on profile page"
        )

        try:
            # Get state input field from profile page
            state_input = profile_page.page.locator("input[formcontrolname='state']")

            # Update the state field value
            state_input.clear()
            new_state = "Maharashtra"
            state_input.fill(new_state)

            # Click the Update button
            update_button = profile_page.page.locator("button:has-text('Update')")
            update_button.click()

            # Validate that a success message is displayed
            success_message = profile_page.page.locator(
                "simple-snack-bar:has-text('User Details Updated Successfully!!')"
            )
            message_text = success_message.text_content().strip()
            message_visible = success_message.is_visible()

            logger.debug(
                "State update message check | expected=%s | actual=%s | new_state=%s | visible=%s",
                "User Details Updated Successfully!!",
                message_text,
                new_state,
                message_visible,
            )
            report_case(
                expected=f"State updated to {new_state}; User Details Updated Successfully!!",
                actual=message_text
            , message="Validate Profile page update state and validate update message")

            assert "User Details Updated Successfully!!" in message_text, (
                f"Expected success message to contain "
                f"'User Details Updated Successfully!!' "
                f"but got '{message_text}'"
            )
            assert (
                success_message.is_visible()
            ), "Expected success message to be visible after updating state field"

            logger.info("Profile page state field update and validation test passed")

        except AssertionError as e:
            logger.error(
                "Assertion error during profile page state update test: %s", str(e)
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during profile page state update test: %s", str(e)
            )
            raise
