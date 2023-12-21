from rest_framework.response import Response
from book.serializers import (CategorySerializer, CategoryCreateSerializer, BookSerializer,
                                BookCreateSerializer, SubCategorySerializer, SubCategoryCreateSerializer,
                                AuthorSerializer, AuthorCreateSerializer, BookCommentSerializer,
                                BookCommentCreateSerializer, CountrySerializer, BookLikeSerializer,
                                BookLikeCreateSerializer, GlobalSearchSerializer, BookViewsListSerializer,
                                BookAudioSerializer)
from book.models import Category, Book, BookComment, Author, SubCategory, Country, BookViews, LikeBook
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.db.models import Q
from config.custom_permission import UserCheckAdmin
from config.custom_pagination import CustomPagination
from django.http import FileResponse


class GetAudioData(APIView):
    serializer_class= BookAudioSerializer
  
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
            return FileResponse(book.book_audio.open(), as_attachment=True)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        

class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    @swagger_auto_schema(request_body=CategoryCreateSerializer)
    def post(self, request):
        serializer = CategoryCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)
    
    def get(self, request):
        categories = Category.objects.all().filter(category_status ='active').order_by('-created_time')
        if categories:
            serializer = CategorySerializer(categories, many=True)
            data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success":True
                }
            return Response(data=data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class CategoryRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CategorySerializer(category)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)
        
    
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        category.delete()
        return Response({
                        "success": True,
                        "status":status.HTTP_204_NO_CONTENT,
                        "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
                    })

    @swagger_auto_schema(request_body=CategoryCreateSerializer)
    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CategoryCreateSerializer(instance=category, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
        
    
    @swagger_auto_schema(request_body=CategoryCreateSerializer)
    def patch(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CategoryCreateSerializer(instance=category, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "code":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "code":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)


class SubCategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    @swagger_auto_schema(request_body=SubCategoryCreateSerializer)
    def post(self, request):
        serializer = SubCategoryCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)
    
    def get(self, request):
        subcategories = SubCategory.objects.all().order_by('-created_time')
        if subcategories:
            serializer = SubCategorySerializer(subcategories, many=True)
            data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success":True
                }
            return Response(data=data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class SubCategoryRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            subcategory = SubCategory.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = SubCategorySerializer(subcategory)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)
    
    def delete(self, request, id):
        try:
            subcategory = SubCategory.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        subcategory.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
            })
    
    @swagger_auto_schema(request_body=SubCategoryCreateSerializer)
    def put(self, request, id):
        try:
            subcategory = SubCategory.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = SubCategoryCreateSerializer(instance=subcategory, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
    

    @swagger_auto_schema(request_body=SubCategoryCreateSerializer)
    def patch(self, request, id):
        try:
            subcategory = SubCategory.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = SubCategoryCreateSerializer(instance=subcategory, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
    

class CountryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    @swagger_auto_schema(request_body=CountrySerializer)
    def post(self, request):
        serializer = CountrySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)
    
    def get(self, request):
        countries = Country.objects.all().order_by('-created_time')
        if countries:
            serializer = CountrySerializer(countries, many=True)
            data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success":True
                }
            return Response(data=data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class CountryRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CountrySerializer(country)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)
    
    def delete(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        country.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
            })
    
    @swagger_auto_schema(request_body=CountrySerializer)
    def put(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CountrySerializer(instance=country, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
    
    @swagger_auto_schema(request_body=CountrySerializer)
    def patch(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = CountrySerializer(instance=country, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)


class AuthorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]
    
    @swagger_auto_schema(request_body=AuthorCreateSerializer)
    def post(self, request):
        serializer = AuthorCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)
    
    def get(self, request):
        authors = Author.objects.all().order_by('-created_time')
        if authors:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(authors, request)
            serializer = AuthorSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)
        
    
class AuthorRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = AuthorSerializer(author)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)

    
    def delete(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        author.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
            })
    
    @swagger_auto_schema(request_body=AuthorCreateSerializer)
    def put(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = AuthorSerializer(instance=author, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
    
    @swagger_auto_schema(request_body=AuthorCreateSerializer)
    def patch(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = AuthorSerializer(instance=author, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)


class BookListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(request_body=BookCreateSerializer)
    def post(self, request):
        serializer = BookCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)
    
    def get(self, request):
        books = Book.objects.all().filter(book_status = 'published').order_by('-created_time')
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        
        if request.user.is_authenticated:
            BookViews.objects.create(user = self.request.user,book = book)
        serializer = BookSerializer(book)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        book.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
            })
    
    @swagger_auto_schema(request_body=BookCreateSerializer)
    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCreateSerializer(instance=book, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)

    
    @swagger_auto_schema(request_body=BookCreateSerializer)
    def patch(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCreateSerializer(instance=book, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)


class BookCommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(request_body=BookCommentCreateSerializer)
    def post(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCommentCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user, book = book)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)

    def get(self, request, id):
        bookcomments = BookComment.objects.filter(book__id=id).order_by('-created_time')
        if bookcomments:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(bookcomments, request)
            serializer = BookCommentSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookCommentRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    def get(self, request, id):
        try:
            bookcomment = BookComment.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCommentSerializer(bookcomment)
        data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success":True
                }
        return Response(data=data)
    
    def delete(self, request, id):
        try:
            bookcomment = BookComment.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        bookcomment.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Book comment successfully updated"
            })
    

    @swagger_auto_schema(request_body=BookCommentCreateSerializer)
    def put(self, request, id):
        try:
            bookcomment = BookComment.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCommentCreateSerializer(instance=bookcomment, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)
    
    @swagger_auto_schema(request_body=BookCommentCreateSerializer)
    def patch(self, request, id):
        try:
            bookcomment = BookComment.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        serializer = BookCommentCreateSerializer(instance=bookcomment, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                "data":serializer.data,
                "success": True,
                "status":status.HTTP_200_OK,
                "message":"Ma'lumot muvaffaqiyatli o'zgartirildi!"
            }
            return Response(data=data)
        else:
            data = {
                "success": False,
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Ma'lumot yuborishda xatolik!",
                "data":serializer.errors
            }
            return Response(data=data)


class PopularBookViewsListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def get(self, request):
        books = Book.objects.all().filter(book_status = 'published').order_by('-views')
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class PopularBookCommentListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def get(self, request):
        books = Book.objects.all().filter(book_status = 'published').order_by('-comments')
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookFilterByCategoryView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, id):
        books = Book.objects.filter(category__id=id)
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookFilterBySubCategoryView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, id):
        books = Book.objects.filter(subcategory__id=id)
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class SubcategoryFilterByCategoryView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, id):
        subcategory = SubCategory.objects.filter(category__id=id)
        if subcategory:
            serializer = SubCategorySerializer(subcategory, many=True)
            data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success":True
                }
            return Response(data=data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookAuthorFilterView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id):
        books = Book.objects.filter(author__id=id)
        if books:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookGlobalFilterView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=GlobalSearchSerializer)
    def post(self, request):
        serializer = GlobalSearchSerializer(data = request.data)
        if serializer.is_valid():
            q = request.data['query']
            books = Book.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(author__full_name__icontains=q))
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewsListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def get(self, request, id):
        bookviews = BookViews.objects.filter(book__id=id).order_by('-created_time')
        if bookviews:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(bookviews, request)
            serializer = BookViewsListSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)
        
    
class BookLikeListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        booklikes = LikeBook.objects.filter(user=request.user).order_by('-created_time')
        if booklikes:
            paginator = CustomPagination()
            page_obj = paginator.paginate_queryset(booklikes, request)
            serializer = BookLikeSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class BookLikeCreateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, UserCheckAdmin]

    @swagger_auto_schema(request_body=BookLikeCreateSerializer)
    def post(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        if request.user.is_authenticated:
            LikeBook.objects.create(user = self.request.user, book = book)
            data = {
                "status": status.HTTP_201_CREATED,
                "success":True,
                "message":"Ma'lumot muvaffaqiyatli qo'shildi!"
                }
            return Response(data=data)
        else:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message":"Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)

    def delete(self, request, id):
        try:
            booklikes = LikeBook.objects.get(id=id)
        except:
            data = {
                    "data": [],
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success":False,
                    "message":"Berilgan id bo'yicha ma'lumot topilmadi!"
                }
            return Response(data=data)
        booklikes.delete()
        return Response(
            {
                "success": True,
                "status":status.HTTP_204_NO_CONTENT,
                "message":"Ma'lumot muvaffaqiyatli o'chirildi!"
            })