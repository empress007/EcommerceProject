from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from products.models import Product

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('This Email Field Must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email





# Managing Orders 
# models.py

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


    












































# from django.db import models
# from products.models import Product  # Importing the Product model from the products app
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# # Custom User Manager
# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#         return self.create_user(email, username, password, **extra_fields)



# # Custom User Model
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email
    

# # Order Model
# class Order(models.Model):
#     customer = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, blank=True,
#         related_name="orders", related_query_name="order"
#     )
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=True)
#     transaction_id = models.CharField(max_length=100, null=True)
    
#     def __str__(self):
#         return str(self.id)
    
#     @property
#     def get_cart_total(self):
#         return sum(item.get_total for item in self.order_items.all())

#     @property
#     def get_cart_items(self):
#         return sum(item.quantity for item in self.order_items.all())


# # OrderItem Model
# class OrderItem(models.Model):
#     product = models.ForeignKey(
#         Product, on_delete=models.SET_NULL, null=True,
#         related_name="order_items", related_query_name="order_item_product"
#     )
#     order = models.ForeignKey(
#         Order, on_delete=models.SET_NULL, null=True,
#         related_name="order_items", related_query_name="order_item_order"
#     )
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     @property
#     def get_total(self):
#         return self.product.price * self.quantity


# # ShippingAddress Model
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, blank=True,
#         related_name="shipping_addresses", related_query_name="shipping_address_customer"
#     )
#     order = models.ForeignKey(
#         Order, on_delete=models.SET_NULL, null=True,
#         related_name="shipping_addresses", related_query_name="shipping_address_order"
#     )
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     zipcode = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.address




