from django.shortcuts import render, get_object_or_404, redirect
from .models import *

def home(request):
    post = Blog.objects.order_by('-id')
    
    main_post = Blog.objects.order_by('-id').filter(Main_post=True)[0:1]
    recent = Blog.objects.filter(section='Recent').order_by('-id')[0:5]
    popular = Blog.objects.filter(section='Popular').order_by('-id')[0:5]
    category = Category.objects.all()


    context = {
        'post': post,    
        'main_post': main_post,
        'recent': recent,
        'popular': popular,
        'category': category,
    }

    return render(request, 'index.html', context)

def blog_detail(request, slug):
    category = Category.objects.all()
    post = get_object_or_404(Blog, blog_slug=slug)
    popular = Blog.objects.filter(section='Popular').order_by('-id')[0:5]
    comment = Comment.objects.filter(blog_id = post.id).order_by('-date')

    print(post)

    context = {
        'post': post,
        'category': category,
        'comment': comment,
        'popular':popular,
    }

    return render(request, 'blog_detail.html', context)

def category(request, slug):
    cat = Category.objects.all()
    blog_cat = Category.objects.filter(slug=slug)
    context = {
        'cat': cat,
        'active_category': slug,
        'blog_cat': blog_cat,
    }

    return render (request, 'category.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug=slug)
        email = request.POST.get('InputEmail')
        web = request.POST.get('InputWeb')
        name = request.POST.get('InputName')
        comment_text = request.POST.get('InputComment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        # Comment.objects.create(
        #     post=post,
        #     name=name,
        #     email=email,
        #     website=web,
        #     comment_text=comment_text,
        #     parent=parent_comment
        # )
        Comment.objects.create(
            post=post,
            comment=request.POST.get("InputComment")
        )

        return redirect ('blog_detail', slug=post.blog_slug)

    return redirect ('blog_detail')

def blog(request):
    post = Blog.objects.order_by('-id')
    recent = Blog.objects.filter(section='Recent').order_by('-id')[0:5]
    popular = Blog.objects.filter(section='Popular').order_by('-id')[0:5]

    context = {
        'post': post,    
        'recent': recent,
        'popular': popular,
    }

    return render(request, 'blog.html', context)

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def search(request):
    query = request.GET.get('search')  # 'q' matches the name in the input field
    results = []

    if query:
        results = Blog.objects.filter(title__icontains=query)

    return render(request, 'search.html', {'query': query, 'results': results})


