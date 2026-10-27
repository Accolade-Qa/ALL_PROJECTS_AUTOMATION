from utils.helpers import Helpers
from utils.logger import get_logger
from datetime import datetime
from utils.helpers import Helpers
from pages.common_utils import TableSection, SearchHelper

import pytest

logger = get_logger(__name__)

class TestRoleGroupPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        if self.__class__.group is None:
            self.__class__.group = f"Test{Helpers.generate_random_string(4)}"

        test_name = request.node.name
        logger.info("Starting Role Group test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Role Group test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Role Group test passed: %s", test_name)
        elif report.failed:
            logger.error("Role Group test failed: %s", test_name)
            logger.debug(
                "Role Group failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Role Group test skipped: %s", test_name)

    """" Test for deleting role group from the role group page. """
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_role_group_page_delete_roles_api(self, api, report_case):
        """Test deleting a role permission."""
        logger.info("Testing delete role permission functionality")
        result = api.role_group.delete_atcu_role_groups()
        report_case(
            expected=True,
            actual=result.get("success"),
            message="Validate delete role groups via API in role group page",
        )
        assert result.get("success"), "Role group deletion API execution failed"
        logger.info("Delete role management test completed")