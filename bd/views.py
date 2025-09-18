from django.shortcuts import render


def under_construction(request):
    return render(request, 'site_under_construction.html')
