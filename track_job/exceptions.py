from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 1. Call DRF's default handler first to get the standard error response.
    response = exception_handler(exc, context)

    # 2. If response is None, it means DRF didn't catch it (e.g., a database crash)
    if response is None:
        return Response({
            'success': False,
            'error': 'Server Error',
            'message': 'An unexpected error occurred on our end.',
            'technical_details': str(exc) # Optional: remove this in production!
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 3. If it's a standard DRF error (like 400 Bad Request or 401 Unauthorized)
    # You can wrap it in a consistent structure
    custom_data = {
        'success': False,
        'status_code': response.status_code,
        'errors': response.data,  # This contains the field-specific errors
    }
    response.data = custom_data

    return response