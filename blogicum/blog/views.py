from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import CommentForm, PostForm, RegistrationForm, UserEditForm
from .models import Category, Comment, Post

User = get_user_model()

POSTS_PER_PAGE = 10


def _public_posts_q():
    now = timezone.now()
    return Q(
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
    )


def _base_posts_qs():
    return (
        Post.objects.select_related("category", "location", "author")
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )


def _paginate(request, qs):
    paginator = Paginator(qs, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    posts = _base_posts_qs().filter(_public_posts_q())
    context = {"page_obj": _paginate(request, posts)}
    return render(request, "blog/index.html", context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        Q(slug=category_slug) & Q(is_published=True),
    )
    posts = _base_posts_qs().filter(category=category).filter(_public_posts_q())
    context = {
        "page_obj": _paginate(request, posts),
        "category": category,
    }
    return render(request, "blog/category.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(
        _base_posts_qs(),
        id=post_id,
    )
    if post.author != request.user and not (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category
        and post.category.is_published
    ):
        raise Http404

    comments = post.comments.select_related("author").all()
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = _base_posts_qs().filter(author=profile_user)
    if request.user != profile_user:
        posts = posts.filter(_public_posts_q())
    context = {
        "profile": profile_user,
        "page_obj": _paginate(request, posts),
    }
    return render(request, "blog/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "blog/user.html", {"form": form})


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/registration_form.html", {"form": form})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author_id != request.user.id:
        return redirect("blog:post_detail", post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            post.refresh_from_db()
            comments = post.comments.select_related("author").all()
            return render(
                request,
                "blog/detail.html",
                {"post": post, "comments": comments, "form": CommentForm()},
            )
    else:
        form = PostForm(instance=post)
    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author_id != request.user.id:
        return redirect("blog:post_detail", post_id=post.id)
    form = PostForm(instance=post)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category
        and post.category.is_published
    ):
        raise Http404

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("blog:post_detail", post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post.id)
    else:
        form = CommentForm(instance=comment)
    return render(
        request,
        "blog/comment.html",
        {"form": form, "comment": comment},
    )


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post.id)
    return render(
        request,
        "blog/comment.html",
        {"comment": comment},
    )
