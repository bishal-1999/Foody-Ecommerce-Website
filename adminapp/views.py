from django.shortcuts import render, redirect, get_object_or_404
from app.models import Product,OrderPlaced
from django.contrib import messages
from app.forms import ProductForm


####################################################################################################################################################################

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')  
    else:
        form = ProductForm()
    return render(request, 'adminapp/add_product.html', {'form': form})

####################################################################################################################################################################

def admin_panel(request):
    return render(request, 'adminapp/admin.html')

####################################################################################################################################################################

def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminapp/product_list.html', {'products': products})

####################################################################################################################################################################


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')
####################################################################################################################################################################

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Add success message
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminapp/update_product.html', {'form': form, 'product': product})

####################################################################################################################################################################

def order_list(request):
    orders = OrderPlaced.objects.all()
    return render(request, 'adminapp/order_list.html', {'orders': orders})

####################################################################################################################################################################

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = OrderPlaced.objects.get(pk=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('order_list')
    return render(request, 'adminapp/update_order_status.html', {'order_id': order_id})

####################################################################################################################################################################
