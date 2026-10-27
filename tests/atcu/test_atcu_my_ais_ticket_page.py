import pytest

from pages.atcu.atcu_my_ais_ticket_page import AtcuMyAisTicketPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.ticket
@pytest.mark.atcu
@pytest.mark.regression
class TestMyAisTicketPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Model page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Model page test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("ATCU Model page test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Model page test failed: %s", test_name)
            logger.debug(
                "ATCU Model page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Model page test skipped: %s", test_name)