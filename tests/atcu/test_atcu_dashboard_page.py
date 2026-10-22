from api import APIClient
from pages.common_base_page import BasePage
from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.dashboard
@pytest.mark.regression
@pytest.mark.usefixtures("project_config")
class TestDashboardPage:
    @pytest.fixture(autouse=True)
    def _inject_project_config(self, request, project_config):
        # Make `project_config` accessible as `self.project_config` inside test methods
        request.cls.project_config = project_config

    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dashboard test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Dashboard test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Dashboard test passed: %s", test_name)
        elif report.failed:
            logger.error("Dashboard test failed: %s", test_name)
            logger.debug(
                "Dashboard failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Dashboard test skipped: %s", test_name)
