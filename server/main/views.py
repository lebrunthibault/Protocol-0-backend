from django.http import HttpResponse, JsonResponse
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


class Search():
    LAST_SEARCH = None


def index(request):
    return HttpResponse("Hello, world. You're at the protocol 0 index.")


def search(request, search):
    response = HttpResponse("You searched for : %s, last_search: %s" % (search, Search.LAST_SEARCH))
    Search.LAST_SEARCH = search
    return response


def show_plugins(request):
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
        send_keys('^%p')
    return HttpResponse("show plugins")


def action(request):
    if Search.LAST_SEARCH:

        response = JsonResponse({'action': 'SEARCH_TRACK', 'arg': Search.LAST_SEARCH})
        Search.LAST_SEARCH = None
        return response
    else:
        return HttpResponse()
