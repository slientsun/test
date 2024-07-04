from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import UpdateView, ListView

from .forms import NewTopicForm, PostForm
from .models import Topic, Post, Board


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


# 从board跳转到topic
def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


# 新建topic
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():# 用于判断变量form是否有效
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(# 创建post
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)# 跳转到topic_posts
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):#从topic条撞到post
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1 #浏览量+1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):#回复topic
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)#
    # 双下划线__在这里用于进行关联查询，这是一种DjangoORM（对象关系映射）中的查询语法，称为“字段查找器”（Fieldlookups）。具体到这个例子：
    # board__pk = pk 表示在Topic模型中通过关联的board外键字段筛选，其pk（主键）等于变量pk的值。这用来限制查询的Topic必须属于指定ID的board。
    # pk = topic_pk 则直接限制查询的Topic对象的主键必须等于变量topic_pk的值。
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# Create your views here.

class PostUpdateView(UpdateView):#更改留言
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):#验证表单 处理表单验证成功后的逻辑
        post = form.save(commit=False)#保存表单数据，但不立即提交到数据库
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


def form_valid(self, form):#验证表单 处理表单验证成功后的逻辑
    post = form.save(commit=False)
    post.updated_by = self.request.user
    post.updated_at = timezone.now()
    post.save()
    return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class TopicListView(ListView):#topics分页
    model = Topic#指定模型为Topic，表示该类与Topic模型相关联
    context_object_name = 'topics'#指定在模板中使用'topics'作为对象的名称
    template_name = 'topics.html'#指定使用'topics.html'作为模板文件
    paginate_by = 2#每页显示2条

    def get_context_data(self, **kwargs):#get_context_data方法是在类视图中重写的一个方法，用于向模板传递额外的数据。在这个函数中，它将self.board对象添加到kwargs字典中，并通过调用super().get_context_data(**kwargs)返回上下文数据。
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):#get_context_data方法是在类视图中重写的一个方法，用于向模板传递额外的数据。在这个函数中，它将self.board对象添加到kwargs字典中，并通过调用super().get_context_data(**kwargs)返回上下文数据。get_queryset方法也是在类视图中重写的一个方法，用于返回查询集。在这个函数中，它首先通过get_object_or_404函数获取Board对象，使用pk参数从URL中获取。然后，它对self.board的topics进行排序，并计算每个主题的回复数（通过Count('posts') - 1实现），最后返回查询集。
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):#post分页
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset
