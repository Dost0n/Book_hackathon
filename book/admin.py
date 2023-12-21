from django.contrib import admin
from book.models import Category, SubCategory, Country, Author, Book, BookComment, BookViews, LikeBook


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Country)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookViews)
admin.site.register(LikeBook)
admin.site.register(BookComment)