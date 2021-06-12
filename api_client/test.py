from pprint import pprint

import openapi_client
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
from api_client.openapi_client.api.default_api import DefaultApi

configuration = openapi_client.Configuration(
    host="http://localhost:8000"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = DefaultApi(api_client)

    print(openapi_client.__file__)
    try:
        # Index
        api_response = api_instance.read_item_items_item_id_get()
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->index_get: %s\n" % e)
