# handler.py
import traceback
from importlib import import_module
import warnings
warnings.simplefilter("ignore")

from akerbp.mlops.cdf.helpers import get_function_metadata
from akerbp.mlops.core import logger, config
service_name = config.envs.service_name
logging=logger.get_logger("mlops_cdf")

service = import_module(f"akerbp.mlops.services.{service_name}").service


def handle(data, client, secrets, function_call_info):
   try:
      config.update_cdf_keys(secrets)
      output = service(data, secrets)
      metadata = get_function_metadata(client, function_call_info)
      output.update(metadata)
      return output
   except Exception:
      trace = traceback.format_exc()
      error_message = f"{service_name} service failed.\n{trace}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
