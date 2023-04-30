from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class UsersTests(APITestCase):

    def test_create_user(self):
        sample_user = {
            "email": "m@m.com",
            "username": "Lolo",
            "password": "potterlol1"
        }
        response = self.client.post('/api/auth/users/', sample_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual((response.data['username']), 'Lolo')
        self.assertEqual((response.data['email']), 'm@m.com')


class AuthorBookTest(APITestCase):
    def authenticate(self):
        self.client.post('/api/auth/users/', {
            "email": "m@m.com",
            "username": "Lolo",
            "password": "potterlol1"
        })
        response = self.client.post('/api/auth/token/login/', {
            "username": "Lolo",
            "password": "potterlol1"
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['auth_token']}")

    def test_should_create_author(self):
        previous_author_count = Author.objects.all().count()
        self.authenticate()
        sample_author = {
            "first_name": "Дядя",
            "last_name": "Лёша",
            "date_of_birth": "2012-04-28"
        }
        response = self.client.post('/api/author/', sample_author)
        self.assertEqual(Author.objects.all().count(), previous_author_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Дядя')
        self.assertEqual(response.data['last_name'], 'Лёша')
        self.assertEqual(response.data['date_of_birth'], '2012-04-28')

    def test_should_create_book(self):
        previous_book_count = Book.objects.all().count()
        self.authenticate()
        self.test_should_create_author()
        sample_book = {
            "title": "ГРАФ",
            "description": "Монте Кристо",
            "date_of_publication": "2012-04-28"
        }
        response = self.client.post('/api/books/', sample_book)
        self.assertEqual(Book.objects.all().count(), previous_book_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'ГРАФ')
        self.assertEqual(response.data['description'], 'Монте Кристо')
        self.assertEqual(response.data['date_of_publication'], '2012-04-28')

    def test_should_get_book(self):
        self.test_should_create_book()

        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_author(self):
        self.authenticate()
        self.test_should_create_author()
        get_author = Author.objects.get(first_name='Дядя')
        get_id = get_author.id

        sample_author = {
            "first_name": "Тётя",
            "last_name": "Мотя",
            "date_of_birth": "2012-04-28"
        }
        response = self.client.put(f'/api/author/{get_id}/', sample_author)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Тётя')
        self.assertEqual(response.data['last_name'], 'Мотя')
        self.assertEqual(response.data['date_of_birth'], '2012-04-28')

    def test_should_delete_author(self):
        self.authenticate()
        self.test_should_create_author()
        get_author = Author.objects.get(first_name='Дядя')
        get_id = get_author.id
        response = self.client.delete(f'/api/author/{get_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_update_book(self):
        self.test_should_create_book()
        get_book = Book.objects.get(title='ГРАФ')
        get_id = get_book.id

        sample_book = {
            "title": "Барон",
            "description": "Медич",
            "date_of_publication": "2012-04-22"
        }
        response = self.client.put(f'/api/books/{get_id}/', sample_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Барон')
        self.assertEqual(response.data['description'], 'Медич')
        self.assertEqual(response.data['date_of_publication'], '2012-04-22')

    def test_should_delete_book(self):
        self.test_should_create_book()
        get_book = Book.objects.get(title='ГРАФ')
        get_id = get_book.id

        response = self.client.delete(f'/api/books/{get_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
