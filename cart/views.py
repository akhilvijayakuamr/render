from django.shortcuts import render, redirect
from products.models import Product
from django.http import JsonResponse
from cart.models import Cart
from django.contrib import messages
from wishlist.models import Wishlist
# Create your views here.


# User view cart

# View cart page

def view_cart(request):
    if 'username' in request.session:
        if 'username' in request.session:
            ca = Cart.objects.filter(user = request.user)
        else:
            messages.info(request, 'Login to continue')
        context = { 'ca' : ca}
        return render(request, 'cart/Cart.html', context)
    else:
        return redirect('/')



# Add to cart

def add_to_cart(request):
    if 'username' in request.session:
        if request.method == 'POST':
            if 'username' in request.session:
                prod_id =  int(request.POST.get('product_id'))
                product_check = Product.objects.get(id = prod_id)
                if product_check:
                    if Cart.objects.filter(user = request.user.id, product_id = prod_id):
                        return JsonResponse({'status':'Product already in cart'})
                    else:
                        prod_qty = int(request.POST.get('product_qty'))
                        if product_check.quantity >= prod_qty:
                            Cart.objects.create(user = request.user,
                                                product_id = prod_id,
                                                product_qty = prod_qty)
                            return JsonResponse({'status' : 'Product add successfully'})
                        else:
                            return JsonResponse({'status' : 'Only '+ str(product_check.quantity) +' quantity Available'})
                else:
                    return JsonResponse({'status':'No such product found'})
            else:
                return JsonResponse({'status':'Login to continue'})
    else:
        return redirect('/')
        
# Add to cart in wishlist
        
def add_to_cart_wishlist(request):
    if 'username' in request.session:
        if request.method == 'POST':
            if 'username' in request.session:
                prod_id =  int(request.POST.get('product_id'))
                product_check = Product.objects.get(id = prod_id)
                if product_check:
                    if Cart.objects.filter(user = request.user.id, product_id = prod_id):
                        return JsonResponse({'status':'Product already in cart'})
                    else:
                        Cart.objects.create(user = request.user,
                                            product_id = prod_id)
                        Wishlist.objects.get(product__id = prod_id ).delete()
                        return JsonResponse({'status' : 'Product add successfully'})
                        
                else:
                    return JsonResponse({'status':'No such product found'})
            else:
                return JsonResponse({'status':'Login to continue'})
        return redirect('/')
        

# Remove Cart
        
def remove_cart(request, cid):
    if 'username' in request.session:
        ca = Cart.objects.filter(id = cid)
        ca.delete()
        return redirect('cart')
    else:
        return redirect('/')

# Update Cart

def update_cart(request):
    if 'username' in request.session:
        if request.method == 'POST':
            prod_id = int(request.POST.get('product_id'))
            if(Cart.objects.filter(user = request.user, product_id = prod_id)):
                prod_qty = int(request.POST.get('product_qty'))
                cart = Cart.objects.get(product_id = prod_id, user = request.user)
                cart.product_qty = prod_qty
                cart.save()
                return JsonResponse({'status' : "Update Successfully"})
        return redirect('user_home')
    else:
        return redirect('/')

