from django.shortcuts import render, HttpResponse

# Create your views here.

def home_view(request):


    if request.user.is_authenticated:
        context = {
            'isim' : 'İbra',
        }
    else:
        context = {
            'isim' : 'Misafir',
        }

    return render(request, 'home.html', context)
