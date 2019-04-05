from django.urls import path
from . import views

urlpatterns = [
    path('school_list/', views.schList, name='schList'),    #院校列表展示

    path('edit_sch/', views.editSch, name='editSch'),    #编辑院校信息
    path('update_sch/', views.updateSch, name='updateSch'),

    path('detail_sch/', views.detailSch, name='detailSch'), #查看院校信息详情

    path('delete_sch/', views.delSch, name='delSch'),       #删除院校信息

    path('add_sch/', views.addSch, name='addSch'),          #添加新院校,需要优化填写判断输入
    path('addss_sch/', views.addssSch, name='addssSch'),

    path('school_type/', views.schType, name='schType'),    #院校类型展示

    path('edit_type/', views.editType, name='editType'),        #编辑院校类型
    path('update_type/', views.updateType, name='updateType'),

    path('delete_type/', views.delType, name='delType'),    #删除院校类型

    path('add_schtype/', views.addSchtype, name='addSchtype'), #添加新院校类型,需要优化填写判断输入
    path('addss_schtype/', views.addssSchtype, name='addssSchtype'),

    path('school_fea/', views.schFea, name='schFea'),   #院校特征展示

    path('edit_fea/', views.editFea, name='editFea'),       #编辑院校特征
    path('update_fea/', views.updateFea, name='updateFea'),

    path('delete_fea/', views.delFea, name='delFea'),   #删除院校特征

    path('add_schfea/', views.addSchfea, name='addSchfea'), #添加新院校特征,需要优化填写判断输入
    path('addss_schfea/', views.addssSchfea, name='addssSchfea'),

    path('deld_sch/', views.deldSch, name='deldSch'),   #已删除院校展示
    path('sch_sch/', views.schSch, name='schSch'),      #还原已删除院校
    path('deletes_sch/', views.delesSch, name='delesSch'),#永久删除院校信息，数据库数据删除

    path('deld_schtype/', views.deldSchtype, name='deldSchtype'), #已删除院校类型展示
    path('type_type/', views.typeType, name='typeType'),        #还原已删除院校类型
    path('deletes_type/', views.delesType, name='delesType'),   #永久删除院校类型

    path('deld_schfea/', views.deldSchfea, name='deldSchfea'),  #已删除院校特征展示
    path('fea_fea/', views.feaFea, name='feaFea'),              #还原已删除院校特征
    path('deletes_fea/', views.delesFea, name='delesFea'),      #永久删除院校特征
]