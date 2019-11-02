from rest_framework.routers import DefaultRouter
from rest_framework_jwt.settings import api_settings


class NoPutRouter(DefaultRouter):
    """
    Router class that disables the PUT method.
    """
    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)

        if 'put' in bound_methods.keys():
            del bound_methods['put']

        return bound_methods


def jwt_obtain_token(obj):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(obj)
    return jwt_encode_handler(payload)