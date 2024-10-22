from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from app.api.login import LoginView, RedirectToLoginView, LoginErrorView
from app.api.position import PositionListCreateView
from app.api.user import ActiveUserListView, \
    UserDetailView, UserCreateView, UserTerminateView, \
    ActiveUserJsonView, UserUpdateView
from app.views import custom_404_view

handler404 = custom_404_view

app_name = 'app'

urlpatterns = [

    path('token/', obtain_auth_token, name='token_obtain'),

    path('', RedirectToLoginView.as_view(), name='redirect_to_login'),
    path('login-error/', LoginErrorView.as_view(), name='login_error'),

    path('login/', LoginView.as_view(), name='login'),
    path('users/', ActiveUserListView.as_view(), name='active-user-list'),
    path('users_json/', ActiveUserJsonView.as_view(), name='active-json-user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/update/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/<int:id>/', UserTerminateView.as_view(), name='user-terminate'),
    path('positions/', PositionListCreateView.as_view(), name='position'),
]