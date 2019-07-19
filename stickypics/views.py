from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from accounts.models import UserProfile

from stickypics.forms import StickypicModelForm, CommentModelForm
from stickypics.models import Stickypic, Comment


class StickypicCreateAndListView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Stickypic
    form_class = StickypicModelForm
    template_name = 'stickypics/stickypic_list.html'

    login_url = 'login'
    success_message = 'Your Stickypic created successfully'

    def form_valid(self, form):
        form = StickypicModelForm(self.request.POST, self.request.FILES)
        form.instance.user = self.request.user

        return super(StickypicCreateAndListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StickypicCreateAndListView, self).get_context_data(**kwargs)
        following_post = self.request.user.profile.get_following()
        qs1 = self.model.objects.filter(user__in=following_post)
        qs2 = self.model.objects.filter(user=self.request.user)
        content = (qs1 | qs2).distinct().order_by('-update_at')
        context['recommended'] = UserProfile.object.recommended(self.request.user)[:4]

        context['object_list'] = content

        return context


class StickypicUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Stickypic
    template_name = 'stickypics/stickypic_update.html'
    login_url = 'login'
    success_message = 'Your Stickypic update successfully'
    form_class=StickypicModelForm


class StickypicDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Stickypic
    template_name='stickypics/delete_confirm.html'
    login_url = 'login'
    success_message = 'Your Stickypic Delete Successfully'
    form_class=StickypicModelForm
    success_url = reverse_lazy('stickypic:stickylist')



@login_required()
def stickypic_detail(request,pk):
    #like_part
    stickypic=get_object_or_404(Stickypic,id=pk)
    is_liked=False
    if stickypic.liked.filter(id=request.user.id):
        is_liked=True

    #comment
    comments=Comment.objects.filter(stickypic=stickypic).order_by('-update_at')
    if request.method=='POST':
        comment_form=CommentModelForm(request.POST or None)
        if comment_form.is_valid():
            content=request.POST.get('comment')
            comment=Comment.objects.create(stickypic=stickypic,user=request.user,comment=content)
            comment.save()
            return HttpResponseRedirect(stickypic.get_absolute_url())
    else:
        comment_form=CommentModelForm()

    context={
        'object':stickypic,
        'is_liked':is_liked,
        'comment_form':comment_form,
        'comments':comments,
    }
    return render(request,'stickypics/stickypic_detail.html',context)



def like_post(request):
    post=get_object_or_404(Stickypic,id=request.POST.get('object_id'))
    is_liked=False
    if post.liked.filter(id=request.user.id):
        post.liked.remove(request.user)
        is_liked=False
    else:
        post.liked.add(request.user)
        is_liked=True
    return redirect('stickypic:stickydetail',pk=post.pk)