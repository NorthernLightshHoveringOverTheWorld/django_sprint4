from datetime import date

from blog.models import Category, Post
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    render,
)


def index(request):
    today = date.today()
    posts = (
        Post.objects.select_related("category")
        .filter(
            is_published=True,
            pub_date__lte=today,
            category__is_published=True,
        )
        .select_related("category", "location", "author")
        .order_by("-pub_date")[:5]
    )
    context = {"blog_list": posts}
    return render(request, "blog/index.html", context)


def category_posts(request, category_slug):
    today = date.today()
    category = get_object_or_404(
        Category,
        Q(slug=category_slug) & Q(is_published=True),
    )
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=today,
    ).select_related("category", "location", "author")
    context = {
        "blog_list": posts,
        "category": category,
    }
    return render(request, "blog/category.html", context)


def post_detail(request, id):
    today = date.today()
    post = get_object_or_404(
        Post,
        Q(id=id)
        & Q(is_published=True)
        & Q(pub_date__lte=today)
        & Q(category__is_published=True),
    )
    context = {"post": post}
    return render(request, "blog/detail.html", context)
