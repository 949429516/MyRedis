from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.cache import cache_page
from app01 import models
from django.core.cache import cache


# 视图增加redis缓存
@cache_page(60 * 15)
def myredis(request):
    if request.method == "GET":
        return HttpResponse(111)
    else:
        pass


def find_person(request):
    if request.method == "GET":
        # 判断redis中是否有缓存数据
        redis_key = "person"
        redis_value = cache.get(redis_key)
        if redis_value and len(redis_value) > 0:
            # 如果有并且不是空列表,返回redis缓存
            name_list = redis_value
        else:
            name_list = models.myperson.objects.all()
            # 查询出结果放入redis
            cache.set(redis_key, name_list)
        return render(request, 'person.html', {'name_list': name_list})
    else:
        name = request.POST.get('user')
        models.myperson.objects.create(name=name)
        # 删除redis缓存,模糊匹配key返回列表（增删改查都要加）
        redis_key = cache.keys('person*')
        for k in redis_key:
            cache.delete(k)
        return redirect('/app01/person/')


def find_condition(request):
    """
    带条件查询需要key多样化

    customer:name_ khno_ state_
    """
    name = request.GET.get('name', '')  # 没有值反回空
    age = request.GET.get('age', '')
    state = request.GET.get('state', '')
    redis_key = f'customer:name_{name}:age_{age}:state_{state}'
    redis_value = cache.get(redis_key)
    if redis_value and len(redis_value) > 0:
        return redis_value
    else:
        cache.set(redis_key, redis_value)
