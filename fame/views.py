from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.forms import UserRegisterForm
from accounts.models import UserProfile
from articles.models import Article
from photos.models import Photo


from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from stickypics.models import Stickypic
from .settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from .forms import PasswordResetRequestForm, SetPasswordForm, SignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your Fame account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse("Thank you for your email confirmation. Now you can login your account. <a href='/login'>login now </a>")
    else:
        return HttpResponse('Activation link is invalid!')


class ResetPasswordRequestView(FormView):
    template_name = "registration/password_reset_form.html"    #code for template is given below the view's code
    success_url = '/account/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

   # This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):

 #   A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).

        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above

          #  If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.

            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'http://127.0.0.1:8000',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000', #or your domain
                        'site_name': 'example',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "registration/password_reset_form.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)






@login_required(login_url='/login')
def index(request):
    context={'pins':Photo.objects.all().order_by('-timestamp')}
    return render(request,'test.html',context)



class SearchView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request,*args,**kwargs):
        query=request.GET.get('q')
        print(query)
        qs=None
        if query:
            photo=Photo.objects.filter(
                Q(caption__icontains=query)|
                Q(user__username__icontains=query))

            sticky=Stickypic.objects.filter(
                Q(description__icontains=query)|
                Q(source__icontains=query)|
                Q(user__username__icontains=query)
            )
            people=UserProfile.object.filter(
                Q(fullname__icontains=query)|
                Q(user__username__icontains=query)|
                Q(bio__icontains=query)
            )
            article=Article.published.filter(
                Q(title__icontains=query)|
                Q(user__username__icontains=query)|
                Q(body__icontains=query)
            )


            all=chain(sticky,photo,article)
            sort_all = sorted(all,
                        key=lambda instance: instance.pk,
                        reverse=True)

            all_count=len(sort_all)

        context={'photo_list':photo,
                 'sticky_list':sticky,
                 'people_list':people,
                 'article_list':article,
                 'all':sort_all,
                 'all_count':all_count,

                  }
        return render (request,'search_result.html',context)


