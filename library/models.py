from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class Genre(models.Model):
    genre = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)", primary_key=True)
    def __str__(self):
        return self.genre

class Book(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    author = models.CharField(max_length=100, default=None)
    genre = models.ForeignKey('Genre', default=None, on_delete=models.CASCADE)
    cover = models.ImageField(default=None, null=False, upload_to='book_image')
    available_borrow = models.IntegerField(default = 1, validators = [MaxValueValidator(1), MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.title},{self.author},{self.genre},{self.cover}, {self.available_borrow}"

class BookBorrowed(models.Model):
    title = models.ForeignKey('Book', max_length=200, default=None, on_delete=models.CASCADE)
    username = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date_borrow = models.DateField(default=datetime.date.today())
    date_return = models.DateField(blank=True, default=None, null=True)

    def __str__(self):
        return f"{self.title},{self.username},{self.date_borrow},{self.date_return}"

class Notification(models.Model):
    username = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, help_text="Enter message for student...")
    time=models.DateField(default=datetime.date.today())

    def __str__(self):
        return f"{self.username},{self.message},{self.time}"
