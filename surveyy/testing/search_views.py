from .models import Test
from django.db.models import Q
from django.shortcuts import render

def search(request):
    q = request.GET.get('q')
    tests = Test.objects.filter(title__icontains=q)
    print(tests)
    return render(request, "testing/search.html", {"tests": tests, "q": q})
    
def search_ajax(request):
    ...