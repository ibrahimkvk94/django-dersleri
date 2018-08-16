from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Dosya
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

def dosya_index(request):
    dosya_list = Dosya.objects.all()

    query = request.GET.get('q')
    if query:
        dosya_list = dosya_list.filter(Q(baslik__icontains=query)|
                                         Q(metin__icontains=query)|
                                         Q(user__first_name__icontains=query)|
                                         Q(user__last_name__icontains=query)

                                    ).distinct()


    paginator = Paginator(dosya_list, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'dosya/index.html', {'posts':posts})

def dosya_detail(request, slug):
    dosya = get_object_or_404(Dosya, slug=slug)
    form = CommentForm(request.DOSYA or None)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.dosya = dosya
        comments.save()
        return HttpResponseRedirect(dosya.get_absolute_url())


    context = {'post' : dosya,
               'form':form,}

    return render(request, 'dosya/detay.html', context)

