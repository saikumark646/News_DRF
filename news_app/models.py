from django.db import models

# Create your models here.


class Journalist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biodeta = models.TextField(blank=True)

    def __str__(self):
        return f' {self.first_name} {self.last_name} '


class Article(models.Model):
    author = models.ForeignKey(
        Journalist, related_name='articals', on_delete=models.CASCADE)
    # if created Forenkey model later db must be deleted.
    #author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    body = models.TextField()
    published = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author} {self.title}'
