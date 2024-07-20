from django.shortcuts import render, redirect
from cart.models import Cart
from user_app . models import Address
from django.contrib import messages
from coupon.models import Coupon
from django.utils import timezone
import re
from checkout.models import Order, OrderItem
import razorpay
from django.conf import settings
from django.http import JsonResponse
from coupon.models import Coupon
from wallet.models import Wallet

# import paypalrestsdk

# Create your views here.

# Coupon 


def coupon(request):
    if 'username' in request.session:
        if request.method == 'GET':
            cpn = request.GET.get('coupon')
            if not cpn:
                messages.info(request, 'Please enter coupon')
                return redirect('check_out')
            current_date = timezone.now()
            coupon_exists = Coupon.objects.filter(expired=False, expiry_date__gte=current_date, coupon_code=cpn).exists()
            if not coupon_exists:
                messages.info(request,'Enter valid coupon')
                return redirect('check_out')
            coupon = Coupon.objects.get(coupon_code = cpn)
            row_cart = Cart.objects.filter(user = request.user)
            for item in row_cart:
                if item.product_qty > item.product.quantity:
                    Cart.objects.delete(id = item.id)
            cart_item = Cart.objects.filter(user = request.user)
            sub_totel=0
            totel_price = 0
            shipping = 10
            wallet_amount = 0
            wallet = Wallet.objects.filter(user = request.user)
            for w in wallet:
                wallet_amount = wallet_amount + w.amount
            for item in cart_item:
                sub_totel = sub_totel + item.product.selling_price * item.product_qty
            if coupon.minimum_amount <totel_price:
                messages.info(request, 'minimum '+ str(coupon.minimum_amount)+ ' needed to apply the coupon')
                return redirect('check_out')
            request.session['coupon'] = coupon.coupon_code 
            totel_price = sub_totel+10-coupon.discount_price
            user_address = Address.objects.filter(user = request.user)
            context = {'cart_item':cart_item,
                    'totel_price':totel_price,
                    'user_address':user_address,
                    'coupon':coupon,
                    'sub_totel':sub_totel,
                    'shipping':shipping,
                    'wallet_amount':wallet_amount}
        return render(request, 'checkout/checkout.html', context)
    return redirect('/')
    
# Razorpay client

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))          



# Check out View


def check_out(request):
    if 'username' in request.session:
        row_cart = Cart.objects.filter(user = request.user)
        currency = 'INR'
        for item in row_cart:
            if item.product_qty > item.product.quantity:
                Cart.objects.delete(id = item.id)
        cart_item = Cart.objects.filter(user = request.user)
        sub_totel=0
        totel_price = 0
        shipping = 10
        wallet_amount=0
        wallet = Wallet.objects.filter(user = request.user)
        for w in wallet:
            wallet_amount = wallet_amount + w.amount
        for item in cart_item:
            sub_totel = sub_totel + item.product.selling_price * item.product_qty
        totel_price = sub_totel+shipping
        user_address = Address.objects.filter(user = request.user)
        razorpay_order = razorpay_client.order.create(dict(
            amount = totel_price,
            currency = currency,
            payment_capture = '0'
        ))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        context = {'cart_item':cart_item,
                'totel_price':totel_price,
                'user_address':user_address,
                'sub_totel':sub_totel,
                'shipping' : shipping,
                'razorpay_merchant_key':settings.RAZOR_KEY_ID,
                'razorpay_order_id':razorpay_order_id,
                'razorpay_amount':totel_price,
                'currency':currency,
                'callback_url':callback_url,
                'wallet_amount':wallet_amount
                }
        return render(request, 'checkout/checkout.html', context)
    return redirect('/')

# Check out view address

def check_address(request):
    if 'username' in request.session:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            house_no = request.POST.get('house_no')
            post_code = request.POST.get('post_code')
            state = request.POST.get('state')
            street = request.POST.get('street')
            phone_no = request.POST.get('phone_number')
            city = request.POST.get('city')

            if (not full_name or
                not house_no or
                not post_code or
                not state or
                not street or
                not phone_no or
                not city ):
                messages.info(request, 'Please fill all fields')
            elif post_code and not re.match(r'^\d{6}$', post_code):
                messages.info(request, 'Please fill valid 6 digit pincode')
            elif  not re.match(r'^[789]\d{9}$', phone_no):
                messages.info(request, 'Please fill valid phone number')
            else:
                user = request.user
                address = Address(user = user,
                                full_name = full_name,
                                house_no = house_no,
                                state = state,
                                street = street,
                                post_code = post_code,
                                phone_no = phone_no,
                                city = city)
                address.save()
                return redirect('check_out')
        return render(request, 'checkout/check_address.html')
    else:
        return redirect('/')



#Place order view

