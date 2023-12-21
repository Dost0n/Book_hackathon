from rest_framework import serializers
from book.models import Category, Book, BookComment, Author, SubCategory, Country, LikeBook, BookViews
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    subcategory_count = serializers.SerializerMethodField('get_subcategory_count')
    category_status = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name' ,'category_status', 'subcategory_count')

    @staticmethod
    def get_subcategory_count(obj):
        return obj.subcategories.count()
    

class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name' ,)


class SubCategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
            'category',
            'category_id'
        )


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = SubCategory
        fields = (
            'name',
            'category_id'
        )


class CountrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    authors_count = serializers.SerializerMethodField('get_book_authors_count')

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'authors_count',
        )
    
    @staticmethod
    def get_book_authors_count(obj):
        return obj.authors.count()


class AuthorSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = Author
        fields = (
            'id',
            'full_name',
            'birthday',
            'country',
            'country_id',
            'image'
        )


class AuthorCreateSerializer(serializers.ModelSerializer):
    country_id = serializers.UUIDField(write_only = True)
    image = serializers.ImageField(required=False, max_length=None, allow_null=True, use_url=True)
    class Meta:
        model = Author
        fields = (
            'full_name',
            'birthday',
            'country_id',
            'image',
        )


class BookSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    subcategory = SubCategorySerializer(read_only=True, many=True,)
    author = AuthorSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    subcategory_id = serializers.UUIDField(write_only = True)
    author_id = serializers.UUIDField(write_only = True)
    book_status = serializers.CharField(read_only=True)
    views_count = serializers.SerializerMethodField('get_book_views_count')
    comment_count = serializers.SerializerMethodField('get_book_comments_count')
    likes_count = serializers.SerializerMethodField('get_book_likes_count')

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'book_file' ,'book_audio', 'subcategory',
                    'subcategory_id', 'image', 'book_status','author', 'author_id', 'user',
                    'views_count', 'comment_count', 'likes_count')

        extra_kwargs = {
            "book_audio":{"required":False},
            "image":{"required":False}
        }

    @staticmethod
    def get_book_comments_count(obj):
        return obj.comments.count()
    
    @staticmethod
    def get_book_views_count(obj):
        return obj.views.count()
    
    @staticmethod
    def get_book_likes_count(obj):
        return obj.likes.count()


class BookCreateSerializer(serializers.ModelSerializer):
    # subcategory = serializers.SlugRelatedField(slug_field='id', many=True, queryset=SubCategory.objects.all())
    author_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = Book
        fields = ('title', 'description', 'book_file' ,'book_audio','subcategory', 'image','author_id')

        extra_kwargs = {
            "book_audio":{"required":False},
            "image":{"required":False}
        }


class BookCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    

    class Meta:
        model = BookComment
        fields = (
            'id',
            'user',
            'book',
            'comment'
            )
        

class BookCommentCreateSerializer(serializers.ModelSerializer):
    # book_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = BookComment
        fields = (
            # 'book_id',
            'comment',
            )
        

class BookViewsListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    

    class Meta:
        model = BookViews
        fields = (
            'id',
            'user',
            'book'
            )


class BookLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = LikeBook
        fields = (
            'id',
            'user',
            'book'
            )


class BookLikeCreateSerializer(serializers.ModelSerializer):

    book_id = serializers.UUIDField(write_only = True)

    class Meta:
        model = LikeBook
        fields = ('book_id',)
    

class GlobalSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)


class BookAudioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ('book_audio', )
