from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from qrGenerator import views
from qrGenerator import send_grid

urlpatterns=[
    path('users/',views.UserList.as_view()),
    path('user/<int:pk>/',views.UserDetail.as_view()),  #primary key for User method
    path('items/',views.ItemList.as_view()),
    path('item/<int:pk>/',views.ItemDetail.as_view()),
    path('addlostitem_sol/',views.AddLostItemView.as_view()),
    path('send_email/', views.SendEmailView.as_view(), name='send_email'),
    # path('send_gmail',send_grid.SendEmailView.as_view(),name='google-email_api')
]

urlpatterns=format_suffix_patterns(urlpatterns)