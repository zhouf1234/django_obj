from django.urls import path
from . import views

urlpatterns = [
    path('order_list/', views.orderList, name='orderList'), #报名信息展示

    path('detail_ord/', views.detailOrd, name='detailOrd'), #查看报名信息详情

    path('edit_ord/', views.editOrd, name='editOrd'),       #编辑报名信息

    path('get_cates/', views.get_cates, name='get_cates'),  #用于edit_ord0.html了
    path('get_school/', views.get_school, name='get_school'), #用于edit_ord0.html了

    path('update_ord/', views.updateOrd, name='updateOrd'),

    path('add_ord/', views.addOrd, name='addOrd'),          #添加新报名信息
    path('get_catess/', views.get_catess, name='get_catess'),
    path('get_level/', views.get_level, name='get_level'),
    path('get_schools/', views.get_schools, name='get_schools'),
    path('addss_ord/', views.addssOrd, name='addssOrd'),

    path('delete_ord/', views.delOrd, name='delOrd'),       #删除报名信息

    path('deld_ord/', views.deldOrd, name='deldOrd'),    #已删除报名信息展示
    path('ord_ord/', views.ordOrd, name='ordOrd'),  # 还原已删除报名信息
    path('deletes_ord/', views.delesOrd, name='delesOrd'),  #永久删除报名信息
]