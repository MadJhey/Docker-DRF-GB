
# from mixer.backend.django import mixer
import math
from .models import Author, Book
from .views import AuthorModelViewSet

import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import force_authenticate,  APIRequestFactory, APIClient, APISimpleTestCase, APITestCase
from django.contrib.auth.models import User
from mixer.backend.django import mixer


class TestAuthorViewSet(TestCase):
    #  APIRequestFactory()
    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('api/authors/')
        view = AuthorModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_guest(self):
        factory = APIRequestFactory()
        request = factory.post(
            '/api/authors/', {'first_name': 'Грин', 'last_name': '123', 'birthday_year': 1880}, format='json')
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_admin(self):
        factory = APIRequestFactory()
        request = factory.post('/api/authors/', {'name': 'Пушкин',
                                                 'birthday_year': 1799}, format='json')
        admin = User.objects.create_superuser('admin', 'admin@admin.com',
                                              'admin123456')
        force_authenticate(request, admin)
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#   ApiClient

    def test_get_detail(self):
        author = Author.objects.create(birthday_year=1799)
        client = APIClient()
        response = client.get(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_admin(self):
        author = Author.objects.create(first_name='Пушкин', birthday_year=1799)
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@admin.com',
                                              'admin123456')
        client.login(username='admin', password='admin123456')
        response = client.put(f'/api/authors/{author.id}/', {
                              'first_name':      'Грин', 'last_name': '123', 'birthday_year': 1880})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author = Author.objects.get(id=author.id)
        self.assertEqual(author.first_name, 'Грин')
        self.assertEqual(author.birthday_year, 1880)
        client.logout()

# APISimpleTestCase


class TestMath(APISimpleTestCase):
    def test_sqrt(self):
        self.assertEqual(math.sqrt(4), 2)

# APITestCase


class TestBookViewSet(APITestCase):
    def test_get_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_admin(self):
        author = Author.objects.create(first_name='Пушкин', birthday_year=1799)
        book = Book.objects.create(name='Пиковая дама')
        book.author.add(author)
        book.save()
        admin = User.objects.create_superuser('admin', 'admin@admin.com',
                                              'admin123456')
        self.client.login(username='admin', password='admin123456')
        response = self.client.put(
            f'/api/books/{book.pk}/', {'name': 'Руслан и Людмила', 'author': author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(pk=book.id)
        self.assertEqual(book.name, 'Руслан и Людмила')

    def test_edit_admin_by_mixer(self):
        book = mixer.blend(Book)
        admin = User.objects.create_superuser('admin', 'admin@admin.com',
                                              'admin123456')
        self.client.login(username='admin', password='admin123456')
        response = self.client.put(
            f'/api/books/{book.pk}/', {'name': 'Руслан и Людмила', 'author': book.author__id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(pk=book.id)
        self.assertEqual(book.name, 'Руслан и Людмила')
