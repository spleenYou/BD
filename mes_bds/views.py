from django.shortcuts import render


def home(request):
    member_list = None
    return render(request, 'mes_bds/index.html', {'member_list': member_list})
