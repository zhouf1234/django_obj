from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from school.models import Schools
from .models import Posts,Tag

# Create your views here.
#文章列表展示
def postsList(request):
    posts = Posts.objects.filter(is_status=1)
    context ={'posts':posts}
    return render(request,'posts/posts_list.html',context=context)

#查看文章详情
def detailPos(request):
    pos_id = request.POST.get('pos_id',None)
    posts = Posts.objects.get(id=pos_id)
    return render(request,'posts/detailpos.html',context={'posts':posts})

#编辑文章:接收数据
def editPos(request):
    pos_id = request.GET.get('pos_id',None)
    posts = Posts.objects.get(id=pos_id)
    post_school = Schools.objects.filter(is_status=1).exclude(name=posts.post_school.name)
    tag = Tag.objects.exclude(name=posts.tags.name)
    context = {
        'posts':posts,
        'post_school':post_school,
        'tag':tag
    }
    return render(request,'posts/edit_pos.html',context=context)

#编辑文章:上传数据,文章内容是用富文本编辑器写的，目前只是文本，进一步需要的是同时上传多张图片功能，哎。。。
def updatePos(request):
    # 接收数据
    pos_id = request.POST.get("pos_id",None)
    posts = Posts.objects.get(id=pos_id)

    '''处理数据'''
    data = request.POST.get('data',None)
    data = json.loads(data)

    '''处理图片数据'''
    post_image = request.FILES.get("post_image")

    if post_image != None:      #none：即没有上传新图片时的值
        posts.post_image = post_image
    print(posts.post_image)

    posts.save()
    '''对其他数据进行处理'''
    pos = Posts.objects.filter(id=pos_id)
    pos.update(**data)

    return HttpResponse(123)

#添加新文章:获取新页面
#除了文章标题外，都可不填
def addPos(request):
    post_school = Schools.objects.filter(is_status=1)
    tag = Tag.objects.all()
    context = {
        'post_school': post_school,
        'tag': tag
    }
    return render(request, 'posts/add_pos.html',context=context)

#添加新文章，上传数据
def addssPos(request):
    #获取data的数据
    data = request.POST.get('data', None)
    data = json.loads(data)
    # print(data['post_school'])
    post_image = request.FILES.get("post_image",None)
    # print(post_image)
    # 判断文章标题是否存在
    info = Posts.objects.filter(post_title=data['post_title'], is_status=1).exists()
    if info:
        return JsonResponse({
            'status': 'fail',
            'message': '该文章已存在！',
            'info': ''
        })
    Posts.objects.create(
        post_title=data['post_title'],
        source=data['source'],
        source_link=data['source_link'],
        #这两项是外键的id如果不填，会报错，标签'无'的id为5，school的id为11的是'无'，不填就给这个默认值
        tags_id='5' if data['tags']==' ' else data['tags'],
        post_school_id='11' if data['post_school']==' ' else data['post_school'],
        post_content=data['post_content'],
        post_image=post_image,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除文章，其实是把status变为0
def delPos(request):
    pos_id=request.GET.get('pos_id')
    posts = Posts.objects.get(id=pos_id)
    context={'posts':posts}
    is_status = 0
    posts.is_status = is_status
    posts.save()
    return render(request, 'posts/posts_list.html', context=context)

#已删除文章展示
def deldPos(request):
    posts = Posts.objects.filter(is_status=0)
    context ={'posts':posts}
    return render(request,'posts/deld_pos.html',context=context)

#还原删除文章，其实是把status变为1
def posPos(request):
    pos_id=request.GET.get('pos_id')
    posts = Posts.objects.get(id=pos_id)
    context={'posts':posts}
    is_status = 1
    posts.is_status = is_status
    posts.save()
    return render(request, 'posts/deld_pos.html', context=context)

#永久删除文章，删除存在数据库的信息
def delesPos(request):
    #获取id
    pos_id = request.GET.get('pos_id')
    posts = Posts.objects.get(id=pos_id)
    context = {'posts': posts}
    Posts.objects.get(id=pos_id).delete()
    return render(request,'posts/deld_pos.html',context=context)