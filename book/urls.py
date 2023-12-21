from django.urls import path
from book.views import (CategoryListCreateAPIView, BookCommentListCreateAPIView, BookListCreateAPIView,
                        AuthorListCreateAPIView, SubCategoryListCreateAPIView, CountryListCreateAPIView,
                        CategoryRetrieveUpdateDestroyView, SubCategoryRetrieveUpdateDestroyView, 
                        BookRetrieveUpdateDestroyView, AuthorRetrieveUpdateDestroyView,
                        BookCommentRetrieveUpdateDestroyView, CountryRetrieveUpdateDestroyView, 
                        BookViewsListAPIView, BookLikeListAPIView, BookLikeCreateDeleteAPIView,
                        PopularBookViewsListAPIView, PopularBookCommentListAPIView,
                        BookFilterByCategoryView, BookAuthorFilterView, BookGlobalFilterView,
                        GetAudioData, BookFilterBySubCategoryView, SubcategoryFilterByCategoryView)


urlpatterns = [
    path('category/', CategoryListCreateAPIView.as_view(), name='category' ),
    path('category/<str:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrive' ),
    path('category/<str:id>/books/', BookFilterByCategoryView.as_view(), name='book-category'),
    path('category/<str:id>/subcategory/', SubcategoryFilterByCategoryView.as_view(), name='subcategory-category'),
    path('subcategory/', SubCategoryListCreateAPIView.as_view(), name='subcategory' ),
    path('subcategory/<str:id>/', SubCategoryRetrieveUpdateDestroyView.as_view(), name='subcategory-retrive' ),
    path('subcategory/<str:id>/books/', BookFilterBySubCategoryView.as_view(), name='subcategory-book' ),
    path('book/', BookListCreateAPIView.as_view(), name='book' ),
    path('book/<str:id>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrive' ),
    path('book/<str:id>/audio/', GetAudioData.as_view(), name='book-audio' ),
    path('book/<str:id>/views/', BookViewsListAPIView.as_view(), name='book-views'),
    path('book/<str:id>/comment/', BookCommentListCreateAPIView.as_view(), name='book-comment' ),
    path('liked/books', BookLikeListAPIView.as_view(), name='book-likes'),
    path('liked/book/<str:id>/', BookLikeCreateDeleteAPIView.as_view(), name='book-like-delete'),
    path('popularbooks/views/', PopularBookViewsListAPIView.as_view(), name='book-popular'),
    path('popularbooks/comment/', PopularBookCommentListAPIView.as_view(), name='book-comment-popular'),
    path('globalsearch/', BookGlobalFilterView.as_view(), name='global-search'),
    path('comment/<str:id>/', BookCommentRetrieveUpdateDestroyView.as_view(), name='book-comment-retrive' ),
    path('authors/', AuthorListCreateAPIView.as_view(), name='authors' ),
    path('authors/<str:id>/', AuthorRetrieveUpdateDestroyView.as_view(), name='authors-retrive' ),
    path('authors/<str:id>/books/', BookAuthorFilterView.as_view(), name='book-author'),
    path('country/', CountryListCreateAPIView.as_view(), name='country'),
    path('country/<str:id>/', CountryRetrieveUpdateDestroyView.as_view(), name='country-retrive')
]
