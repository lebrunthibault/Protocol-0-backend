# Executed with python 2
import logging
import os

from protocol0.utils.decorators import EXPOSED_P0_METHODS

from lib.openapi_spec_generation import generate_api_specs

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    generate_api_specs(title="P0 script API", methods_dict=EXPOSED_P0_METHODS, out_folder=os.path.dirname(__file__),
                       package_name="p0_script_api")
