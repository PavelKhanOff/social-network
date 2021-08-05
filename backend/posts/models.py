from django.db import models

from users.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(verbose_name='Твой лучший текст!',
                            help_text='Пишите без ошибок')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True,
                              verbose_name='Изображение',
                              help_text='Изображение вашего поста.')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="favorite_subscriber", verbose_name='Пользователь')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="favorite_recipe",
        verbose_name='Пост')
    when_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
