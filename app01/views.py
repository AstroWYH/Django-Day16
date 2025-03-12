from django.shortcuts import render, redirect
from app01 import models

# Create your views here.
def depart_list(request):
    """ depart list """
    
    # 去数据库中获取所有的 Department List 信息
    # queryset 可理解为列表，[[对象], [对象], [对象]]
    queryset = models.Department.objects.all()
    
    return render(request, "depart_list.html", {"queryset": queryset})

def depart_add(request):
    """ depart add """
    if request.method == "GET":
        return render(request, "depart_add.html")
    
    # 获取用户通过 Post 提交的数据(暂时默认title不为空)
    title = request.POST.get("title")
    
    # 保存到数据库
    models.Department.objects.create(title=title)
    
    # 重定向回 Department List
    return redirect("/depart/list/")

def depart_delete(request):
    """ depart delete """
    # 获取ID
    nid = request.GET.get("nid")
    # 删除
    models.Department.objects.filter(id=nid).delete()
    
    # 重定向回 Department List
    return redirect("/depart/list/")

# 这里是配合 urls.py 里传递的中间的 int, 这种传值方式可能比 ? 更方便
def depart_edit(request, nid):
    """ depart edit """
    # nid 不用专门去获取了，已经通过参数传递过来了
    # .first 是从 queryset 里取第一个对象; 即使只有一个, queryset 也是 [对象]
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()
        print(row_obj.id, row_obj.title)
        return render(request, "depart_edit.html", {"row_obj": row_obj})

    # 获取用户提交的 title
    title=request.POST.get("title")
    # 根据 id 找到数据库中的数据，进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回 Department List
    return redirect("/depart/list/")
