from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


def is_auth(allowed_roles: set):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header is not None:
                try:
                    token_type, token = auth_header.split()

                    token_obj = Token.objects.get(key=token)
                    request.user = token_obj.user

                    if request.user.position.rights_level not in allowed_roles:
                        return Response({'error': 'У вас нет доступа'}, status=status.HTTP_403_FORBIDDEN)

                    return view_func(view, request, *args, **kwargs)
                except (ValueError, Token.DoesNotExist):
                    return Response({'error': 'Неверный токен'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Доступ запрещен '},
                                status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view
    return decorator

class RedirectToLoginView(View):
    def get(self, request):
        return redirect('login/')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:active-user-list')
        else:
            return redirect('app:login_error')


class LoginErrorView(View):
    def get(self, request):
        return render(request, 'login_error.html', {'error': 'Неверные учетные данные'})


