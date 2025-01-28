from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout 
from django.shortcuts import render, redirect,  HttpResponse,get_object_or_404
from products.models import Product,Category
from .forms import UserRegistrationForm, CustomLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
# from django.contrib.auth import 
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from users.models import User,Product, Order,OrderItem  # Ensure this line exists
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
# from django.views.generic import View
# from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Authentication proceeds 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account successfully created.")
            login(request, user)
            return redirect('login')  # Redirect to the homepage
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})




# class CustomLoginView(FormView):
#     template_name = 'registration/login.html'
#     form_class = AuthenticationForm

#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return redirect(self.request.GET.get('next', '/'))

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
        
        
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('index') #Redirect to the homepage after login
    


# from django.shortcuts import redirect

# def CustomLoginView(request):
#     if request.method == "POST":
#         # Handle login logic
#         if next_url := request.GET.get('next'):
#             return redirect(next_url)
#         return redirect('index')  # Default redirect
#     return render(request, 'login.html')

    
        # Logout View
def logout_view(request):
    logout(request)
    return redirect('login')




class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    # success_url = reverse_lazy('password_reset/done/')  # Redirect to "password reset done" page
    success_url = '/password-reset/done/'  # Redirect to "password reset done" page

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            # If the email is not registered, render a custom template
            return render(self.request, 'registration/email_not_found.html', {'email': email})
        return super().form_valid(form)


    
# class CustomPasswordResetView(View):
#     def get(self, request):
#         form = PasswordResetForm()
#         # return render(request, 'password_reset_form.html', {'form': form})
#         return render(request, 'registration/password_reset_email.html', {'form': form})

#     def post(self, request):
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'registration/password_reset_done.html')
#         return render(request, 'registration/password_reset_email.html', {'form': form})




class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_message"] = "If the email is valid, you'll receive a password reset link shortly."
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')  # Redirect to "password reset complete" page

    def form_valid(self, form):
        # You can add custom logic here if needed
        return super().form_valid(form)
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

   
#  pages view

def home(request):
    category = Category.objects.all()
    products = Product.objects.all()
    context = {
        "products":products,
        "category":category
    }
    
    return render(request, "pages/index.html", context)


# class CustomPasswordResetView(View):
#     def post(self, request):
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'password_reset_done.html')
#         return render(request, 'password_reset_form.html', {'form': form})

# def home(request):
#     # return HttpResponse("Hello World! My E-commerce project kicks-off----")
#     return render(request, "pages/index.html")

# def cart(request):
#     user = request.user
#     order = Order.objects.filter(customer=user, complete=False).first()
#     context = {'order': order}
#     return render(request, 'cart.html', context)



def add_to_cart(request, product_id,):
    '''
    Add to cart
    '''
    product = get_object_or_404 (Product, id=product_id)
    user = request.user if request.user.is_authenticated else None
    order, created =  Order.objects.get_or_create(customer=user, complete=False)
    
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1 
    order_item.save()
    
    return redirect(request.META.get('HTTP REFERER', "/"))
 
# def add_to_cart(request, product_id):
    
#     '''
#     Add to cart
#     '''
#     product = get_object_or_404 (Product, id=product_id)
#     user = request.user if request.user.is_authenticated else None
#     order, created =  Order.objects.get_or_create(customer=user, complete=False)
    
#     order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#     order_item.quantity += 1 
#     order_item.save()   
#     # If AJAX request, return JSON response
#     if request.headers.get("X-Requested-With") == 'XMLHttpRequest':
#         return JsonResponse({
#         'cart_itens': order.get_cart_items,
#         'cart_total': order.get cart_total,
#         })
#     return redirect(request.META.get('HTTP REFERER', "home"))



def remove_from_cart (request, pk):
    user = request.user
    order = Order.objects.filter(customer=user, couplete=False).first()
    if order:
        order_item  = get_object_or_404(OrderItem, pk=pk, order=order)
        order_item.delete()
    return redirect("cart") #Redirect to the checkout page or cart page


def cart(request):
    user = request.user if request.user.is_authenticated else None 
    order =  Order.objects.filter(customer=user, complete=False).first()
    items =order.orderitem_set.all() if order else []
    
    context = {
        'items': items,
        'order': order,
    }
    return render (request, 'pages/cart.html', context)
import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from paystackapi.transaction import Transaction

def checkout(request):
    order = Order.objects.filter(customer=request.user, complete=False).first()
    if request.method == "POST":
        transaction_ref = str(uuid.uuid4())  # Generate a unique transaction reference
        amount = int(order.get_cart_total * 100)  # Amount in kobo/cents

        # Pass transaction data to Paystack
        response = Transaction.initialize(
            reference=transaction_ref,
            email=request.user.email,
            amount=amount,
            callback_url=request.build_absolute_uri('/verify-payment/'),
        )
        return redirect(response['data']['authorization_url'])  # Redirect to Paystack

    items = order.orderitem_set.all()
    context = {
        'items': items,
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)


from django.http import JsonResponse
from paystackapi.transaction import Transaction

def verify_payment(request):
    reference = request.GET.get('reference')
    response = Transaction.verify(reference=reference)
    if response['status'] == True:
        # Update the order to complete
        order = Order.objects.get(transaction_id=reference)
        order.complete = True
        order.save()

        return JsonResponse({'status': 'success', 'message': 'Payment successful!'})
    return JsonResponse({'status': 'failure', 'message': 'Payment failed. Please try again.'})




def shop_grid(request):
    return render(request, "pages/shop-grid.html")

def blog(request):
    return render(request, "pages/blog.html")

def contact(request):
    return render(request, "pages/contact.html")




  

  
  
  
  
