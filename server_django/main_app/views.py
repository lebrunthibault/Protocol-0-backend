from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.request import Request

from lib.click import pixel_has_color
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from scripts.commands.reload_ableton import reload_ableton


class Search():
    LAST_SEARCH = None


class MainView(View):
    @staticmethod
    def _response(res):
        return JsonResponse({"res": res})

    @staticmethod
    @api_view()
    def index(request):
        return MainView._response("protocol0 server up")

    @staticmethod
    @api_view()
    def test(request: Request, id: int):
        return MainView._response(f"id: {id}")

    @staticmethod
    @api_view()
    def bad_request(request):
        return HttpResponse("bad request", status=400)

    @staticmethod
    @api_view()
    def search(request, search):
        res = HttpResponse("You searched for : %s, last_search: %s" % (search, Search.LAST_SEARCH))
        Search.LAST_SEARCH = search
        return MainView._response(res)

    @staticmethod
    @api_view()
    def pixel_has_color(request):
        res = pixel_has_color(x=int(request.GET.get('x')), y=int(request.GET.get('y')), color=request.GET.get('color'))
        return MainView._response(res)

    @staticmethod
    @api_view()
    def show_plugins(request):
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')
        return MainView._response("ok")

    @staticmethod
    @api_view()
    def show_hide_plugins(request):
        send_keys('^%p')
        return MainView._response("ok")

    @staticmethod
    @api_view()
    def hide_plugins(request):
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')
        return MainView._response("ok")

    @staticmethod
    @api_view()
    def arrow_up(request):
        send_keys("{UP}")
        return MainView._response("ok")

    @staticmethod
    @api_view()
    def reload_ableton(request):
        reload_ableton()
        return MainView._response("ok")

    @staticmethod
    @api_view()
    def show_windows(request):
        result = show_windows()
        return JsonResponse(result, safe=False)

    @staticmethod
    @api_view()
    def action(request):
        if Search.LAST_SEARCH:
            res = JsonResponse({'action': 'SEARCH_TRACK', 'arg': Search.LAST_SEARCH})
            Search.LAST_SEARCH = None
            return MainView._response(res)
        else:
            return MainView._response({'action': None})
