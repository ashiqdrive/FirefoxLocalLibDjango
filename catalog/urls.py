from django.urls import path
from catalog import views

urlpatterns = []

urlpatterns += [
    path('', views.index, name='index'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.SeeLoanedBooksListView.as_view(), name='all-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    path('books/', views.BookListView.as_view(), name='books'),#list of all books
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),# Detailed view of a particular book whose primary key is passed
    path('books/create/',views.BookCreate.as_view(),name='book_create'),
    path('books/<int:pk>/update/',views.BookUpdate.as_view(),name='book_update'),
    path('books/<int:pk>/delete/',views.BookDelete.as_view(),name='book_delete'),
]