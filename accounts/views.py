from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.forms import SignUpForm
from django.utils.decorators import method_decorator


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():#判断表单是否合法
            user = form.save()
            auth_login(request, user)#登录
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form, 'error': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required,name= 'dispatch')
class UserUpdateView(UpdateView):
    model = User #指定了模型model为User，即更新用户的信息。
    fields = ('first_name', 'last_name', 'email', )#通过fields属性指定了需要更新的字段，包括first_name、last_name和email
    template_name = 'my_account.html'#指定了模板文件my_account.html
    success_url = reverse_lazy('home')#指定了更新成功后重定向到的URL，这里使用reverse_lazy()函数来延迟解析URL，直到视图被调用。

    def get_object(self):#定义了一个get_object()方法，用于获取当前登录用户的信息。
        return self.request.user#返回当前登录用户的信息。
