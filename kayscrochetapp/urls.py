from django.urls import path

from . import views
app_name = 'kayscrochetapp'
urlpatterns = [
    # ex: /kayscrochetapp/
    path("", views.index, name="index"),
    # ex: /kayscrochetapp/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /kayscrochetapp/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /kayscrochetapp/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
