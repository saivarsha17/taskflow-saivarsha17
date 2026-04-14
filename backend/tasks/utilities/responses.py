from rest_framework import status
from rest_framework.response import Response


def validation_error(fields):
    return Response(
        {"error": "validation failed", "fields": fields},
        status=status.HTTP_400_BAD_REQUEST,
    )


def forbidden():
    return Response({"error": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
