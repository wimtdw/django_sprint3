from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Category, Post


def get_posts():
    now = timezone.now()
    posts = Post.objects.select_related('category', 'location').filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    )
    return posts


def index(request):
    template = 'blog/index.html'
    posts = get_posts()[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_posts(), pk=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
        ),
        slug=category_slug
    )
    now = timezone.now()
    posts = category.posts.select_related('location').filter(
        pub_date__lte=now,
        is_published=True,
    )
    context = {'category': category,
               'post_list': posts}
    return render(request, template, context)
