from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='42_home'),
    path('save_pwd', views.save_pwd, name='save_pwd'),
    path('index/<username>', views.index, name='42_index'),
    path('share_me/prod_cat/<username>', views.prod_cat, name='prod_cat'),
    path('purchase/<prod_pk>/<username>', views.purchase, name='purchase'),
    path('share_me/top_up/<username>', views.top_up, name='top_up'),
    path('share_me/add_prod/<username>', views.add_prod, name='add_prod'),
    path('share_me/receivables/<username>', views.receivables, name='receivables')
]