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
            response = requests.get(
                settings.EXTERNAL_API_URL, timeout=settings.EXTERNAL_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def get(self, request):
        cat_fact_json = self.get_cat_fact(request)
        if not cat_fact_json:
            return Response({"status": "error", "message": "Failed to fetch external fact"},
                             status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Extract a plain fact string
        if isinstance(cat_fact_json, dict):
            fact_text = cat_fact_json.get("fact") or cat_fact_json.get(
                "message") or json.dumps(cat_fact_json)
        else:
            fact_text = str(cat_fact_json)

        # RFC3339 UTC timestamp ending with 'Z'
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
            "fact": fact_text,
        }

        return Response(profile_data, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})
