from django.urls import path, reverse_lazy, re_path
from . import views
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [

    # path('signup/', views.signup, name='signup'),

    re_path(r'^signup/$', views.signup,name='signup'),  # 改为re_path # 注册视图

    path('logout/', LogoutView.as_view(), name='logout'),    # 注销视图

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # 登录视图

    path('reset/', PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt', ),
         name='password_reset'
         ), # 密码重置

    path('reset/done/', PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),# 重置完成

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),# 重置确认

    path('reset/complete/', PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),# 重置完成
    # 修改用户信息
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),# 修改用户信息
    #修改密码
    path('settings/password/', PasswordChangeView.as_view(template_name= 'password_change.html'), name='password_change'),# 修改密码
    #修改密码完成
    path('settings/password/done/', PasswordChangeDoneView.as_view(template_name= 'password_change_done.html'), name='password_change_done'),# 修改密码完成

]
