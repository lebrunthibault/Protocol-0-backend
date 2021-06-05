from django.shortcuts import render

from django.http import HttpResponse, JsonResponse


class Search():
    LAST_SEARCH = None


def index(request):
    return HttpResponse("Hello, world. You're at the protocol 0 index.")


def search(request, search):
    response = HttpResponse("You searched for : %s, last_search: %s" % (search, Search.LAST_SEARCH))
    Search.LAST_SEARCH = search
    return response


def action(request):
    if Search.LAST_SEARCH:

        response = JsonResponse({'action': 'SEARCH_TRACK', 'arg': Search.LAST_SEARCH})
        Search.LAST_SEARCH = None
        return response
    else:
        return HttpResponse()
