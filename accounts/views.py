from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, FormView, CreateView

from accounts.forms import UserRegisterForm, ProfileEditForm, UserEditForm, PasswordChangeForm
from accounts.models import UserProfile

class UserRegisterView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        email=form.cleaned_data.get('email')

        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        print(email)
        new_user=User.objects.create(username=username,email=email,password=password)
        new_user.set_password(password)
        new_user.save()

        
        return super(UserRegisterView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin,DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def get_object(self, queryset=None):
        return get_object_or_404(User,username__iexact=self.kwargs.get('username'))

    def get_context_data(self,*args, **kwargs):
        context=super(UserDetailView, self).get_context_data(*args,**kwargs)
        following=UserProfile.object.is_following(self.request.user,self.get_object())
        context['following']=following
        return context






class PeopleListView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'people/people.html'
    login_url = 'login'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context=super(PeopleListView, self).get_context_data(*args,**kwargs)

        context['recommended'] = UserProfile.object.recommended(self.request.user)


        return context


class UserFollowView(View):
    def get(self,request,username,*args,**kwargs):

        toggle_user=get_object_or_404(User,username__iexact=username)
        if request.user.is_authenticated:
            is_following=UserProfile.object.toggle_follow(request.user,toggle_user)

        return redirect("profile:userdetail",username=username)








### account update view
### profile update view (not worked yet successfullly
@login_required()
def profile_edit(request,username):
    username=request.user.username
    if request.method=="POST":
        profile_form=ProfileEditForm(request.POST or None,request.FILES, instance=request.user.profile)

        user_form=UserEditForm(request.POST or None,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.user=request.user
            user_form.user=request.user
            user_form.email=request.user.email
            profile_form.save(commit=True)
            user_form.save(commit=True)
            return redirect('profile:userdetail',username=request.user.username)
    else:
        profile_form=ProfileEditForm(instance=request.user.profile)

        user_form=UserEditForm(instance=request.user)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'accounts/profile_edit.html',context)
