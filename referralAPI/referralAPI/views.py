from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import User, LoginHistory
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer


def welcome(request):
    return HttpResponse("This is API HOST URL")


@api_view(["POST"])
def user_registration(request):
    if request.method == "POST":
        data = request.data
        name = data.get("name", None) or None
        if not name:
            return Response({"error": "name is not provided"}, status=status.HTTP_403_FORBIDDEN)
        email = data.get("email", None) or None
        password = data.get("password", None) or None
        referral_code = data.get("referral_code", None)
        if User.objects.filter(name=name).exists():
            user = User.objects.get(name=name)
            print(user, user.referral_code, referral_code)
            if referral_code and user.referral_code != referral_code:
                user.referral_code = referral_code
                user.referral_score += 1
                user.save()
            user_history = LoginHistory.objects.get(user=user)
            return Response({"token": user_history.token, "userID": user.userID, "status": "your token is provided"},
                            status=status.HTTP_201_CREATED)
        if name and email and password:
            password = make_password(password)
            if referral_code:
                user_data = User(name=name, email=email, password=password, referral_code=referral_code,
                                 referral_score=1)
                user_data.save()
                return Response(user_data.get_token(user=user_data), status=status.HTTP_201_CREATED)
            user_data = User(name=name, email=email, password=password, referral_code=referral_code)
            user_data.save()
            return Response(user_data.get_token(user=user_data), status=status.HTTP_201_CREATED)
        return Response({"error": "either email or password is not provided"},
                        status=status.HTTP_403_FORBIDDEN)
    return HttpResponse("This is registration url", status=status.HTTP_200_OK)


@api_view(["GET"])
def users_info(request):
    if request.method == "GET":
        token = request.META.get("HTTP_TOKEN", "not provided") or None
        users_login_tokens = LoginHistory.objects.values_list('token', flat=True)
        if token in list(users_login_tokens):
            users_login_tokens = LoginHistory.objects.get(token=token)
            user = User.objects.get(name=str(users_login_tokens.user).split("_")[1])
            serializers = UserSerializer([user], many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response({"status": "token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def users_info_referral(request):
    if request.method == "GET":
        token = request.META.get("HTTP_TOKEN", "not provided")
        users_login_tokens = LoginHistory.objects.values_list('token', flat=True)
        if token in list(users_login_tokens):
            paginator = PageNumberPagination()
            paginator.page_size = 20
            users = User.objects.all().exclude(referral_score=0)
            result_obj = paginator.paginate_queryset(users, request)
            serializers = UserSerializer(result_obj, many=True)

            return paginator.get_paginated_response(serializers.data)
        return Response({"status": "token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
