from django.shortcuts import render

def menu_view(request):
    return render(request, 'index.html')
