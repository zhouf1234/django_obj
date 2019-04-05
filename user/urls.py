from django.urls import path,re_path
from . import views
# from django_obj.settings import MEDIA_ROOT
# from django.views.static import serve
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('',views.indexView,name='IndexList'),  #用户列表信息
    path('add_user/',views.AddUserView.as_view(),name='AddUser'),   #添加用户

    path('edit_user/', views.EditUser.as_view(), name='EditUser'),  #编辑用户
    path('get_city/', views.get_city, name='get_city'),
    path('get_country/', views.get_country, name='get_country'),
    path('user_info/', views.userInfo, name='user_info'),

    path('detail_user/', views.detailUser, name='detail_user'), #用户详细

    path('edit_pwd/', views.EditPwd.as_view(), name='EditPwd'),#修改密码

    path('upload/',views.UserImageUpload.as_view(),name="upload"),#修改用户头像

    path('restart_pwd/', views.RestartPwd.as_view(), name='restartPwd'),#发送密码重置邮件
    re_path('active/(?P<active_code>.*)/', views.changePwd, name='active'),

    path('delete_user/', views.DelUser.as_view(), name='DelUser'), #删除用户

    path('deld_user/',views.deldUser,name='deldUser'),  #已删除用户列表

    path('user_user/', views.UserUser.as_view(), name='UserUser'), #还原删除用户

    path('deletes_user/', views.DelesUser.as_view(), name='DelesUser'), #永久删除用户

    path('admin_list/',views.adminView,name='admin_list'),  #管理员列表
    path('add_admin/',views.AddAdminView.as_view(),name='AddAdmin'),   #添加新管理员

    path('delete_admin/', views.DelAdmin.as_view(), name='DelAdmin'), #删除管理员

    path('admin_admin/', views.AdminAdmin.as_view(), name='AdminAdmin'),  # 还原已删除管理员

    path('deletes_admin/', views.DelesAdmin.as_view(), name='DelesAdmin'), #永久删除管理员

]
