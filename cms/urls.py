from django.urls import path
from . import views

app_name = 'cms'
urlpatterns = [

    path('',views.IndexView.as_view(),name='index'), # 当前路径表示后台首页
    path('login/',views.LoginView.as_view(),name='login'),

]
