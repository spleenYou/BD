from django.shortcuts import render


def test(request):
    return render(request, 'mes_bds/index.html')
