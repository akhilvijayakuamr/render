from django.shortcuts import render, redirect
from .models import Wallet

# Create your views here.


# Wallet


def wallet(request):
    if 'username' in request.session:
        user=request.user
        wal=Wallet.objects.filter(user=user)
        Total = 0
        for val in wal:
            Total = Total+val.amount
        context = {'wal':wal,
                'Total':Total}
        return render(request, 'wallet/wallet.html', context)
    else:
        return redirect('/')
