from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
import requests
import json
from datetime import datetime, timezone


class ProfileView(APIView):
    def get_cat_fact(self):
        try:
            response = requests.get(
                settings.EXTERNAL_API_URL, timeout=settings.EXTERNAL_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json().get("fact")
        except requests.RequestException:
            return None

    def get(self, request):
        cat_fact = self.get_cat_fact()
        if not cat_fact:
            return Response({"status": "error", "message": "Failed to fetch external fact"},
                             status=status.HTTP_503_SERVICE_UNAVAILABLE)

             
        current_time_utc = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat().replace("+00:00", "Z")

        profile_data = {
            "status": "success",
            "user": {
                "email": getattr(settings, "MY_EMAIL", ""),
                "name": getattr(settings, "MY_NAME", ""),
                "stack": getattr(settings, "MY_STACK", ""),
            },
            "timestamp": current_time_utc,
            "fact": cat_fact,
        }

        return Response(profile_data, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})
