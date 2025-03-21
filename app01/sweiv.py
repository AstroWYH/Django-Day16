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

def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    """
    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。
    """
    return render(request, 'user_list.html', {"queryset": queryset})

def user_add(request):
    """ 添加用户（原始方式） """

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


# ################################# ModelForm 示例 #################################
from django import forms

class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})