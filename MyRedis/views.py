from django.shortcuts import HttpResponse
from django.views.decorators.cache import cache_page



#视图增加redis缓存
@cache_page(60 * 15)
def myredis(request):
    if request.method == "GET":
        return HttpResponse(111)
    else:
        pass
