from utils.logger import get_logger
from utils.helpers import Helpers
from .endpoints import GET_CUSTOMERS, SAVE_CUSTOMER

logger = get_logger(__name__)


class CustomerAPI:
    """Customer API methods for Dispatched Device / Customer Master pages."""

    def __init__(self, client=None):
        self._client = client

    def get_customer_list(self=None, *args, **kwargs):
        """Fetch all customer names from API.

        Usage:
            api = APIClient()
            customers = api.customer.get_customer_list()
        """
        if not isinstance(self, CustomerAPI):
            from .api_client import APIClient
            return APIClient.get_default().customer.get_customer_list(*args, **kwargs)

        logger.info("Fetching customer list from API")
        response = self._client.get(GET_CUSTOMERS)
        customers = response.get("data", [])
        return [
            c["customerName"].strip()
            for c in customers
            if isinstance(c, dict) and c.get("customerName")
        ]

    def save_customer(self=None, customer_name=None, *args, **kwargs):
        """Create and save a new customer via API.

        Usage:
            api = APIClient()
            res, name = api.customer.save_customer()
        """
        if not isinstance(self, CustomerAPI):
            from .api_client import APIClient
            return APIClient.get_default().customer.save_customer(customer_name, *args, **kwargs)

        if not customer_name or hasattr(customer_name, "request"):
            customer_name = "API cust " + Helpers.generate_random_string(5)

        logger.info("Saving customer via API: %s", customer_name)
        payload = {"id": 0, "customerName": customer_name}
        response = self._client.post(SAVE_CUSTOMER, json=payload)
        return response, customer_name
