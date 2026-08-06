from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Thread, Reply

"""
TODO: Security, this code IS NOT safe for production whatsoever
"""

# Create your views here.
def index(request):        
    categories = Category.objects.all().order_by("order")
    return render(request, "forum/index.html", {"categories": categories})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    threads_qs = category.threads.order_by("-is_pinned", "-updated_at")
    paginator = Paginator(threads_qs, 10)
    threads = paginator.get_page(request.GET.get("page"))
    return render(request, "forum/category.html", {
        "category": category,
        "threads": threads,
    })


def thread(request, category_slug, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id, category__slug=category_slug)
    if request.method == "POST" and request.user.is_authenticated:
        Reply.objects.create(
            thread=thread,
            body=request.POST["body"],
            author=request.user,
        )
        return redirect("forum:thread", category_slug=category_slug, thread_id=thread.pk)
    
    return render(request, "forum/thread.html", {
        "thread": thread,
        "replies": thread.replies.order_by  ("created_at"),
    })

@login_required
def new_thread(request):
    if request.method == "POST":
        category = get_object_or_404(Category, slug=request.POST.get("category"))
        thread = Thread.objects.create(
            category=category,
            title=request.POST["title"],
            body=request.POST["body"],
            author=request.user,
        )
        return redirect("forum:thread", category_slug=category.slug, thread_id=thread.pk)
    return render(request, "forum/new_thread.html", {
        "categories": Category.objects.all().order_by("order"),
    })