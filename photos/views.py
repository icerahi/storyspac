from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from accounts.models import UserProfile
from photos.forms import PhotoModelForm,CommentModelForm
from photos.models import Photo, Comment, Notification
import re




class PhotoCreateAndListView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Photo
    form_class = PhotoModelForm
    template_name = 'photos/photo_list.html'
    success_url = '/photo/'
    login_url = 'login'
    success_message = 'Your Post created successfully'

    
    def form_valid(self, form):

        form=PhotoModelForm(self.request.POST, self.request.FILES)
        form.instance.user=self.request.user

        return super(PhotoCreateAndListView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context=super(PhotoCreateAndListView, self).get_context_data(**kwargs)
        following_post=self.request.user.profile.get_following()
        qs1=self.model.objects.filter(user__in=following_post)
        qs2=self.model.objects.filter(user=self.request.user)
        content=(qs1 | qs2 ).distinct().order_by('-timestamp')


        context['recommended']=UserProfile.object.recommended(self.request.user)
        context['object_list']=content

        return context

class PhotoUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Photo
    form_class = PhotoModelForm
    template_name = 'photos/update_view.html'
   #success_url = "/photo/"
    login_url = 'login'
    success_message = "Your Post Updated Successfully"



class PhotoDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Photo
    form_class=PhotoModelForm
    template_name = 'photos/delete_confirm.html'
    success_url = reverse_lazy('photo:list')
    login_url = 'login'
    success_message = "YOur POst has been deleted"
# search View in the fame main view




@login_required(login_url='login')
def photo_detail(request,pk):

    photo=get_object_or_404(Photo,id=pk)

    viewed=request.session.get('viewed',[])
    if viewed:
        if photo.id not in viewed:
            viewed.append(photo.id)
            request.session['viewed']=viewed
            photo.views +=1
            photo.save()
    else:
        viewed=[photo.id]
        request.session['viewed']=viewed
        photo.views +=1
        photo.save()
    comments=Comment.objects.filter(photo=photo).order_by('-timestamp')
    is_liked=False
    if photo.liked.filter(id=request.user.id).exists():
        is_liked=True
    if request.method=='POST':
        comment_form=CommentModelForm(request.POST or None)
        if comment_form.is_valid():
            content=request.POST.get('comment')
            comment=Comment.objects.create(photo=photo,user=request.user,comment=content)
            comment.save()
            return HttpResponseRedirect(photo.get_absolute_url())
    else:
        comment_form=CommentModelForm()
    context={
        'object':photo,
        'is_liked':is_liked,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'photos/photo_detail.html',context)




@login_required(login_url='login')
def like_post(request):

    post=get_object_or_404(Photo,id=request.POST.get('object_id'))
    is_liked=False
    if post.liked.filter(id=request.user.id):
        post.liked.remove(request.user)
        is_liked=False
    else:
        post.liked.add(request.user)
        is_liked=True
    return redirect('photo:detail', pk=post.pk)

#Queryset returns three types of notifications specific to each user.
class ViewNotifications(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification.html'

    def get_queryset(self):
        object_list = Notification.objects.filter(
        Q(profile_id=self.request.user.id) |
        ~Q(role_user=self.request.user)
        )
        return object_list