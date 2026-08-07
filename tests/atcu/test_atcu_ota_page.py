from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestOtaPage:
    """Test suite for OTA Batch and OTA Master pages."""

    # Test data
    SEARCH_QUERY = "test"

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting OTA test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("OTA test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("OTA test passed: %s", test_name)
        elif report.failed:
            logger.error("OTA test failed: %s", test_name)
            logger.debug("OTA failure details for %s: %s", test_name, report.longrepr)
        elif report.skipped:
            logger.warning("OTA test skipped: %s", test_name)