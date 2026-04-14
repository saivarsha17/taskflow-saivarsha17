import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from auth.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from auth.utilities.responses import validation_error

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        logger.info("User registered: %s", user.email)
        return Response(
            {"token": str(refresh.access_token), "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        logger.info("User logged in: %s", user.email)
        return Response(
            {"token": str(refresh.access_token), "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )
