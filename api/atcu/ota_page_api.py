from urllib.parse import quote

from utils.logger import get_logger

from ..api_client import APIClient
from ..endpoints import GET_ATCU_OTA_BATCH_KPI, GET_ATCU_OTA_BATCH_LIST

logger = get_logger(__name__)

from config import config

class AtcuOtaPageAPI(APIClient):
	"""API client for ATCU OTA batch list and KPI data."""

	BASE_URL = config.API_BASE_URL
	USERNAME = config.API_USERNAME
	PASSWORD = config.API_PASSWORD

	@staticmethod
	def get_ota_batch_list(
		page,
		page_no=1,
		size=10,
		search="",
		api_base_url=BASE_URL,
		api_username=USERNAME,
		api_password=PASSWORD,
	):
		"""Return the OTA batch list response."""

		endpoint = GET_ATCU_OTA_BATCH_LIST.format(
			page_no=page_no,
			size=size,
			search=quote(search, safe=""),
		)
		logger.info("Fetching ATCU OTA batch list from %s", endpoint)
		logger.debug("username and password %s %s", api_username, api_password)
		result = APIClient.send_request(
			page,
			api_base_url,
			api_username,
			api_password,
			"GET",
			endpoint,
		)
		batch_device_data = result.get("data", {}).get("batchDeviceData", [])
		batch_ids = [
			batch["_id"]
			for batch in batch_device_data
			if isinstance(batch, dict) and batch.get("_id")
		]
		return result, batch_ids


	@staticmethod
	def get_ota_batch_kpi(
		page,
		batch_ref_id,
		page_no=1,
		size=10,
		search="",
		kpi_selected="All",
		api_base_url=BASE_URL,
		api_username=USERNAME,
		api_password=PASSWORD,
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

