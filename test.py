import openapi_client
from a_protocol_0.enums.ServerActionEnum import ServerActionEnum
from openapi_client.api.default_api import DefaultApi

client = DefaultApi(openapi_client.ApiClient())
print(client.health())
action = Action(enum=ServerActionEnum.SEARCH_TRACK, arg=Search.LAST_SEARCH)
