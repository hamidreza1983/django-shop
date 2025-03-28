from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView
)
from .models import Blog, BlogTags, Comment, Replay
from .forms import *
from accounts.models import Profile, User
from django.contrib import messages

class BlogView(ListView):
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'
    model = Blog

    def get_queryset(self):
        if self.kwargs.get('tag'):
            return Blog.objects.filter(tags__name=self.kwargs['tag'], status=True).order_by('-created_at')
        return Blog.objects.filter(status=True).order_by('-created_at')

class BlogDetataiView(DetailView):
    model = Blog
    template_name = 'blog/blog-post.html'
    context_object_name = 'blog'
    queryset = Blog.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.total_views += 1
        blog.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = BlogTags.objects.all()
        return context
    
class CreateReplayView(FormView):
    form_class = ReplayForm

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        return redirect('blog:blog-details', pk=comment.blog.pk)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            replay = form.save(commit=False)
            replay.comment = comment
            replay.name = profile
            replay.email = email
            replay.save()
            messages.success(request, 'پاسخ شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود')
            return redirect('blog:blog-details', pk=comment.blog.pk)
        else:
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال پاسخ')
        return super().form_invalid(form)


class CreateCommentView(CreateView):
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        return redirect(f'blog/blog-details/{blog.pk}')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.name = profile
            comment.email = email
            comment.save()
            messages.success(request, 'کامنت شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود')
            return redirect('blog:blog-details', pk=blog.pk)
        else:
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال کامنت')
        return super().form_invalid(form)