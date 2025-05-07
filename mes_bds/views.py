from django.shortcuts import render


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'mes_bds/index.html', {'member_list': member_list})
