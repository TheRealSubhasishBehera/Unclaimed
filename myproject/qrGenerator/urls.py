from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from qrGenerator import views


urlpatterns=[
    path('user/',views.UserList.as_view()),
    path('user/<int:pk>/',views.Userdetail.as_view()),  #primary key for User method
    path('item/',views.ItemList.as_view()),
    path('iser/<int:pk>/',views.ItemDetail.as_view()),
]

urlpatterns=format_suffix_patterns(urlpatterns)