from urllib.parse import quote

from config.config import API_PASSWORD, API_USERNAME
from utils.logger import get_logger

from ..api_client import APIClient
from ..endpoints import GET_ATCU_OTA_BATCH_KPI, GET_ATCU_OTA_BATCH_LIST

logger = get_logger(__name__)


ATCU_OTA_API_BASE_URL = "https://aepl-tcu4g-qa.accoladeelectronics.com"



class AtcuOtaPageAPI(APIClient):
	"""API client for ATCU OTA batch list and KPI data."""

	@staticmethod
	def _get_batch_device_data(response_data):
		"""Extract the batchDeviceData list from common API response shapes."""
		if isinstance(response_data, dict):
			payload = response_data.get("data", response_data)
			if isinstance(payload, dict):
				batch_device_data = (
					payload.get("batchDeviceData")
					or payload.get("batchData")
					or payload.get("data")
					or []
				)
				if isinstance(batch_device_data, list):
					return batch_device_data
			elif isinstance(payload, list):
				return payload
		elif isinstance(response_data, list):
			return response_data
		return []

	@staticmethod
	def get_ota_batch_list(
		page,
		page_no=1,
		size=10,
		search="",
		api_base_url=None,
		api_username=None,
		api_password=None,
	):
		"""Fetch the ATCU OTA batch list and its batchDeviceData records."""
		from config import config
		api_base_url = api_base_url or getattr(config, "API_BASE_URL", ATCU_OTA_API_BASE_URL)
		api_username = api_username or getattr(config, "API_USERNAME", "")
		api_password = api_password or getattr(config, "API_PASSWORD", "")

		endpoint = GET_ATCU_OTA_BATCH_LIST.format(
			page_no=page_no,
			size=size,
			search=quote(search, safe=""),
		)
		logger.info("Fetching ATCU OTA batch list from %s", endpoint)
		response_data = APIClient.send_request(
			page,
			api_base_url,
			api_username,
			api_password,
			"GET",
			endpoint,
		)
		batch_device_data = AtcuOtaPageAPI._get_batch_device_data(response_data)
		batch_ids = []
		for item in batch_device_data:
			if isinstance(item, dict):
				b_id = item.get("_id") or item.get("id") or item.get("batchId") or item.get("batch_id")
				if b_id:
					batch_ids.append(str(b_id))

		logger.info("Extracted %d ATCU OTA batch IDs", len(batch_ids))
		return {
			"response": response_data,
			"batchDeviceData": batch_device_data,
			"batch_ids": batch_ids,
		}


	@staticmethod
	def get_ota_batch_kpi(
		page,
		batch_ref_id,
		page_no=1,
		size=10,
		search="",
		kpi_selected="All",
		api_base_url=ATCU_OTA_API_BASE_URL,
		api_username=API_USERNAME,
		api_password=API_PASSWORD,
	):
		"""Fetch KPI data for one OTA batch reference ID."""
		if not batch_ref_id:
			raise ValueError("batch_ref_id must be provided")

		endpoint = GET_ATCU_OTA_BATCH_KPI.format(
			page_no=page_no,
			size=size,
			search=quote(search, safe=""),
			batch_ref_id=quote(str(batch_ref_id), safe=""),
			kpi_selected=quote(kpi_selected, safe=""),
		)
		logger.info("Fetching ATCU OTA batch KPI for batchRefId=%s", batch_ref_id)
		return APIClient.send_request(
			page,
			api_base_url,
			api_username,
			api_password,
			"GET",
			endpoint,
		)

	@staticmethod
	def get_ota_batch_list_with_kpi(
		page,
		page_no=1,
		size=10,
		search="",
		kpi_selected="All",
		api_base_url=ATCU_OTA_API_BASE_URL,
		api_username=API_USERNAME,
		api_password=API_PASSWORD,
	):
		"""Fetch the batch list, then fetch KPI data for its first batch ID."""
		batch_list = AtcuOtaPageAPI.get_ota_batch_list(
			page,
			page_no=page_no,
			size=size,
			search=search,
			api_base_url=api_base_url,
			api_username=api_username,
			api_password=api_password,
		)
		batch_ids = batch_list["batch_ids"]
		if not batch_ids:
			raise ValueError("No _id found in batchDeviceData")

		batch_ref_id = batch_ids[0]
		kpi_response = AtcuOtaPageAPI.get_ota_batch_kpi(
			page,
			batch_ref_id=batch_ref_id,
			page_no=page_no,
			size=size,
			search=search,
			kpi_selected=kpi_selected,
			api_base_url=api_base_url,
			api_username=api_username,
			api_password=api_password,
		)
		return {
			**batch_list,
			"batch_ref_id": batch_ref_id,
			"kpi": kpi_response,
		}
