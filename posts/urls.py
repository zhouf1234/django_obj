from django.urls import path
from . import views


urlpatterns = [
    path('posts_list/', views.postsList, name='postsList'),    #文章表展示

    path('detail_pos/', views.detailPos, name='detailPos'),  # 查看文章详情

    path('edit_pos/', views.editPos, name='editPos'),  # 编辑文章
    path('update_pos/', views.updatePos, name='updatePos'),

    path('add_pos/', views.addPos, name='addPos'),  # 添加新文章
    path('addss_pos/', views.addssPos, name='addssPos'),

    path('delete_pos/', views.delPos, name='delPos'),  #删除文章

    path('deld_pos/', views.deldPos, name='deldPos'),  # 已删除文章展示
    path('pos_pos/', views.posPos, name='posPos'),  # 还原已删除文章
    path('deletes_pos/', views.delesPos, name='delesPos'),  # 永久删除文章
]