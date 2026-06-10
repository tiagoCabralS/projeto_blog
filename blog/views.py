from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages

from blog.forms import PostForm, RegisterForm
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

@login_required(login_url='blog:login')
def novo_post(request):
    form_action = reverse('blog:novo_post')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            
            post.save()
            messages.success(request, 'Post publicado com sucesso.')
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

@login_required(login_url='blog:login')
def post_update(request, post_id):
    form_action = reverse('blog:post_update', args=(post_id,))
    post = get_object_or_404(
        Post,
        pk=post_id,
        owner=request.user
    )
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        context = {
        'form': form,
        'form_action': form_action
    }
        
        if form.is_valid():
            print('Formulário válido')
            post = post.save()
            return redirect('blog:post_update', post_id=post_id)
        
    context = {
        'form': PostForm(instance=post),
        'form_action': form_action
    }
    
    return render(
        request,
        'blog/post_update.html',
        context
        )

@login_required(login_url='blog:login')    
def post_delete(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')
    print('confirmation: ', confirmation)
    
    if confirmation == "'yes'":
        post.delete()
        return redirect('blog:index')
    
    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
            'confirmation': confirmation
        }
    )

def login(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('blog:index')
        messages.error(request, 'Login ou senha inválidos.')
    
    context = {
        'form': form
    }
    
    return render(
        request,
        'blog/login.html',
        context
    )
 
@login_required(login_url='blog:login')   
def logout(request):
    auth.logout(request)
    messages.info(request, 'Você saiu do sistema')
    return redirect('blog:login')
    
def register(request):
    context = {
        'form': RegisterForm()
        }
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado.')
            return redirect('blog:login')
        messages.error(request, 'Usuário ou senha inválidoss.')
    
    return render(
        request,
        'blog/register.html',
        context
    )