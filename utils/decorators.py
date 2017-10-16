from functools import wraps

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from forecast.exceptions import ForecastException


def render_to_json(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            data = f(request, *args, **kwargs)
            return JsonResponse(data, safe=isinstance(data, dict))
        except (ValidationError, ForecastException) as e:
            return JsonResponse(data={'error': e.message}, status=400)
    return wrapper
