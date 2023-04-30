from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    date_of_birth = models.DateField('Дата рождения')

    ''''
    В экземпляре модели user  переданы отношение Один к ОДНОМУ.
    Сделано это для того чтобы, зарегестрированный пользователь
    мог публиковать книги под ОДНИМ автором а не несколькими.
    '''

    class Meta:
        ordering = ['id']
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.first_name


class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    description = models.TextField('Описание')
    date_of_publication = models.DateField('Дата публикации')
    """
    Дата публикации не заполняется автоматически т.к.
    Дата публикации поста и публиции книги могут отличаться.
    Поэтому автор создавая КНИГУ указывает самостоятельно когда была издана книга.
    Если же требуется именно дата публкиции ПОСТА о книге, в date_of_publication 
    добавляем поле auto_now = True - что позволит автоматически добавить текушую дату.
    """

    class Meta:
        ordering = ['id']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title