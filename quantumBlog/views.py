# QuantumIndex/quantumBlog/views.py

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Review
from .forms import ReviewForm


# Index view, main page
def index(request):
    recent_posts = Post.objects.all().order_by('-created_at').filter(published=True)[:3]
    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(published=True).order_by('-created_at')

    def count(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return post.likes.count()


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.order_by('-created_at')
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            review = form.save(commit=False)
            review.post = self.object
            review.user = request.user
            review.save()
        return self.get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_create.html'
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_edit.html'
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('post_list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post/post_confirm_delete.html'


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('index'))


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    post_id = review.post.id
    review.delete()
    return redirect('post_detail', pk=post_id)


# About view
def about(request):
    return render(request, 'about.html')
