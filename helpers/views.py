from typing import Any

from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from helpers.serializers import EmptySchema


class ReadWriteModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet с двумя сериализаторами - на чтение и на запись"""

    serializer_class_in = EmptySchema
    serializer_class_out: Any = EmptySchema

    @swagger_auto_schema(responses={200: serializer_class_out()})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class_out(
            instance=instance, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializer_class_out(many=True)})
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

    @swagger_auto_schema(
      request=serializer_class_in, responses={200: serializer_class_out}
    )
    def create(self, request, *args, **kwargs):
        serializer_in = self.serializer_class_in(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        walk = serializer_in.save()
        serializer_out = self.serializer_class_out(
            instance=walk, context={'request': request})
        return Response(serializer_out.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
      request=serializer_class_in, responses={200: serializer_class_out()}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_in = self.serializer_class_in(
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
