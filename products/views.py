from django.shortcuts import render,redirect, reverse
from .models import Product, Image, Review
from . forms import ProductForm, ImageForm
from games.models import Games
from main_category_app.models import Main_category
from django.http import JsonResponse
# Create your views here.

# View Games

def products_view(request):
        if 'admin' in request.session:
            pr = Product.objects.all()
            context={'pr' : pr}
            return render(request, 'products/products_view.html', context )
        else:
              return redirect('admin')




# Add  Games

def products_add(request):
        if 'admin' in request.session:
            form = ProductForm()
            if request.method == "POST":
                  form = ProductForm(request.POST, request.FILES)
                  if form.is_valid():
                        form.save()
                  return redirect('products_view')
            context = {'form' : form}
            return render(request, 'products/add_products.html', context)
        else:
              return redirect('admin')
    


# Update Games

def products_update(request, pid):
        if 'admin' in request.session:
            val = Product.objects.get(id = pid)
            form = ProductForm(instance = val)
            if request.method == "POST":
                  form = ProductForm(request.POST, request.FILES, instance=val)
                  if form.is_valid():
                        form.save()
                        return redirect('products_view')    
            context = {'form' : form}     
            return render(request, 'products/update_products.html', context)
        else:
              return redirect('admin')
     
    
# Delete Games
     

def products_delete(request, pid):
        if 'admin' in request.session:
            cat = Product.objects.filter(id = pid)
            cat.delete()
            return redirect('products_view')
        else:
              return redirect('admin')


# Add Product images

def image_add(request):
        if 'admin' in request.session:
            form = ImageForm()
            if request.method == "POST":
                  form = ImageForm(request.POST, request.FILES)
                  if form.is_valid():
                        form.save()
                  return redirect('products_view')
            context = {'form' : form}
            return render(request, 'products/add_image.html', context)
        else:
              return redirect('admin')



# View Images

def image_view(request, pid):
      if 'admin' in request.session:
            if(Product.objects.filter(id = pid)):
                  val = Image.objects.filter(product__id = pid)
            context = {'val' : val}
            return render(request, 'products/view_images.html', context)
      else:
            return redirect('admin')


# Delete Image


def image_delete(request, pid):
      if 'admin' in request.session:
            v = Image.objects.get(id = pid)   
            val = Image.objects.filter(product__id = v.product.id)
            v.delete()
            context = {'val' : val}
            return render(request, 'products/view_images.html', context)
      else:
            return redirect('admin')



# User Products View


def user_products_view(request, pid):
      if 'username' in request.session:
            filter=Games.objects.all()
            if (Games.objects.filter(id = pid)):
                  cat=Games.objects.get(id = pid)
                  print(cat)
                  pro = Product.objects.filter(catagory__id = pid)
                  context = {'pro':pro,
                        'filter':filter,
                        'cat':cat}
                  return render(request, 'products/user_products.html', context)
            else:
                  return redirect('user_games_view')
      else:
            return redirect('/')


# User Product View
      

def user_product_view(request, mid, gid, pid):
      if 'username' in request.session:
            if (Main_category.objects.filter(id = mid)):
                  if (Games.objects.filter(id = gid)):
                        if (Product.objects.filter(id = pid)):
                              img = Image.objects.filter(product__id = pid)[:4]
                              pro = Product.objects.get(id = pid)
                              gro = Product.objects.filter(catagory__id = gid)
                              Totel=0
                              offer = None
                              if pro.catagory.main_category.category_offer:
                                    offer = pro.catagory.main_category.category_offer
                                    Totel = pro.orginal_price-(offer*pro.orginal_price //100)
                                    if pro.product_offer:
                                          if offer < pro.product_offer:
                                                offer = pro.product_offer
                                                Totel = pro.orginal_price-(offer*pro.orginal_price //100)
                                          else:
                                                Totel = pro.orginal_price-(offer*pro.orginal_price //100)
                              elif pro.product_offer:
                                    offer = pro.product_offer
                                    Totel=pro.orginal_price-(offer*pro.orginal_price //100)
                              else:
                                    Totel=pro.orginal_price  

                              review=Review.objects.filter(product__id=pid).order_by('-created_at')[:4]
                              reviews=Review.objects.filter(product__id=pid)
                              totel_val=0
                              rating_val=0
                              rating = 0
                              for re in reviews:
                              
                                    totel_val=totel_val+re.review_rating
                                    rating_val=rating_val+1
                              if rating_val != 0:
                                    rating=totel_val//rating_val
                              else:
                                    rating=0

                              context = { 'pro':pro ,
                                          'img' :img,
                                          'gro':gro,
                                          'offer':offer,
                                          'Totel':Totel,
                                          'review':review,
                                          'rating':rating}
                        
                              return render(request, 'products/main_product.html', context)
                        else:
                              return redirect('user_products_view')
                  else:
                        return redirect('user_products_view')
            else:
                  return redirect('user_products_view')
      else:
            return redirect('/')
      


# Search product
      
def search_products(request):
        if 'admin' in request.session:
            if request.method == 'POST':
                  quarey = request.POST.get('q')
                  pr = Product.objects.filter(name__icontains=quarey)
            context={'pr' : pr}
            return render(request, 'products/products_view.html', context )
        else:
              return redirect('admin')




# Add review

def add_review(request):
      if 'username' in request.session:
            if request.method == 'GET':
                  prod_id = request.GET.get('pro_id')
                  product = Product.objects.get(id = prod_id)
                  review_text = request.GET.get('comment')
                  review_rating = request.GET.get('rate')
                  user = request.user
                  Review.objects.create(user = user,
                        product = product,
                        review_text = review_text,
                        review_rating = review_rating)
                  redirect_url = reverse("user_product_view", args=[product.catagory.main_category.id, product.catagory.id, product.id])
                  return redirect(redirect_url)
      else:
            return redirect('/')      

#filter price range
      

def products_price(request, pid, low_price, high_price):
    if 'username' in request.session:
      filter=Games.objects.all()
      cat=Games.objects.get(id = pid)
      pro = Product.objects.filter(catagory__id = pid,orginal_price__range=(low_price, high_price))
      context = {'pro':pro,
                  'cat':cat,
                  'filter':filter}
      return render(request, 'products/user_products.html', context)
    else:
          return redirect('/')
            

# max to min

def max_to_min(request, pid):
    if 'username' in request.session:
      filter=Games.objects.all()
      cat=Games.objects.get(id = pid)
      pro = Product.objects.filter(catagory__id = pid).order_by('-orginal_price')
      context={
            'pro':pro,
            'cat':cat,
            'filter':filter
      }
      return render(request, 'products/user_products.html', context)
    else:
          return redirect('/')


# min to max

def min_to_max(request, pid):
    if 'username' in request.session:
      filter=Games.objects.all()
      cat=Games.objects.get(id = pid)
      pro = Product.objects.filter(catagory__id = pid).order_by('orginal_price')
      context={
            'pro':pro,
            'cat':cat,
            'filter':filter
      }
      return render(request, 'products/user_products.html', context)
    else:
          return redirect('/')



      

