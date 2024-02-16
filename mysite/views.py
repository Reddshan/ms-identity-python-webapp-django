import os
import json

from django.conf import settings
from django.shortcuts import render
import requests


__version__ = "0.4.0"


@settings.AUTH.login_required
def index(request, *, context):
    return render(request, 'index.html', dict(
        user=context['user'],
        version=__version__,
        edit_profile_url=settings.AUTH.get_edit_profile_url(),
        downstream_api=os.getenv("ENDPOINT"),
    ))

@settings.AUTH.login_required(scopes=os.getenv("SCOPE", "").split())
def call_downstream_api(request, *, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render(request, 'display.html', {
        "title": "Result of downstream API call",
        "content": json.dumps(api_result, indent=4),
    })

