from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"staticportfolio/index.html")

def valentine(request):
    return render(request, "staticportfolio/valentine.html")