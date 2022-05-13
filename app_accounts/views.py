import logging
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from app_accounts.forms import LoginForm, RegisterForm, UserProfileForm, EmployeeProfileForm
from app_accounts.models import Employee, User
from app_accounts.service import create_user
from app_organization.models import OrgMembers
from app_project.models import ProjectMember
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                redirect_url = reverse_lazy('home')
                return redirect(redirect_url)
            else:
                messages.error(request, 'Bad Credentials', extra_tags='danger')
        return render(request, self.template_name, {'form': form})


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                create_user(form)
                return redirect('auth:login')
            except Exception as e:
                logging.error(e)
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


# def user_profile(request, user_id):
#     # user = request.user
#     employee = OrgMembers.objects.filter(user=user_id)
#     project = ProjectMember.objects.filter(user=user_id)
#     users = Employee.objects.filter(user_id=user_id)
#     context = {
#         'employees': employee,
#         'projects': project,
#         'users': users
#     }
#     return render(request, 'profile.html', context=context)
#
#
# def ProfileUpdateView(request):
#     emp = Employee.objects.get(user_id=request.user.employee)
#     if request.method == "POST":
#         u_form = UserProfileForm(request.POST, instance=request.user)
#         e_form = EmployeeProfileForm(request.POST, request.FILES, instance=emp)
#         if u_form.is_valid() and e_form.is_valid():
#             u_form.save()
#             e_form.save()
#             return redirect('auth:profile')
#     else:
#         u_form = UserProfileForm(instance=request.user)
#         e_form = EmployeeProfileForm(instance=emp)
#     context = {'u_form': u_form, 'e_form': e_form}
#     return render(request, 'update_profile.html', context=context)
