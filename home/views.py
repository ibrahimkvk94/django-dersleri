from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

# Create your views here.

def home_view(request):
    post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(Q(baslik__icontains=query)|
                                         Q(metin__icontains=query)|
                                         Q(user__first_name__icontains=query)|
                                         Q(user__last_name__icontains=query)

                                    ).distinct()


    paginator = Paginator(post_list, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'posts':posts})