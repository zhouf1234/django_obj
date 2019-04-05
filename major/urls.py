from django.urls import path
from . import views

urlpatterns = [
    path('major_list/', views.majorList, name='majorList'),    #专业列表展示

    path('detail_maj/', views.detailMaj, name='detailMaj'), #查看专业详情

    path('edit_maj/', views.editMaj, name='editMaj'),       #编辑专业信息
    path('update_maj/', views.updateMaj, name='updateMaj'),

    path('add_maj/', views.addMaj, name='addMaj'),          #添加新专业
    path('addss_maj/', views.addssMaj, name='addssMaj'),

    path('delete_maj/', views.delMaj, name='delMaj'),       #删除专业信息

    path('major_cates/', views.majorCates, name='majorCates'),    #专业分类展示

    path('add_cates/', views.addCates, name='addCates'),          #添加新专业分类
    path('addss_cates/', views.addssCates, name='addssCates'),

    path('edit_cates/', views.editCates, name='editCates'),       #编辑专业分类
    path('update_cates/', views.updateCates, name='updateCates'),

    path('delete_cates/', views.delCates, name='delCates'),       #删除专业分类

    path('deld_maj/', views.deldMaj, name='deldMaj'),    #已删除专业展示
    path('maj_maj/', views.majMaj, name='majMaj'),  # 还原已删除专业
    path('deletes_maj/', views.delesMaj, name='delesMaj'),  #永久删除专业信息

    path('deld_cates/', views.deldCates, name='deldCates'),    #已删除专业分类展示
    path('cates_cates/', views.catesCates, name='catesCates'),    #还原已删除专业分类
    path('deletes_cates/', views.delesCates, name='delesCates'),    #永久删除专业分类
]