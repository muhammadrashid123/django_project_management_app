from rest_framework.response import Response


def custom_response(message, data=None, status_code=200):
    response_data = {
        "message": message,
        "data": data,
        "status_code": status_code
    }
    return Response(response_data, status=status_code)