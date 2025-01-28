from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.forms import ProductForm
from .models import *
# Create your views here.



# CRUD
# create/upload product
@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user #Associate product with logged-in user
            product.save()
            messages.success(request, "Product upload successfully!")
            return redirect('index')  # Replace with your desired redirect URL
    else:
        form = ProductForm()
    return render(request, 'pages/product-page/upload-product.html',{'form':form})


# List Products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'pages/product-page/product-list.html',{'products':products})

# Update Product
# @login_required
def product_update(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')  
    else:
        form = ProductForm(instance=product)
    return render(request, 'pages/product-page/product-update.html',{'form':form})

# Delete Product
@login_required
def product_delete(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
         product.delete()
         return redirect('product-list') 
    return render(request, 'pages/product-page/product-confirm-delete.html',{'product':product})

