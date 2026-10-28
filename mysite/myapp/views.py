from django.shortcuts import render
import requests
from .models import Movie
from django.shortcuts import get_object_or_404, redirect
from .forms import MovieForm


# Create your views here.

def home(request):
    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&type=movie")
    results_json = response.json()
    movies = results_json["Search"]
    context = {
        "movies": movies
    }
    return render(request, "index.html", context)


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})


def movie_create(request):
    form = MovieForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("movie_list")
    return render(request, "movie_form.html", {"form": form, "is_update": False})


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.POST or None, instance=movie)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("movie_list")
    return render(
        request,
        "movie_form.html",
        {"form": form, "is_update": True, "movie": movie},
    )


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        movie.delete()
        return redirect("movie_list")
    return render(request, "movie_confirm_delete.html", {"movie": movie})