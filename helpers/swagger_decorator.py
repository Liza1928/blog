from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


def decorate_with_serializers(
        function,
        write_serializer_class,
        read_serializer_class
):
    function_name = function.__name__
    print(function_name)
    swagger_decorator = swagger_auto_schema()
    if function_name == 'list':
        swagger_decorator = swagger_auto_schema(
            responses={200: read_serializer_class(many=True)})
    elif function_name == 'retrieve':
        swagger_decorator = swagger_auto_schema(
            responses={200: read_serializer_class()})
    elif function_name == 'create':
        swagger_decorator = swagger_auto_schema(
            request_body=write_serializer_class,
            responses={205: read_serializer_class()})
    elif function_name == 'update':
        swagger_decorator = swagger_auto_schema(
            request_body=write_serializer_class,
            responses={200: read_serializer_class()}),
    elif function_name == 'destroy':
        pass
    swagger_decorator = method_decorator(
        swagger_decorator, 'swagger_decorator')
    function = swagger_decorator(function)
    return function


def swagger_auto_viewset(target):
    def init_with_swagger(self, *args, **kwargs):
        super(target, self).__init__(*args, **kwargs)
        serializer_write = target.get_write_serializer_class(self)
        serializer_read = target.get_read_serializer_class(self)
        decorated_functions = ['list', 'retrieve', 'create', 'update',
                               'destroy']
        for function in decorated_functions:
            if hasattr(target, function):
                decorated_method = getattr(target, function)
                setattr(target, function,
                        decorate_with_serializers(
                            decorated_method, serializer_write, serializer_read
                        ))
    target.__init__ = init_with_swagger
    return target