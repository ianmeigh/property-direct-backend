from rest_framework.views import exception_handler


# CREDIT: Custom Exceptions with Django Rest Framework
# AUTHOR: ruddra - StackOverflow
# URL:    https://stackoverflow.com/a/63129274
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data["status_code"] = response.status_code
    return response
