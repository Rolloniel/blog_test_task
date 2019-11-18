from django.contrib import auth
from django.http import Http404, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm


class ShowHomeView(View):
    """
    Default view for displaying home page

    """
    template = 'news/news_list.html'

    def get(self, request):
        return redirect('/news/')


class NewsListView(View):
    """
    Default view for displaying list of posts

    """
    template = 'news/news_list.html'

    def get(self, request):
        post_list = Post.objects.filter(state="P")
        paginator = Paginator(post_list, 3)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {'post_list': posts}

        return render(request, self.template, context)

    def post(self, request):
        if not request.session or not request.session.session_key:
            request.session.save()
        return render(request, self.template)


class NewsPremoderationListView(View):
    """
    View for displaying posts that require premoderation

    """
    template = 'news/news_list.html'

    def get(self, request):
        post_list = Post.objects.filter(state="NP")
        paginator = Paginator(post_list, 3)
        page = request.GET.get('page')
        print("PING!", page)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {'post_list': posts}
        return render(request, self.template, context)


class NewsDetailView(View):
    model = Post
    template = "news/news_post.html"

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(pk=pk)
        if not post.exists():
            raise Http404('Post with this ID does not exist')

        post = post.first()
        return render(request, self.template, {'post': post})


class NewsAddView(View):
    form = PostForm()
    model = Post
    template = "news/news_edit.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form})

    def post(self, request):
        form = PostForm(request.POST)
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.created = timezone.now()
            if 'base_ui.no_moderation_required' in user.get_all_permissions() or user.is_superuser or user.is_staff:
                post.state = 'P'
            else:
                post.state = 'NP'
            post.save()
            return redirect("news_detail", pk=post.pk)


class NewsEditView(View):
    model = Post
    template = "news/news_edit.html"

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        if post.author.pk == request.user.pk or request.user.is_superuser or request.user.is_staff:
            return render(request, self.template, {'form': form})
        else:
            return HttpResponseNotAllowed("ASDF")

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.updated = timezone.now()
            post.save()
            return redirect("news_detail", pk=post.pk)


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")
