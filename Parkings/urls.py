"""Parkings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from members import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("banned/", views.banned_view, name='banned_view'),
    path("logout/", views.logout_request, name= "logout"),
    path("create-listing/", views.create_listing),
    path("my-requests/", views.my_requests),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-requests/deleted", views.cancel_booking, name="cancel_booking"),
    path("chatbot/", views.chatbot, name="get_response"),
    path("chatbot/get-response/", views.bot_response, name="get_response"),
    path('stripe_checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path("reward-points/", views.reward_points),
    path("edit-listing/", views.edit_listing, name= 'edit-listing'),
    path('mes/', views.get_messages, name='mes'),
    path('admin_messages/', views.get_dm, name='admin_messages'),
    path('send_dm/', views.send_dm, name='send_dm'),
    path('get_dm/', views.get_dm, name='get_dm'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('report_msg/', views.report_view, name='report_msg'),
    path('del_report_msg/', views.del_report_view, name='del_report_msg'),
    path('ban_user/', views.ban_user, name='ban_user'),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-requests/deleted", views.cancel_booking, name="cancel_booking"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
