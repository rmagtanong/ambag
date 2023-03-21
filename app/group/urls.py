"""
URL Mappings for Group API
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from group import views
from expense import views as expense_views


router = DefaultRouter()
router.register('', views.GroupViewSet)

expense_router = DefaultRouter()
expense_router.register('', expense_views.ExpenseViewSet, basename='expense')

app_name = 'group'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:group_id>/',
         include([path('expense/', include(expense_router.urls))]))
]
