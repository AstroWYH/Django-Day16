from django.db import models

# Create your models here.
class Department(models.Model):
    """ Department Table """
    title = models.CharField(verbose_name='Title', max_length=32)
    
class UserInfo(models.Model):
    """ UserInfo Table """
    name = models.CharField(verbose_name='Name', max_length=16)
    password = models.CharField(verbose_name='Password', max_length=64)
    age = models.IntegerField(verbose_name='Age')
    account = models.DecimalField(verbose_name='Account', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='Create Time')
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='Department ID')
    # 1.有约束
    # to 与表关联
    # to_filed 与表中列关联
    # 2.这种情况(ForeignKey)，django 自动会添加后缀_id，此时写的depart，到mysql里，会变成depart_id
    # 3.DepartmentTable 如果删除了某个 DepartmentId
    # 3.1级联删除: 和这个 DepartmentId 关联的 UserInfoId 那些行的数据，也删除
    depart = models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE)
    # 3.2置空：和这个 DepartmentId 关联的 UserInfoId 那些行的数据，不删除，置空
    # depart = models.ForeignKey(to='Department',to_field='id',null=True,blank=True, ondelete=models.SET_NULL())
    
    # 在 django 中做的约束，gender 只能 1 or 2 以后
    gender_choices = ((1, 'Male'), (2, 'Female'))
    gender = models.SmallIntegerField(verbose_name='Gender', choices=gender_choices)