"""API operations used by the customer master and dispatched-device pages."""

from utils.helpers import Helpers

from .api_service import APIService


GET_CUSTOMERS = "/customerMaster/getCustomers?page=1&size=100000&search="
SAVE_CUSTOMER = "/customerMaster/saveCustomer"


class CustomerAPI(APIService):
    def get_customer_list(self):
        response = self._client.get(GET_CUSTOMERS)
        return [
            customer["customerName"].strip()
            for customer in response.get("data", [])
            if isinstance(customer, dict) and customer.get("customerName")
        ]

    def save_customer(self, customer_name=None):
        customer_name = customer_name or (
            "API cust " + Helpers.generate_random_string(5)
        )
        payload = {"id": 0, "customerName": customer_name}
        return self._client.post(SAVE_CUSTOMER, json=payload), customer_name
