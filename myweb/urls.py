from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('index', views.home),
    path('books', views.books, name="book"),
    path('books/create', views.createBook, name="createBook"),
    path('books/update/<doc_id>', views.updateBook, name="updateBook"),
    path('books/delete/<doc_id>', views.deleteBook, name="deleteBook"),
]
