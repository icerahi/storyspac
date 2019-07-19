from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.views.generic import CreateView

from articles.forms import ArticleCreateForm, ArticleEditForm, CommentForm
from articles.models import Article, Images, Comment
from django.forms import modelformset_factory


def article_list(request):
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)

    formset=ImageFormset(queryset=Images.objects.none())


    form=ArticleCreateForm()

    following_post = request.user.profile.get_following()
    qs1 = Article.published.filter(user__in=following_post)
    qs2 = Article.published.filter(user=request.user)
    articles = (qs1 | qs2).distinct().order_by('-updated')



    context={'form':form,
             'formset':formset,
             "object_list":articles}
    return render(request,'articles/article_list.html',context)



def article_create(request):
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
    if request.method=="POST":
        form=ArticleCreateForm(request.POST)

        formset=ImageFormset(request.POST or None,request.FILES or None)

        if form.is_valid() and formset.is_valid():
            article=form.save(commit=False)
            article.user=request.user
            article.save()

            for f in formset:
                try:
                    photo=Images(article=article,image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break

            return redirect('article:list')


def article_edit(request,id):
    ImagesFormset = modelformset_factory(Images, fields=('image',), extra=4,max_num=4)
    article=get_object_or_404(Article,id=id)

    if article.user !=request.user:
        raise Http404()

    if request.method=="POST":
        form=ArticleEditForm(request.POST or None,instance=article)
        formset=ImagesFormset(request.POST or None,request.FILES or None)


        if form.is_valid() and formset.is_valid():
            form.save()
            data = Images.objects.filter(article=article)

            for index,f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        image=Images(article=article,image=f.cleaned_data.get('image'))
                        image.save()

                    elif f.cleaned_data['image'] is False:
                        image=Images.objects.get(id=request.POST.get('form-'+str(index)+'-id'))
                        image.delete()
                    else:
                        image=Images(article=article,image=f.cleaned_data.get('image'))
                        d=Images.objects.get(id=data[index].id)
                        d.image=image.image
                        d.save()

            return redirect(article.get_absolute_url())
    else:
        form=ArticleEditForm(instance=article)

        formset=ImagesFormset(queryset=Images.objects.filter(article=article))

    context={
        'form':form,
        'article':article,
        'formset':formset,
    }
    return render(request,'articles/article_update.html',context)



def article_detail(request,pk,slug):
    article=get_object_or_404(Article,id=pk,slug=slug)

    comments=Comment.objects.filter(article=article,reply=None).order_by('-timestamp')

    is_liked=False
    if article.liked.filter(id=request.user.id).exists():
        is_liked=True

    is_favourite=False
    if article.favourite.filter(id=request.user.id).exists():
        is_favourite=True

    if request.method=="POST":
        comment_form=CommentForm(request.POST or None)

        if comment_form.is_valid():
            comment=request.POST.get('comment')
            reply_id=request.POST.get('object_id')
            comment_qs=None

            if reply_id:
                comment_qs=Comment.objects.get(id=reply_id)

            obj=Comment.objects.create(article=article,user=request.user,comment=comment,reply=comment_qs)
            obj.save()
            return redirect(article.get_absolute_url())
    else:
        comment_form=CommentForm()

    context={'object':article,
             'is_liked':is_liked,
             'is_favourite':is_favourite,
             'comments':comments,
             'form':comment_form,}
    return render(request,'articles/article_detail.html',context)

def favourite(request,id):
    article=get_object_or_404(Article,id=id)
    if article.favourite.filter(id=request.user.id).exists():
        article.favourite.remove(request.user)
    else:
        article.favourite.add(request.user)

    return redirect(article.get_absolute_url())



def like_post(request):
    post=get_object_or_404(Article,id=request.POST.get('object_id'))
    is_liked=False
    if post.liked.filter(id=request.user.id):
        post.liked.remove(request.user)
        is_liked=False
    else:
        post.liked.add(request.user)
        is_liked=True
    return redirect(post.get_absolute_url())

def article_delete(request,id):
    article=get_object_or_404(Article,id=id)
    if request.user != article.user:
        raise Http404

    article.delete()
    return redirect('article:list')