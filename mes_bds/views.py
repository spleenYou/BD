from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'mes_bds/index.html', {'member_list': member_list})


@login_required
def account(request):
    return render(request, 'mes_bds/account.html')
