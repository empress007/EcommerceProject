from django.urls import path
from . import views
# django's default logout
# from django.contrib.auth.views import LogoutView
# from django.contrib.auth.views import LoginView
# from django.urls import path
# from .views import (
#     CustomPasswordResetView,
#     CustomPasswordResetDoneView,
#     CustomPasswordResetConfirmView,
#     CustomPasswordResetCompleteView,
# )
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from django.contrib.auth import views as auth_views



urlpatterns = [
    path("",views.home, name ="index"),
    path("shop",views.shop_grid, name ="shop-grid"),
    path("blog",views.blog, name ="blog"),
    path("contact",views.contact, name ="contact"),
    path("cart/", views.cart, name='cart'),
    path("add-to-cart/<int:product_id>/",views.add_to_cart, name='add_to_cart'),
    path("remove-from-cart/<int:pk>/",views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
        # authentication
    path("login/", views.CustomLoginView.as_view(), name='login'),
    # path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("sign-up/", views.register, name="sign-up"),
    
    # '''Modified password reset functions
    
    
     
    path("password-reset/", PasswordResetView.as_view(template_name='registration/password_reset.html', email_template_name='registration/password_reset_email.html'), name='password_reset',),
    # """Modified password reset functionality""",
    # path("password-reset/", views.CustomPasswordResetView.as_view(), name='password_reset'),
    path("password-reset/done/", PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    

    
    # path("password_reset/", auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',email_template_name='registration/password_reset_email.html'), name='password_reset'),
    # path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    # path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    # path("password_reset_complete", auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
