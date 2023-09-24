from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
##@login_required
def int_entrada(request):
    return render(request, 'interfaz_entrada.html')

def salir(request):
    logout(request)
    return redirect('/')

