from django.shortcuts import render, redirect, reverse
from . models import Customuser
from django.contrib import messages
from django.contrib.auth import login, logout
from products.models import Product
from banner.models import Banner
import re
import smtplib
import secrets
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views.decorators.cache import cache_control,never_cache
import string
import random
from wallet.models import Wallet
from django.http import JsonResponse


# Create your views here.


# Home page
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def user_home(request):
            if 'username' in request.session:
                val = Product.objects.filter(trending = True)
                last_5_banners = Banner.objects.all().order_by('-created_at')[:5]

                if last_5_banners.count() >= 5:
                    banner1, banner2, banner3, banner4, banner5 = (
                    last_5_banners[0],
                    last_5_banners[1],
                    last_5_banners[2],
                    last_5_banners[3],
                    last_5_banners[4],
                )
                else:
                    banner1, banner2, banner3, banner4, banner5 = None, None, None, None, None

                context = {'val':val,
                           'banner1':banner1,
                           'banner2':banner2,
                           'banner3':banner3,
                           'banner4':banner4,
                           'banner5':banner5}
                return render(request, 'auth_app/index.html', context)
            else:
                 return redirect('/')
        
    


# Register User
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache    
def user_register(request):
        if request.method == 'POST':
            try:
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                username = request.POST.get('username')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone_number')
                user_bio=request.POST.get('user_bio')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                refferal_code  =    request.POST.get('refferal')

                if not (firstname 
                        and lastname 
                        and username 
                        and email
                        and phone_number
                        and user_bio
                        and password1
                        and password2):
                    messages.info(request, 'Please fill required fields')
                    return redirect('user_register')
                
                if password1 != password2:
                    messages.error(request, 'Password mismatch')
                    return redirect('user_register')
                
                elif Customuser.objects.filter(username = username).exists():
                    messages.info(request, "User name already exits")
                    return redirect('user_register')
                    
                elif Customuser.objects.filter(email = email).exists():
                    messages.info(request, "Email is already exits")
                    return redirect('user_register')
                        
                elif Customuser.objects.filter(phone_number = phone_number).exists():
                    messages.info(request, 'Phone number already exits')
                    return redirect('user_register')
                
                elif not validate_email(email):
                    messages.error(request, 'Please enter a valid email address.')
                    return redirect('user_register')
                
                elif not re.match(r'^[789]\d{9}$', phone_number):
                    messages.error(request, 'Please enter a valid 10-digit phone number starting with 7,8 or 9.')
                    return redirect('user_register')
                
                else:
                    
                    message = generate_otp()
                    sender_email = "gamersgt84@gmail.com"
                    receiver_mail = email
                    password_email = "omleyluxnmmdxpnp"
                    try:
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(sender_email, password_email)
                            server.sendmail(sender_email, receiver_mail, message)
                    except smtplib.SMTPAuthenticationError:
                            messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                            return redirect('user_register')
                    
                    user = Customuser.objects.create_user(
                        first_name = firstname,
                        last_name = lastname,
                        username = username,
                        email = email,
                        phone_number = phone_number,
                        user_bio = user_bio,
                        refferal = generate_referral_code(),
                        password = password1 )
                    
                    user.save()

                    if refferal_code:
                        referrer = Customuser.objects.get(refferal = refferal_code)
                        if referrer:
                                Wallet.objects.create(
                                    user=referrer,
                                    status = 'referal',
                                    amount = 100
                                )
                        else:
                            message.info(request, 'Incorrect refferal code')
                    
                        
                    request.session['email'] =  email
                    request.session['otp']   =  message
                    messages.success(request,'OTP is sent to your email')
                    return redirect('verify')
                
            except ValidationError as e:
                messages.error(request, f'Invalid email address: {e}')
                return redirect('user_register')

            except IntegrityError:
                messages.error(request, 'An internal error occurred. Please try again.')
                return redirect('user_register')

            except smtplib.SMTPException:
                messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                return redirect('user_register')

        return render(request, 'auth_app/user_register.html')


# Forgot Password

def for_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.info(request, 'Please Enter the email')
            return redirect()
        if  Customuser.objects.filter(email = email).exists():
            if not validate_email(email):
                messages.error(request, 'Please enter a valid email address.')
                return redirect('for_password')
            else:
                message = generate_otp()
                sender_email = "gamersgt84@gmail.com"
                receiver_mail = email
                password_email = "omleyluxnmmdxpnp"
                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, password_email)
                        server.sendmail(sender_email, receiver_mail, message)
                except smtplib.SMTPAuthenticationError:
                    messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                    return redirect('for_password')       
                request.session['email'] =  email
                request.session['otp']   =  message
                messages.success(request,'OTP is sent to your email')
                return redirect('reset_check')     
    return render(request, 'auth_app/forgot_password.html')
            

