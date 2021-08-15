from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator


class ReadWriteModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet с двумя сериализаторами - на чтение и на запись"""

    serializer_class_in = None
    serializer_class_out = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ниже представлен вариант явного декорирования
        # decorator = swagger_auto_schema(responses={500: self.serializer_class_in(many=True)})
        # decorator = method_decorator(decorator, 'decorator')
        # self.retrieve = decorator(self.retrieve)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class_out
        elif self.serializer_class_in:
            return self.serializer_class_in
        else:
            return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class_out(
            instance=instance, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            queryset = self.filter_queryset(queryset)
        except AttributeError:
            # OrderingFilter object has no attribute filter_queryset
            pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class_out(
                instance=page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class_out(
            instance=queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer_in = self.serializer_class_in(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        obj = serializer_in.save()
        serializer_out = self.serializer_class_out(
            instance=obj, context={'request': request})
        return Response(serializer_out.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_in = self.serializer_class_out(
            instance, data=request.data, partial=partial)
        serializer_in.is_valid(raise_exception=True)
        self.perform_update(serializer_in)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer_out = self.serializer_class_out(
            instance=instance, context={'request': request})
        return Response(serializer_out.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        obj = self.serializer_class_out(
            instance=instance, context={'request': request}).data
        self.perform_destroy(instance)
        return Response(obj, status=status.HTTP_200_OK)