# class CustomPasswordRestView(PasswordResetView):
#     template_name = 'registration/password_reset.html'
#     email_template_name = 'registration/password_reset_email.html'
#     success_url = '/password-reset/done/'
    
#     def form_valid(self, form):
#         email = form.cleaned.data.get('email')
#         if not User.objects.filter(email=email).exits():
#             # if the email is not registered, render a custom template
#             return render(self.request, 'registration/email_not_found.html', {'email': email})
#         return super().form_valid(form)
         
  
# class CustomPasswordResetView(View):
#     def get(self, request):
#         form = PasswordResetForm()
#         return render(request, 'registration/password_reset_email.html', {'form': form})

#     def post(self, request):
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             # Get the email address from the form
#             email = form.cleaned_data['email']
#             users = User.objects.filter(email=email)
            
#             for user in users:
#                 # Create uidb64 and token
#                 uidb64 = urlsafe_base64_encode(user.pk.encode())
#                 token = default_token_generator.make_token(user)

#                 # Send the email
#                 send_mail(
#                     'Password Reset Request',
#                     render_to_string('registration/password_reset_email.html', {
#                         'uidb64': uidb64,
#                         'token': token,
#                         'user': user,
#                         'domain': request.get_host(),
#                         'site_name': 'Your Site',
#                     }),
#                     'no-reply@yourdomain.com',
#                     [email],
#                 )
#             return render(request, 'registration/password_reset_done.html')
#         return render(request, 'registration/password_reset_email.html', {'form': form}) 
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

# from django.shortcuts import render,HttpResponse

# # Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.utils import timezone
# from django.urls import reverse
# from .models import *

# @login_required
# def Home(request):
#     return render(request, 'index.html')

# def RegisterView(request):

#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user_data_has_error = False

#         if User.objects.filter(username=username).exists():
#             user_data_has_error = True
#             messages.error(request, "Username already exists")

#         if User.objects.filter(email=email).exists():
#             user_data_has_error = True
#             messages.error(request, "Email already exists")

#         if len(password) < 5:
#             user_data_has_error = True
#             messages.error(request, "Password must be at least 5 characters")

#         if user_data_has_error:
#             return redirect('register')
#         else:
#             new_user = User.objects.create_user(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email, 
#                 username=username,
#                 password=password
#             )
#             messages.success(request, "Account created. Login now")
#             return redirect('login')

#     return render(request, 'register.html')

# def LoginView(request):

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             return redirect('home')
        
#         else:
#             messages.error(request, "Invalid login credentials")
#             return redirect('login')

#     return render(request, 'login.html')

# def LogoutView(request):

#     logout(request)

#     return redirect('login')

# def ForgotPassword(request):

#     if request.method == "POST":
#         email = request.POST.get('email')

#         try:
#             user = User.objects.get(email=email)

#             new_password_reset = PasswordReset(user=user)
#             new_password_reset.save()

#             password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

#             full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

#             email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
#             email_message = EmailMessage(
#                 'Reset your password', # email subject
#                 email_body,
#                 settings.EMAIL_HOST_USER, # email sender
#                 [email] # email  receiver 
#             )

#             email_message.fail_silently = True
#             email_message.send()

#             return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

#         except User.DoesNotExist:
#             messages.error(request, f"No user with email '{email}' found")
#             return redirect('forgot-password')

#     return render(request, 'forgot_password.html')

# def PasswordResetSent(request, reset_id):

#     if PasswordReset.objects.filter(reset_id=reset_id).exists():
#         return render(request, 'password_reset_sent.html')
#     else:
#         # redirect to forgot password page if code does not exist
#         messages.error(request, 'Invalid reset id')
#         return redirect('forgot-password')

# def ResetPassword(request, reset_id):

#     try:
#         password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

#         if request.method == "POST":
#             password = request.POST.get('password')
#             confirm_password = request.POST.get('confirm_password')

#             passwords_have_error = False

#             if password != confirm_password:
#                 passwords_have_error = True
#                 messages.error(request, 'Passwords do not match')

#             if len(password) < 5:
#                 passwords_have_error = True
#                 messages.error(request, 'Password must be at least 5 characters long')

#             expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

#             if timezone.now() > expiration_time:
#                 passwords_have_error = True
#                 messages.error(request, 'Reset link has expired')

#                 password_reset_id.delete()

#             if not passwords_have_error:
#                 user = password_reset_id.user
#                 user.set_password(password)
#                 user.save()

#                 password_reset_id.delete()

#                 messages.success(request, 'Password reset. Proceed to login')
#                 return redirect('login')
#             else:
#                 # redirect back to password reset page and display errors
#                 return redirect('reset-password', reset_id=reset_id)

    
#     except PasswordReset.DoesNotExist:
        
#         # redirect to forgot password page if code does not exist
#         messages.error(request, 'Invalid reset id')
#         return redirect('forgot-password')

#     return render(request, 'reset_password.html')




# class CustomPasswordResetView(View):
#     def post(self, request):
#         # Ensure PasswordResetForm uses the custom user model
#         User = get_user_model()  # Get the custom user model
#         form = PasswordResetForm(request.POST, user_model=User)  # Pass custom user model if needed
#         if form.is_valid():
#             form.save()
#             return render(request, 'password_reset_done.html')
#         return render(request, 'password_reset_form.html', {'form': form})





    
# class CustomPasswordResetView(View):
#     def get(self, request):
#         form = PasswordResetForm()
#         # return render(request, 'password_reset_form.html', {'form': form})
#         return render(request, 'registration/password_reset_email.html', {'form': form})

#     def post(self, request):
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'registration/password_reset_done.html')
#         return render(request, 'registration/password_reset_email.html', {'form': form})




