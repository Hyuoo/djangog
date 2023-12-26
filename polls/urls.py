from django.urls import path
from . import views
# import views 이래하면 안됨.
from .views import *

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/result/', views.result, name='result'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('zzz', views.asdf, name=''),
]
