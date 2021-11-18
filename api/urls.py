from django.urls import path
from .views import (TodoCompletedList,
                    TodoListCreate,
                    TodoListRetrieveUpdateDestroy,
                    TodoListComplete,
                    signup,
                    RegisterUser)

app_name = "api"


urlpatterns = [
    path('signup/', signup, name="signup"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('todo/', TodoListCreate.as_view(), name="create-api"),
    path('todo/<int:pk>/', TodoListRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-api"),
    path('todo/<int:pk>/complete/', TodoListComplete.as_view(), name="complete-api"),
    path('todo/completed/', TodoCompletedList.as_view(), name="api-list"),
]