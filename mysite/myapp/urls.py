from django.urls import path

from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("filmes/novo/", views.movie_create, name="movie_create"),
    path("filmes/<int:pk>/editar/", views.movie_update, name="movie_update"),
    path("filmes/<int:pk>/deletar/", views.movie_delete, name="movie_delete"),
]
