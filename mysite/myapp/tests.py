from django.test import TestCase
from django.urls import reverse

from .models import Movie


class MovieCrudTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Filme original",
            description="Descrição original",
            image_url="https://example.com/original.jpg",
        )

    def test_catalog_displays_movies_and_crud_actions(self):
        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)
        self.assertContains(
            response, reverse("movie_update", args=[self.movie.pk])
        )
        self.assertContains(
            response, reverse("movie_delete", args=[self.movie.pk])
        )
        self.assertContains(response, reverse("movie_create"))

    def test_create_movie(self):
        response = self.client.post(
            reverse("movie_create"),
            {
                "title": "Novo filme",
                "description": "Uma descrição",
                "image_url": "https://example.com/novo.jpg",
            },
        )

        self.assertRedirects(response, reverse("movie_list"))
        self.assertTrue(Movie.objects.filter(title="Novo filme").exists())

    def test_create_movie_with_invalid_data_shows_errors(self):
        response = self.client.post(
            reverse("movie_create"),
            {"title": "", "description": "Uma descrição", "image_url": "inválida"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertEqual(Movie.objects.count(), 1)

    def test_update_movie(self):
        response = self.client.post(
            reverse("movie_update", args=[self.movie.pk]),
            {
                "title": "Filme atualizado",
                "description": "Nova descrição",
                "image_url": "https://example.com/atualizado.jpg",
            },
        )

        self.assertRedirects(response, reverse("movie_list"))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Filme atualizado")

    def test_delete_requires_confirmation_and_post(self):
        delete_url = reverse("movie_delete", args=[self.movie.pk])

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movie.objects.filter(pk=self.movie.pk).exists())

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("movie_list"))
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())
