from django.urls import path
from . import views
from .views import add_to_cart, cart, remove_from_cart

app_name = 'kayscrochetapp'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:item_id>/like/", views.like, name="like"),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('cart', cart, name='cart'),
    path('<int:pk>/item/', add_to_cart, name='add_to_cart'),
    path('<int:item_id>/cart/remove/', remove_from_cart, name='remove_from_cart'),
]
