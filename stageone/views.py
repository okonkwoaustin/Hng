from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
import requests
import json
from datetime import datetime, timezone


class ProfileView(APIView):
    def get_cat_fact(self, request):
        try:
            response = requests.get(settings.EXTERNAL_API_URL,
                                    timeout=settings.EXTERNAL_API_TIMEOUT
                                    )
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            error_message = {
                "error": "Failed to fetch data from external API", "details": str(e)}
            return Response(error_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def get(self, request):
        cat_fact_response = self.get_cat_fact(request)
        if cat_fact_response.status_code != status.HTTP_200_OK:
            return cat_fact_response
        current_time_utc = datetime.now(timezone.utc)
        profile_data = {
            "status": "success",
            "user": {
                "email": settings.MY_EMAIL,
                "name": settings.MY_NAME,
                "stack": settings.MY_STACK
            },
            "timestamp": current_time_utc.isoformat(),
            "fact": cat_fact_response.data
        }
        return Response(profile_data, status=status.HTTP_200_OK)
