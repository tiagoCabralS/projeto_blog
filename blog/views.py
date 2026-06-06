from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from blog.forms import PostForm
from blog.models import Post

def index(request):
    posts = Post.objects.order_by('id')
    
    context = {
        'title': 'Página Inicial - ',
        'posts': posts
    }
    
    return render(
        request, 
        'blog/index.html',
        context
        )

def novo_post(request):
    form_action = reverse('blog:novo_post')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            
            post.save()
            return redirect('blog:index')
    
    context = {
        'form': PostForm(),
        'form_action': form_action
    }
    
    return render(
        request,
        'blog/novo_post.html',
        context
    )

def post_detail(request, post_id):
    single_post = get_object_or_404(
        Post.objects.filter(pk=post_id)
    )
    
    context = {
        'post': single_post,
    }
    
    return render(
        request,
        'blog/post_detail.html',
        context
    )