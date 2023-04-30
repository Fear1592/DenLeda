from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Author, Book
from .permissions import IsOwnerOrIsAuthenticatedReadOnly, IsAuthorOrIsAuthenticatedReadOnly
from .serializers import AuthorDetailSerializer, BookDetailSerializer


class AuthorCreateView(generics.CreateAPIView):
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsAuthenticated, )
    '''
    Переопределил фунцию perform create для автоматической привязки 
    АВТОРИЗОВАННОГО пользователя который на данный момент создаёт себе Автора.
    '''

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AuthorUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsOwnerOrIsAuthenticatedReadOnly,)

    '''
        В данном классе мы можем ПРОСМАТРИВАТЬ/ИЗМЕНЯТЬ/УДАЛЯТЬ авторов.
    '''


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthenticated,)
    '''
        Переопределил фунцию perform create для автоматической привязки 
        для автоматического заполнения поля author текущим АВТОРИЗОВАННЫМ ПОЛЬЗОВАТЕМ!.
    '''

    def perform_create(self, serializer):
        user = self.request.user
        author = Author.objects.get(user=user)

        serializer.save(author=author)


class BookDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthorOrIsAuthenticatedReadOnly,)

    '''
        В данном классе мы можем ПРОСМАТРИВАТЬ/ИЗМЕНЯТЬ/УДАЛЯТЬ книги.
    '''
