from rest_framework import serializers
from .models import Author, Book


class AuthorDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, )
    """
    Сериализот для создания/изминения информации у автора.
    Поле user - заполняется автоматически в views.py
    """

    class Meta:
        model = Author
        fields = ['id', 'user', 'first_name', 'last_name', 'date_of_birth']



class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer(read_only=True, )
    """
    Сериализот для создания/изминения информации у Книги.
    Поле автор - заполняется автоматически в views.py
    Передан селизатор Автора, чтобы была видно вся информация о нём.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'date_of_publication']