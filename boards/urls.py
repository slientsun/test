from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # views.index是指view里的index方法，name=“home"是路径  #首页，运行开始的界面
    # path('boards/<int:pk>/', views.board_topics, name='board_topics'),  # 运行路径‘boards/<int:pk>/’（带参）
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),

    # path('boards/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    # 修改回复信息
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    # 分页
    path('boards/<int:pk>/', views.TopicListView.as_view(),name='board_topics'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(),name='topic_posts'),

]
