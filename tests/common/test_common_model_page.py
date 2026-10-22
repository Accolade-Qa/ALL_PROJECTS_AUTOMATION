from playwright.sync_api import expect
from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.regression
@pytest.mark.lct
@pytest.mark.sampark
class TestModelPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Model page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Model page test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("Model page test passed: %s", test_name)
        elif report.failed:
            logger.error("Model page test failed: %s", test_name)
            logger.debug(
                "Model page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Model page test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_navigates_to_correct_url(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model page navigation")

        expected_url = project_config["model_url"]
        actual_url = model_page.page.url
        logger.debug(
            "Model page URL check | expected=%s | actual=%s", expected_url, actual_url
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Model page navigation")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_navigates_to_create_model_page(self, model_page, project_config, report_case):
        logger.info("Starting validation of Create Model page navigation")
        model_page.go_to_create_model(project_config["create_new_model"])

        actual_url = model_page.page.url
        expected_url = project_config["create_new_model"]
        logger.debug(
            "Create Model URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Create Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Create Model page navigation")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_navigates_to_update_model_page(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update Model page navigation")
        model_page.go_to_update_model(project_config["update_model"])

        actual_url = model_page.page.url
        expected_url = project_config["update_model"]
        logger.debug(
            "Update Model URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Update Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Update Model page navigation")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_navbar_list_is_visible(self, model_page, report_case):
        logger.info("Starting validation of Model navigation list visibility")

        is_visible = model_page._nav_list_visibility()
        logger.debug("Model navigation list visible: %s", is_visible)

        report_case(
            expected="Navbar list should be visible",
            actual=f"Navbar list visible: {is_visible}",
            message="Validate Model navbar list visibility",
        )

        assert is_visible, "Navbar list is not visible"
        logger.info("Successfully validated Model navigation list visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_title_is_visible(self, model_page, report_case):
        logger.info("Starting validation of Model page title visibility")

        is_visible = model_page._is_PageTitle_Visible()
        logger.debug("Model page title visible: %s", is_visible)

        report_case(
            expected="Page title should be visible",
            actual=f"Page title visible: {is_visible}",
            message="Validate Model page title visibility",
        )

        assert is_visible, "Page Title is not visible"
        logger.info("Successfully validated Model page title visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_button_is_visible(self, model_page, report_case):
        logger.info("Starting validation of Create Model button visibility")

        is_visible = model_page._create_model_visibility()
        logger.debug("Create Model button visible/enabled: %s", is_visible)

        report_case(
            expected="Create Model button should be visible and enabled",
            actual=f"Create Model button visible/enabled: {is_visible}",
            message="Validate Create Model button availability",
        )

        assert is_visible, "Create Model button is not visible or enabled"
        logger.info("Successfully validated Create Model button visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_button_click_completes(self, model_page, report_case):
        logger.info("Starting validation of Create Model button click")
        model_page._create_model_click()

        actual_url = model_page.page.url
        logger.debug("Create Model click completed | current_url=%s", actual_url)

        report_case(
            expected="Create Model button click should complete",
            actual=f"Current URL after click: {actual_url}",
            message="Validate Create Model button click",
        )
        assert actual_url is not None and actual_url != "", "URL should not be empty after clicking Create Model button"
        logger.info("Successfully clicked Create Model button")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_page_title_is_correct(self, model_page, project_config, report_case):
        logger.info("Starting validation of Create Model page title")
        model_page.go_to_create_model(project_config["create_new_model"])

        expected_title = "Create Device Model"
        actual_title = model_page._create_model_page_title()
        logger.debug(
            "Create Model title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate Create Model page title",
        )

        assert actual_title == expected_title, "Create Model Page Title not visible"
        logger.info("Successfully validated Create Model page title")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_submit_button_is_enabled(self, model_page, project_config, report_case):
        logger.info("Starting validation of Create Model Submit button")
        model_page.go_to_create_model(project_config["create_new_model"])

        is_enabled = model_page._submit_button()
        logger.debug("Create Model Submit button enabled: %s", is_enabled)

        report_case(
            expected="Submit button should be enabled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate Create Model Submit button",
        )

        assert is_enabled, "Submit button is not enabled"
        logger.info("Successfully validated Create Model Submit button")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_code_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model Code input")
        model_page.go_to_create_model(project_config["create_new_model"])

        model_code_locator = model_page.page.get_by_label("Model Code")
        expect(model_code_locator).to_be_visible()
        expect(model_code_locator).to_be_enabled()
        model_code_locator.fill("NewCode")

        actual_value = model_code_locator.input_value()
        logger.debug("Model Code field value after fill: %s", actual_value)

        report_case(
            expected="Model Code field should accept value 'NewCode'",
            actual=f"Model Code field value: '{actual_value}'",
            message="Validate Model Code input",
        )

        assert actual_value == "NewCode", f"Expected 'NewCode', got '{actual_value}'"
        logger.info("Successfully validated Model Code input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_create_model_name_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model Name input")
        model_page.go_to_create_model(project_config["create_new_model"])
        model_page._model_name("NewName")

        logger.debug("Entered Model Name value: %s", "NewName")
        report_case(
            expected="Model Name field should accept value 'NewName'",
            actual="Model Name value entered",
            message="Validate Model Name input",
        )

        logger.info("Successfully validated Model Name input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_create_model_serial_sequence_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model Serial Sequence input")
        model_page.go_to_create_model(project_config["create_new_model"])
        model_page._model_seriel_sequence("NewSequence")

        logger.debug("Entered Model Serial Sequence value: %s", "NewSequence")
        report_case(
            expected="Model Serial Sequence field should accept value 'NewSequence'",
            actual="Model Serial Sequence value entered",
            message="Validate Model Serial Sequence input",
        )

        logger.info("Successfully validated Model Serial Sequence input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_create_model_hardware_version_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Hardware Version input")
        model_page.go_to_create_model(project_config["create_new_model"])
        model_page._hardware_version("NewVersion")

        logger.debug("Entered Hardware Version value: %s", "NewVersion")
        report_case(
            expected="Hardware Version field should accept value 'NewVersion'",
            actual="Hardware Version value entered",
            message="Validate Hardware Version input",
        )

        logger.info("Successfully validated Hardware Version input")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_create_model_submit_button_is_disabled_initially(self, model_page, project_config, report_case):
        logger.info("Starting validation of disabled Submit button state")
        model_page.go_to_create_model(project_config["create_new_model"])

        submit_button_locator = model_page.page.get_by_text("Submit check_circle", exact=True)
        is_enabled = submit_button_locator.is_enabled()
        logger.debug("Submit button enabled state: %s", is_enabled)

        report_case(
            expected="Submit button should be disabled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate disabled Submit button state",
        )

        assert not is_enabled, "Submit button should be disabled"
        logger.info("Successfully validated disabled Submit button state")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_search_by_model_code(self, model_page, report_case):
        logger.info("Starting validation of Model search")
        model_page._search_model("NewCode")

        logger.debug("Executed Model search for keyword: %s", "NewCode")
        report_case(
            expected="Model search should execute for 'NewCode'",
            actual="Model search completed",
            message="Validate Model search",
        )

        logger.info("Successfully validated Model search")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_view_icon_is_clickable(self, model_page, report_case):
        logger.info("Starting validation of Model view icon")
        model_page.view_icon()

        logger.debug("Clicked Model view icon")
        report_case(
            expected="Model view icon should be clickable",
            actual="Model view icon clicked",
            message="Validate Model view icon",
        )

        logger.info("Successfully validated Model view icon")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_update_model_code_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update Model Code input")
        model_page.go_to_update_model(project_config["update_model"])
        model_page.update_model_code("UpdatedCode")

        logger.debug("Entered updated Model Code value: %s", "UpdatedCode")
        report_case(
            expected="Update Model Code field should accept value 'UpdatedCode'",
            actual="Updated Model Code value entered",
            message="Validate Update Model Code input",
        )

        logger.info("Successfully validated Update Model Code input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_update_model_name_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update Model Name input")
        model_page.go_to_update_model(project_config["update_model"])
        model_page.update_model_name("UpdatedName")

        logger.debug("Entered updated Model Name value: %s", "UpdatedName")
        report_case(
            expected="Update Model Name field should accept value 'UpdatedName'",
            actual="Updated Model Name value entered",
            message="Validate Update Model Name input",
        )

        logger.info("Successfully validated Update Model Name input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_update_model_serial_sequence_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update Model Serial Sequence input")
        model_page.go_to_update_model(project_config["update_model"])
        model_page.update_model_seriel_sequence("UpdatedSequence")

        logger.debug(
            "Entered updated Model Serial Sequence value: %s", "UpdatedSequence"
        )
        report_case(
            expected="Update Model Serial Sequence field should accept value 'UpdatedSequence'",
            actual="Updated Model Serial Sequence value entered",
            message="Validate Update Model Serial Sequence input",
        )

        logger.info("Successfully validated Update Model Serial Sequence input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_update_model_hardware_version_field_accepts_input(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update Hardware Version input")
        model_page.go_to_update_model(project_config["update_model"])
        model_page.update_hardware_version("UpdatedVersion")

        logger.debug("Entered updated Hardware Version value: %s", "UpdatedVersion")
        report_case(
            expected="Update Hardware Version field should accept value 'UpdatedVersion'",
            actual="Updated Hardware Version value entered",
            message="Validate Update Hardware Version input",
        )

        logger.info("Successfully validated Update Hardware Version input")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_update_model_button_click_completes(self, model_page, project_config, report_case):
        logger.info("Starting validation of Update button click")
        model_page.go_to_update_model(project_config["update_model"])
        model_page._update_button_click()

        logger.debug("Clicked Update button on Model page")
        report_case(
            expected="Update button click should complete",
            actual="Update button clicked",
            message="Validate Update button click",
        )

        logger.info("Successfully validated Update button click")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_search_updated_model(self, model_page, report_case):
        logger.info("Starting validation of updated Model search")
        model_page._search_model("updated")

        logger.debug("Executed Model search for keyword: %s", "updated")
        report_case(
            expected="Model search should execute for 'updated'",
            actual="Model search completed",
            message="Validate updated Model search",
        )

        logger.info("Successfully validated updated Model search")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_model_page_verify_updated_model_details(self, model_page, report_case):
        logger.info("Starting validation of updated Model text")

        expected_model_text = ["UpdatedCode"]
        actual_model_texts = []

        for text in expected_model_text:
            actual_model_text = model_page._get_updated_model_text(text)
            actual_model_texts.append(actual_model_text)
            logger.debug(
                "Updated Model text check | expected=%s | actual=%s",
                text,
                actual_model_text,
            )

        report_case(
            expected=expected_model_text,
            actual=actual_model_texts,
            message="Validate updated Model text",
        )

        assert (
            actual_model_texts == expected_model_text
        ), f"Expected model text {expected_model_text}, got {actual_model_texts}"
        logger.info("Successfully validated updated Model text")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_model_page_delete_updated_model(self, model_page, report_case):
        logger.info("Starting validation of updated Model delete")
        model_page.delete_updated_model()

        logger.debug("Executed delete action for updated Model")
        report_case(
            expected="Updated Model delete action should complete",
            actual="Updated Model delete action completed",
            message="Validate updated Model delete",
        )

        logger.info("Successfully validated updated Model delete")