def place_order(request):
    if 'username' in request.session:
        cart_items = Cart.objects.filter(user = request.user)
    
        user = request.user
        if request.method == 'POST':
            payment = request.POST.get("payment")
            address_id = request.POST.get("addressId")
            total = request.POST.get('total')
    
        if not payment:
            messages.info(request,'Please select payment method!!')
            return redirect('check_out')
        if  address_id == 'Select':
            messages.info(request,'Input Address!!')
            return redirect('check_out')
        address = Address.objects.get(id = address_id)
        order = Order.objects.create(
            user=user,
            address=address,
            amount=total,
            payment_type=payment,
        )
    
        for item in cart_items:
            product = item.product
            product.quantity -= item.product_qty
            print(item.product_qty)


            order_item = OrderItem.objects.create(order = order,
                                                product = item.product,
                                                quantity = item.product_qty,
                                                image = item.product.img )
        wal = Wallet.objects.filter(user = request.user)
        wal.delete()
        if 'val' in request.session:
            val=int(request.session['val'])
            Wallet.objects.create(
                                user = request.user,
                                status = 'refund',
                                amount = val
                                )
        if 'wallet_amount' in request.session:
            del request.session['wallet_amount']
        if 'coupon' in request.session:
            del request.session['coupon']
        if 'val' in request.session:
            del request.session['val']
        
        cart_items.delete()
        return redirect('orders_view')
    return redirect('/')





# Razorpay


def razorpay(request, address_id):
    if 'username' in request.session:
        user = request.user
        shipping =10
        subtotel=0
        payment = 'razorpay'
        user = request.user
        cart_items = Cart.objects.filter(user = user)
        address = Address.objects.get(id=address_id)
        for item in cart_items:
            subtotel = subtotel +(item.product.selling_price * item.product_qty)
        if 'coupon' in request.session:
            if 'wallet_amount' in request.session:
                coupon = Coupon.objects.get(coupon_code = request.session['coupon'])
                wal_am = request.session['wallet_amount']
                discount_price=coupon.discount_price
                total = (subtotel+shipping-discount_price)-int(wal_am)
            else:
                coupon = Coupon.objects.get(coupon_code = request.session['coupon'])
                discount_price=coupon.discount_price
                total = subtotel+shipping-discount_price
        else:
            if 'wallet_amount' in request.session:
                wal_am = request.session['wallet_amount']
                total = (subtotel+shipping)-int(wal_am)
            else:
                total = subtotel+shipping
        order = Order.objects.create(
            user=user,
            address=address,
            amount=total,
            payment_type=payment,
        )

        for cart_item in cart_items:
            product = cart_item.product
            product.quantity -= cart_item.product_qty
            product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.product_qty,
                image=cart_item.product.img,
            )
        wal = Wallet.objects.filter(user = request.user)
        wal.delete()
        if 'val' in request.session:
            val=int(request.session['val'])
            Wallet.objects.create(
                                user = request.user,
                                status = 'refund',
                                amount = val
                                )
        
        if 'wallet_amount' in request.session:
            del request.session['wallet_amount']
        if 'coupon' in request.session:
            del request.session['coupon']
        if 'val' in request.session:
            del request.session['val']
        cart_items.delete()
        return redirect('orders_view')
    else:
        return redirect('/')



# proceedtopay


def proceedtopay(request):
    if 'username' in request.session:
        cart = Cart.objects.filter(user=request.user)
        total = 0
        subtotel = 0
        shipping = 10
        for item in cart:
            subtotel = subtotel +(item.product.selling_price * item.product_qty)
        if 'coupon' in request.session:
            if 'wallet_amount' in request.session:
                coupon = Coupon.objects.get(coupon_code = request.session['coupon'])
                wal_am = request.session['wallet_amount']
                discount_price=coupon.discount_price
                total = (subtotel+shipping-discount_price)-int(wal_am)
                return JsonResponse({'total':total})
            else:
                coupon = Coupon.objects.get(coupon_code = request.session['coupon'])
                discount_price=coupon.discount_price
                total = subtotel+shipping-discount_price
                return JsonResponse({'total':total})
        else:
            if 'wallet_amount' in request.session:
                wal_am = request.session['wallet_amount']
                total = (subtotel+shipping)-int(wal_am)
                return JsonResponse({'total':total})
            else:
                total = subtotel+shipping
                return JsonResponse({'total':total})
    else:
        return redirect('/')
    



# Wallet using placed order
    

def wallet_order(request):
    if 'username' in request.session:
        shipping = 10
        totel_price = 0
        sub_totel = 0
        wallet_amount = 0
        wal_amount = 0
        val=0
        if request.method == 'POST':
            total = request.POST.get('price')
            wallet = Wallet.objects.filter(user = request.user)
            for w in wallet:
                wallet_amount = wallet_amount + w.amount
            if float(total) >= float(wallet_amount):
                totel_price = float(total)-float(wallet_amount)
                wal_amount = float(wallet_amount)
                request.session['wallet_amount'] = wal_amount
            else:
                totel_price=1
                val = (float(wallet_amount)-float(total))+1
                request.session['val'] = val
                wal_amount = float(total)-1
                request.session['wallet_amount'] = wal_amount
            cart_item=Cart.objects.filter(user=request.user)
            coupon=None
            if 'coupon' in request.session:
                coupon = Coupon.objects.get(coupon_code = request.session['coupon'])
            for item in cart_item:
                sub_totel = sub_totel + item.product.selling_price * item.product_qty
            user_address = Address.objects.filter(user = request.user)
            context = {'cart_item':cart_item,
                'totel_price':totel_price,
                'user_address':user_address,
                'sub_totel':sub_totel,
                'shipping':shipping,
                'wal_amount':wal_amount,
                'wallet_amount':val,
                'coupon':coupon}
        return render(request, 'checkout/checkout.html', context)
    else:
        return redirect('/')
    









