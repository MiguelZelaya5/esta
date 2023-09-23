from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def int_entrada(request):
    return render(request, 'interfaz_entrada.html')