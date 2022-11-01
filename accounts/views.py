from django.shortcuts import render ,redirect
from django.views import View
from accounts.forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code, check_expired_code , IsAdminUserMixin
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
# Create your views here.


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    def get(self,request):
        return render(request,self.template_name,context={'form':self.form_class})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone'],random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'],code=random_code)
            request.session['user_registration_info']={
                'phone_number':form.cleaned_data['phone'],
                'email':form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password'],
            }
            messages.success(request,'we sent you a code','success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, context={'form': form})

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self,request):
        return render(request,'accounts/verify.html',context={'form':self.form_class})

    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                # if check_expired_code(code_instance.created):
                User.objects.create_user(phone_number=user_session['phone_number'],email=user_session['email'],
                                         full_name=user_session['full_name'],password=user_session['password'])
                code_instance.delete()
                messages.success(request,'you registered','success')
                return redirect('home:home')
                # else :
                #     code_instance.delete()
                #     messages.error(request, 'time code has expired', 'danger')
                #     return redirect('accounts:user_register')
            else:
                messages.error(request,'this code wrong','danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,context={'form':self.form_class})

    def post(self,request,*args,**kwargs):
        form  = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number=cd['phone'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','info')
                return redirect('home:home')
            messages.error(request,'phone or password is wrong','warning')
        return render(request,self.template_name,context={'form':form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'you logged out successfully','success')
        return redirect('home:home')