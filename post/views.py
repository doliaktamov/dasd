from pyexpat import model
from re import template
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin,CreateView):
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_posted = datetime.now()
        return super(PostCreateView, self).form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list') 


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = 'comment_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.date_posted = datetime.now()
        return super(CommentCreateView, self).form_valid(form)

