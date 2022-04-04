from django.contrib import admin
from .models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'cover', 'available_borrow')

class BookBorrowedAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'date_borrow', 'date_return')
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('username', 'message', 'time')

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookBorrowed, BookBorrowedAdmin)
admin.site.register(Notification, NotificationAdmin)