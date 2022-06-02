from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save

from account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self): return f'{self.name}'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)


@receiver(post_save, sender=Category)
def product_post_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class Post(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts', null=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self): return f'{self.owner} - {self.name}'


class Mark():
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    marks = ((one, 'Очень плохо'), (two, 'Плохо'), (three, 'Нормально'), (four, 'Хорошо'), (five, 'Прекрасно'),)


class Rating(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    forum = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    mark = models.PositiveSmallIntegerField(choices=Mark.marks)

    def __str__(self) -> str:
        return f'{self.mark}-> {self.forum}'

    class Meta:
        unique_together = ('owner', 'forum')


class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.post} -> {self.created_at}'


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['post', 'user']