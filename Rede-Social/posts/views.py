from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.select_related('author').prefetch_related('likes', 'comments__author').all()

    liked_posts = set()
    if request.user.is_authenticated:
        liked_posts = set(
            Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    comment_form = CommentForm()

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Publicação criada com sucesso!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicação eliminada.')
    return redirect('post_list')


@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes(),
    })


@login_required
@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        messages.success(request, 'Comentário adicionado!')
    return redirect('post_list')


def user_posts(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).select_related('author').prefetch_related('likes', 'comments__author')

    liked_posts = set()
    if request.user.is_authenticated:
        liked_posts = set(
            Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    comment_form = CommentForm()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'liked_posts': liked_posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/user_posts.html', context)
