from django.urls import path
from . import views

urlpatterns = [
    path('server_posts_list/', views.serverpostsList, name='serverpostsList'),    #服务中心文章表展示

    path('detail_ser_pos/', views.detailserPos, name='detailserPos'),  # 查看服务文章详情
    path('edit_ser_pos/', views.editserPos, name='editserPos'),  # 编辑服务文章
    path('update_ser_pos/', views.updateserPos, name='updateserPos'),
    path('add_ser_pos/', views.addserPos, name='addserPos'),  # 添加新服务文章
    path('addss_ser_pos/', views.addssserPos, name='addssserPos'),
    path('delete_ser_pos/', views.delserPos, name='delserPos'),  #删除服务文章

    path('server_cates/', views.serverCates, name='serverCates'),    #服务中心分类展示

    path('edit_ser_cates/', views.editserCates, name='editserCates'),  # 编辑服务分类
    path('update_ser_cates/', views.updateserCates, name='updateserCates'),
    path('add_ser_cates/', views.addserCates, name='addserCates'),  # 添加新服务分类
    path('addss_ser_cates/', views.addssserCates, name='addssserCates'),
    path('delete_ser_cates/', views.delserCates, name='delserCates'),  #删除服务分类

    path('server_center_list/', views.servercenterList, name='servercenterList'),    #教学中心展示

    path('detail_ser_center/', views.detailserCenter, name='detailserCenter'),  # 查看教学中心详情
    path('edit_ser_center/', views.editserCenter, name='editserCenter'),  # 编辑教学中心
    path('update_ser_center/', views.updateserCenter, name='updateserCenter'),
    path('add_ser_center/', views.addserCenter, name='addserCenter'),  # 添加新教学中心
    path('addss_ser_center/', views.addssserCenter, name='addssserCenter'),
    path('delete_ser_center/', views.delserCenter, name='delserCenter'),  #删除教学中心

    path('server_atta/', views.serverAtta, name='serverAtta'),    #附件表展示

    path('detail_ser_atta/', views.detailserAtta, name='detailserAtta'),  # 查看附件详情
    path('edit_ser_atta/', views.editserAtta, name='editserAtta'),  # 编辑附件
    path('update_ser_atta/', views.updateserAtta, name='updateserAtta'),
    path('add_ser_atta/', views.addserAtta, name='addserAtta'),  # 添加新附件
    path('addss_ser_atta/', views.addssserAtta, name='addssserAtta'),
    path('delete_ser_atta/', views.delserAtta, name='delserAtta'),  #删除附件

    path('server_aques/', views.serverAques, name='serverAques'),    #模拟题表展示

    path('detail_ser_aqu/', views.detailserAqu, name='detailserAqu'),  # 查看模拟题附件详情
    path('edit_ser_aqu/', views.editserAqu, name='editserAqu'),  # 编辑模拟题附件
    path('update_ser_aqu/', views.updateserAqu, name='updateserAqu'),

    path('add_ser_aqu/', views.addserAqu, name='addserAqu'),  # 添加新模拟题附件
    path('get_maj/', views.get_maj, name='get_maj'),  #
    path('get_lev/', views.get_lev, name='get_lev'),  #
    path('addss_ser_aqu/', views.addssserAqu, name='addssserAqu'),

    path('delete_ser_aqu/', views.delserAqu, name='delserAqu'),  # 删除模拟题附件

    path('deld_ser_pos/', views.deldserPos, name='deldserPos'),  # 已删除服务文章展示
    path('deld_ser_cates/', views.deldserCates, name='deldserCates'),  # 已删除服务分类
    path('deld_ser_center/', views.deldserCenter, name='deldserCenter'),  # 已删除教学中心
    path('deld_ser_atta/', views.deldserAtta, name='deldserAtta'),  # 已删除附件
    path('deld_ser_aqu/', views.deldserAqu, name='deldserAqu'),  # 已删除模拟题

    path('pos_ser_pos/', views.posserPos, name='posserPos'),  # 还原已删除服务文章
    path('cates_ser_cates/', views.catesserCates, name='catesserCates'),  # 还原已删除服务分类
    path('center_ser_center/', views.centerserCenter, name='centerserCenter'),  # 还原已删除教学中心
    path('atta_ser_atta/', views.attaserAtta, name='attaserAtta'),  # 还原已删除附件
    path('aqu_ser_aqu/', views.aquserAqu, name='aquserAqu'),  # 还原已删除模拟题

    path('deletes_ser_pos/', views.delesserPos, name='delesserPos'),  # 永久删除服务文章
    path('deletes_ser_cates/', views.delesserCates, name='delesserCates'),  # 永久删除服务分类
    path('deletes_ser_center/', views.delesserCenter, name='delesserCenter'),  # 永久删除教学中心
    path('deletes_ser_atta/', views.delesserAtta, name='delesserAtta'),  # 永久删除附件
    path('deletes_ser_aqu/', views.delesserAqu, name='delesserAqu'),  # 永久删除模拟题

]