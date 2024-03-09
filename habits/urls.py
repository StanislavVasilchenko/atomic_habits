from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitDetailAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, GoodHabitListPublicAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('', HabitListAPIView.as_view(), name='habit-list'),
    path('detail/<int:pk>/', HabitDetailAPIView.as_view(), name='habit-detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit-delete'),
    path('public/', GoodHabitListPublicAPIView.as_view(), name='habit-public-list'),

]
