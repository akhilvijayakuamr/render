from django.shortcuts import render, redirect
from products.models import Product
from .models import Wishlist
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.


# View Wishlist


def wish_list(request):
    if 'username' in request.session:
        wi = Wishlist.objects.filter(user = request.user)
    else:
        messages.info(request, 'Login to continue')
    context = {'wi' : wi}
    return render(request, 'wishlist/wishlist.html', context)


# Add to wishlist

def add_to_wishlist(request):
    if request.method == 'POST':
        if 'username' in request.session:
            prod_id =  int(request.POST.get('product_id'))
            product_check = Product.objects.get(id = prod_id)
            if product_check:
                if Wishlist.objects.filter(user = request.user.id, product_id = prod_id):
                    return JsonResponse({'status':'Product already in Wishlist'})
                else:
                        Wishlist.objects.create(user = request.user,
                                            product_id = prod_id)
                        return JsonResponse({'status' : 'Product add successfully'})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status':'Login to continue'})
        



# Remove Wishlist
        

def remove_wishlist(request, wid):
    if 'username' in request.session:
        wis = Wishlist.objects.filter(user = request.user, id = wid)
        wis.delete()
        return redirect('wishlist')
    else:
        return redirect('/')
        