# forgot verify password

def for_verify_signup(request):
    context = {
        'messages': messages.get_messages(request)
    }
    try:
        if request.method == "POST":
            user      = Customuser.objects.get(email=request.session['email'])
            x         =  request.session.get('otp')
            OTP       =  request.POST['otp']     
            if OTP == x:
                user.is_verified = True
                del request.session['otp']        
                messages.success(request, "verify Successfully!")
                return redirect('reset_password')
            else:
                messages.info(request,"invalid otp")
                del request.session['email']
                del request.session['otp']
                return redirect('/')
    except ObjectDoesNotExist:
        messages.error(request, 'User not found. Please retry the registration process.')
        return redirect('/')

    except Exception as e:
        messages.error(request, f'An error occurred during verification: {str(e)}')
        return redirect('/')

    return render(request,'auth_app/for_verify_otp.html',context)


# Change password

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('email')
            try:
                customer = Customuser.objects.get(email=email)
                customer.set_password(new_password)
                customer.save()
                del request.session['email'] 
                messages.success(request, 'Password reset successful. Please login with your new password.')
                return redirect('/')
            except Customuser.DoesNotExist:
                messages.error(request, 'Failed to reset password. Please try again later.')
                return redirect('/')
        else:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('reset_password')
       
    else:
        return render(request, 'auth_app/reset_password.html')


# Verify OTP function

def verify_signup(request):
    context = {
        'messages': messages.get_messages(request)
    }
    try:
        if request.method == "POST":
            user      = Customuser.objects.get(email=request.session['email'])
            x         =  request.session.get('otp')
            OTP       =  request.POST['otp']     
            if OTP == x:
                user.is_verified = True
                user.save()
                del request.session['email'] 
                del request.session['otp']        
                login(request,user)
                messages.success(request, "Signup successful!")
                return redirect('/')
            else:
                user.delete()
                messages.info(request,"invalid otp")
                del request.session['email']
                return redirect('/')
    except ObjectDoesNotExist:
        messages.error(request, 'User not found. Please retry the registration process.')
        return redirect('/')

    except Exception as e:
        messages.error(request, f'An error occurred during verification: {str(e)}')
        return redirect('/')

    return render(request,'auth_app/verify_otp.html',context)

# Generate OTP function

def generate_otp(length = 6):
    return ''.join(secrets.choice("0123456789") for i in range(length))




# Email Vaildate function 


def validate_email(email):
    return '@' in email and '.' in email




# User Login



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache                
def user_login(request):
        if 'username' in request.session:
            return redirect('user_home')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not (username and password):
                 messages.info(request, 'username and password is not required')
            else:
                user = Customuser.objects.filter(username=username).first()
                if user is None:
                    messages.info(request, "Incorrect User")
                else:
                    if not user.check_password(password):
                        messages.info(request, 'Incorrect Password')
                    else:
                        if user.is_active:
                            login(request,user)
                            request.session['username'] = username
                            return redirect('user_home')
                        else:
                            messages.info(request, "Inactive user")
        return render(request, 'auth_app/user_login.html')



# Logout User


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
        logout(request)
        return redirect('/')
    

# Password changing
def password_change(request):
    if 'username' in request.session:
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            user = request.user
            if not user.check_password(old_password):
                messages.info(request, 'Incorrect old password')
                return redirect('password_change')
            if  password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect('password_success')
            else:
                messages.info(request, 'Conform password not matched')
        
        return render(request, 'auth_app/password_changing.html')
    else:
        return redirect('/')

# success
 
def password_success(request):
    return render(request,'auth_app/success.html')


# return login


def return_login(request):
    request.session.flush()
    return render(request, 'auth_app/user_login.html')

# Generate referral code

def generate_referral_code():
    letters = string.ascii_letters + string.digits
    referral_code = ''.join(random.choice(letters) for i in range(10))
    return referral_code

# product list

def productlist_ajax(request):
    products=Product.objects.filter(status=0).values_list('name',flat=True)
    productslist=list(products)
    return JsonResponse(productslist,safe=False)


# search products

def searchproduct(request):
    if 'username' in request.session:
        if request.method == 'POST':
            searchedterm=request.POST.get('productsearch')
            if searchedterm == " ":
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                product=Product.objects.filter(name__icontains=searchedterm).first()
            
                if product:
                    redirect_url = reverse("user_product_view", args=[product.catagory.main_category.id, product.catagory.id, product.id])
                    print(redirect_url)
                    return redirect(redirect_url)
                else:
                    messages.info(request,"No Product Matched Your Searchlist")
                    return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')












