"""atm_simulation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from . import views

from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create-customer/', views.customer_creation, name='customer_creation'),
    path('start-atm-operation/', views.start_atm_operation, name='start_atm_operation'),
    path('atm-operations/<str:pin>/', views.atm_operations, name='atm_operations'),
    path('check-balance/<str:pin>/', views.check_balance, name='check_balance'),
    path('perform-another-transaction/', views.perform_another_trans, name='perform_another_trans'),
    path('change-pin/<str:pin>/', views.change_pin, name='change_pin'),
    path('button-operations/<str:pin>/<str:trans_type>/',
         views.button_operations, name='button_operations'),
    path('withdraw-operation/<str:pin>/<str:amt>', views.withdraw_operation, name='withdraw_operation'),
    path('collect-number/<str:pin>/<str:num_type>/<str:amt>', views.collect_number, name='collect_number'),
    path('send-money/<str:pin>/<str:num_type>/', views.send_money, name='send_money'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
