from django.db import models
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from config.models import BaseModel
from django.core.exceptions import ValidationError
from users.models import User
from django.db.models import UniqueConstraint


def validate_file(image):
    file_size = image.file.size
    if file_size > 2 * 429916160:
        raise ValidationError("Max size of file is %s 1GB")


INACTIVE, ACTIVE = ("inactive", 'active')
DRAFT, PUBLISHED = ("draft", 'published')


class Category(BaseModel):

    CATEGORY_STATUS = (
        (INACTIVE, INACTIVE),
        (ACTIVE, ACTIVE)
    )

    category_status = models.CharField(max_length=31, choices=CATEGORY_STATUS, default=INACTIVE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='subcategories')
    
    def __str__(self) -> str:
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Author(BaseModel):
    full_name = models.CharField(max_length=255)
    birthday  = models.DateField()
    country = models.ForeignKey(Country, blank=True, default=None, on_delete = models.CASCADE, related_name='authors')
    image = models.ImageField(upload_to='authors/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','heic','heif'])])

    def __str__(self) -> str:
        return self.full_name


class Book(BaseModel):

    BOOK_STATUS = (
        (DRAFT, DRAFT),
        (PUBLISHED, PUBLISHED)
    )

    title = models.CharField(max_length=60)
    description = models.TextField(validators=[MaxLengthValidator(2000)])
    book_file = models.FileField(upload_to = 'uploads/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf','epub','doc','docx'])], )
    book_audio = models.FileField(upload_to = 'uploads/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp3','wav']), validate_file])
    subcategory= models.ManyToManyField(SubCategory)
    image = models.ImageField(upload_to='books/')
    book_status = models.CharField(max_length=31, choices=BOOK_STATUS, default=DRAFT)
    author = models.ForeignKey(Author, on_delete= models.CASCADE, related_name='books')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='books')

    def __str__(self) -> str:
        return self.title


class BookViews(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='views')

    class Meta:
        ordering = ['-created_time']
        constraints  = [
            UniqueConstraint(
                fields = ['user', 'book'], name='unique_book_views'
            ),
            ]


class LikeBook(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        ordering = ['-created_time']
        constraints  = [
            UniqueConstraint(
                fields = ['user', 'book'], name='unique_book_likes'
            ),
            ]
        

class BookComment(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self) -> str:
        return f"{self.user} - {self.book}"
