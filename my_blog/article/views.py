from django.shortcuts import render

# 导入数据模型ArticlePost
from .models import ArticlePost
import markdown
# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)
    # return HttpResponse("Hello World!")


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                     ])

    context = {'article': article}
    return render(request, 'article/detail.html', context)


def article_create(request):
    if request.method == 'POST':
        article_post_from = ArticlePostForm(data=request.POST)
        if article_post_from.is_valid():
            new_article = article_post_from.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_from = ArticlePostForm()
        context = {'article_post_form': article_post_from}
        return render(request, "article/create.html", context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_from = ArticlePostForm(data=request.POST)
        if article_post_from.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse("填写错误")
    else:
        article_post_from = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_from}
        return render(request, 'article/update.html', context)
