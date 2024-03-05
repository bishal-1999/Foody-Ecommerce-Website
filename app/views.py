# import all necessary modules

from django.views import View
from django.db.models import Q
from django.contrib.auth import *
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .models import Customer, Product, Cart, OrderPlaced
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.shortcuts import HttpResponse,HttpResponseRedirect,render, redirect


#######################################################################################################################################################

def home(request):
    return render(request,'homepage/index.html')

#######################################################################################################################################################

class ProductView(View):
	def get(self, request):
		totalitem = 0
		all_products = Product.objects.all()
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'app/home.html', { 'all_products':all_products,'totalitem':totalitem})

#######################################################################################################################################################

class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


#######################################################################################################################################################

@login_required()
def add_to_cart(request):
	user = request.user
	item_already_in_cart1 = False
	product = request.GET.get('prod_id')
	item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
	if item_already_in_cart1 == False:
		product_title = Product.objects.get(id=product)
		Cart(user=user, product=product_title).save()
		messages.success(request, 'Product Added to Cart Successfully !!' )
		return redirect('/cart')
	else:
		return redirect('/cart')

#######################################################################################################################################################

@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'app/emptycart.html', {'totalitem':totalitem})


#######################################################################################################################################################

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

#######################################################################################################################################################

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


#######################################################################################################################################################

@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})

#######################################################################################################################################################

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		cid.delete()
	return redirect("orders")

#######################################################################################################################################################

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


#######################################################################################################################################################

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

#######################################################################################################################################################

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'app/orders.html', {'order_placed':op})

#######################################################################################################################################################

def fruits(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			fruits = Product.objects.filter(category='f')
	return render(request, 'app/fruits.html', {'fruits':fruits, 'totalitem':totalitem})


#######################################################################################################################################################

def bakery(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			bakery = Product.objects.filter(category='b')
	return render(request, 'app/bakery.html', {'bakery':bakery, 'totalitem':totalitem})


#######################################################################################################################################################


def dairy_products(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
		dairy_products = Product.objects.filter(category='d')
	return render(request, 'app/dairy_products.html', {'dairy_products':dairy_products,'totalitem':totalitem})


#######################################################################################################################################################

def vegetables(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			vegetables = Product.objects.filter(category='v')
	return render(request, 'app/vegetables.html', {'vegetables':vegetables, 'totalitem':totalitem})


#######################################################################################################################################################

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})

#######################################################################################################################################################

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})


#######################################################################################################################################################

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

#######################################################################################################################################################

from django.db.models import Q

def search_items(data):
    # Case-insensitive search for products whose title contains the search term
    found_products = Product.objects.filter(
        Q(title__icontains=data)
    )
    return found_products



def search_products(request):
    if request.method == "POST":
        data = request.POST.get('data')
        if data:
            if any(keyword in data.lower() for keyword in ['fruits', 'fru']):
                return redirect('fruits')  
            elif any(keyword in data.lower() for keyword in ['vegetables', 'veg']):
                return redirect('vegetables')  
            elif any(keyword in data.lower() for keyword in ['bakery', 'bak']):
                return redirect('bakery')
            elif any(keyword in data.lower() for keyword in ['dairy', 'd']):
                return redirect('dairy')  
            else:
                found_products = search_items(data)
                if found_products:
                    return render(request, 'app/home.html', {'all_products': found_products, 'totalitem': len(found_products)})
                else:
                    messages.info(request, "Sorry! Product is not available.")
                    return render(request, 'app/home.html')
    return redirect('products')

#####################################################################################################################################################

