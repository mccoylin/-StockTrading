from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'tradingSystem'

urlpatterns = [
    path('', views.goto_login, name='goto_login'),
    path('mylogin', views.mylogin, name='mylogin'),
    path('base', views.base, name='base'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('stockdetails',views.stockdetails,name='stockdetails'),
    path('stock_info/<str:stock_id>/', views.stock_info, name='stock_info'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock_comment', views.stock_comment, name='stock_comment'),
    path('buy_in_stock', views.buy_in_stock, name='buy_in_stock'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('log_out', views.log_out, name='log_out'),
    path('do_register', views.do_register, name='do_register'),
    path('deal_user_change', views.deal_user_change, name='deal_user_change'),
    path('get_real_quotes',views.get_real_quotes,name = 'get_real_quotes')
]


