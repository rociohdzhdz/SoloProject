from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def index(request):
    #return HttpResponse('placeholder to users reg')
    return render(request, "index.html")