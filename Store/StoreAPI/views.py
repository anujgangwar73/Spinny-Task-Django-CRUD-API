from rest_framework import generics, filters
from .models import Box
from .serializers import BoxSerializer
from .permissions import IsStaffUser, CanUpdateBox, CanViewBox, CanViewMyBoxes, CanDeleteBox
from django_filters import rest_framework as django_filters
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime,timedelta
from django.db import models
from django.conf import settings

class BoxCreateView(generics.CreateAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsStaffUser]

    def perform_create(self, serializer):
        user = self.request.user
        current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        current_week_end = current_week_start + timedelta(days=6)

        # Condition 1: Average area of all added boxes should not exceed A1
        total_area = Box.objects.aggregate(total_area=models.Sum(models.F('length') * models.F('breadth'))).get(
            'total_area')
        total_boxes = Box.objects.count()
        average_area = total_area / total_boxes if total_boxes > 0 else 0
        if average_area + (serializer.validated_data['length'] * serializer.validated_data['breadth']) > getattr(settings, 'A1', 100):
            return Response({"error": "Average area of all added boxes exceeds A1"}, status=status.HTTP_403_FORBIDDEN)

        # Condition 2: Average volume of all boxes added by the current user shall not exceed V1
        user_boxes = Box.objects.filter(creator=user)
        total_user_area = user_boxes.aggregate(
            total_user_area=models.Sum(models.F('length') * models.F('breadth'))).get('total_user_area')
        total_user_volume = user_boxes.aggregate(
            total_user_volume=models.Sum(models.F('length') * models.F('breadth') * models.F('height'))).get(
            'total_user_volume')
        user_boxes_count = user_boxes.count()
        average_user_area = total_user_area / user_boxes_count if user_boxes_count > 0 else 0
        average_user_volume = total_user_volume / user_boxes_count if user_boxes_count > 0 else 0
        if (average_user_area + (
                serializer.validated_data['length'] * serializer.validated_data['breadth'])) > getattr(settings, 'A1', 100):
            return Response({"error": "Average area of all added boxes exceeds A1"}, status=status.HTTP_403_FORBIDDEN)
        if (average_user_volume + (
                serializer.validated_data['length'] * serializer.validated_data['breadth'] * serializer.validated_data[
            'height'])) > getattr(settings, 'V1', 100):
            return Response({"error": "Average area of all added boxes exceeds V1"}, status=status.HTTP_403_FORBIDDEN)

        # Condition 3: Total Boxes added in a week cannot be more than L1
        week_boxes = Box.objects.filter(created_at__gte=current_week_start, created_at__lte=current_week_end)
        if week_boxes.count() >= getattr(settings, 'L1', 100):
            return Response({"error": "Total Boxes added in a week exceeds L1"}, status=status.HTTP_403_FORBIDDEN)

        # Condition 4: Total Boxes added in a week by a user cannot be more than L2
        user_week_boxes = week_boxes.filter(creator=user)
        if user_week_boxes.count() >= getattr(settings, 'L2', 50):
            return Response({"error": "Total Boxes added in a week by the user exceeds L2"},
                            status=status.HTTP_403_FORBIDDEN)

        # Create the box
        serializer.save(creator=user)


class BoxUpdateView(generics.UpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsStaffUser, CanUpdateBox]

    def perform_update(self, serializer):
        user = self.request.user
        # Check conditions for update (similar to create)
        # Ensure that average area and volume conditions are not violated

        # Update the box
        serializer.save(creator=user)


class BoxFilter(django_filters.FilterSet):
    length_more_than = django_filters.NumberFilter(field_name="length", lookup_expr='gt')
    length_less_than = django_filters.NumberFilter(field_name="length", lookup_expr='lt')
    breadth_more_than = django_filters.NumberFilter(field_name="breadth", lookup_expr='gt')
    breadth_less_than = django_filters.NumberFilter(field_name="breadth", lookup_expr='lt')
    height_more_than = django_filters.NumberFilter(field_name="height", lookup_expr='gt')
    height_less_than = django_filters.NumberFilter(field_name="height", lookup_expr='lt')
    area_more_than = django_filters.NumberFilter(method='filter_by_area_more_than', label="Area is greater than:")
    area_less_than = django_filters.NumberFilter(method='filter_by_area_less_than', label="Area is less than:")
    volume_more_than = django_filters.NumberFilter(method='filter_by_volume_more_than', label="Volume is greater than:")
    volume_less_than = django_filters.NumberFilter(method='filter_by_volume_less_than', label="Volume is less than:")
    created_by = django_filters.CharFilter(method='filter_by_created_by', label="Created by:")
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lt')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gt')

    class Meta:
        model = Box
        fields = []

    def filter_by_area_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0).filter(
            Q(length__gte=value) | Q(breadth__gte=value) | Q(height__gte=value)
        )

    def filter_by_area_less_than(self, queryset, name, value):
        return queryset.filter(
            Q(length__lte=value) & Q(breadth__lte=value) & Q(height__lte=value)
        )

    def filter_by_volume_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0).filter(
            Q(length__gte=value) & Q(breadth__gte=value) & Q(height__gte=value)
        )

    def filter_by_volume_less_than(self, queryset, name, value):
        return queryset.filter(
            Q(length__lte=value) | Q(breadth__lte=value) | Q(height__lte=value)
        )

    def filter_by_created_by(self, queryset, name, value):
        return queryset.filter(creator__username=value)


class BoxListView(generics.ListAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [CanViewBox]
    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)
    filterset_class = BoxFilter
    ordering_fields = '__all__'
    ordering = ('-created_at',)


class MyBoxFilter(django_filters.FilterSet):
    length_more_than = django_filters.NumberFilter(field_name="length", lookup_expr='gt')
    length_less_than = django_filters.NumberFilter(field_name="length", lookup_expr='lt')
    breadth_more_than = django_filters.NumberFilter(field_name="breadth", lookup_expr='gt')
    breadth_less_than = django_filters.NumberFilter(field_name="breadth", lookup_expr='lt')
    height_more_than = django_filters.NumberFilter(field_name="height", lookup_expr='gt')
    height_less_than = django_filters.NumberFilter(field_name="height", lookup_expr='lt')
    area_more_than = django_filters.NumberFilter(method='filter_by_area_more_than', label="Area is greater than:")
    area_less_than = django_filters.NumberFilter(method='filter_by_area_less_than', label="Area is less than:")
    volume_more_than = django_filters.NumberFilter(method='filter_by_volume_more_than', label="Volume is greater than:")
    volume_less_than = django_filters.NumberFilter(method='filter_by_volume_less_than', label="Volume is less than:")

    class Meta:
        model = Box
        fields = []

    def filter_by_area_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0).filter(
            Q(length__gte=value) | Q(breadth__gte=value) | Q(height__gte=value)
        )

    def filter_by_area_less_than(self, queryset, name, value):
        return queryset.filter(
            Q(length__lte=value) & Q(breadth__lte=value) & Q(height__lte=value)
        )

    def filter_by_volume_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0).filter(
            Q(length__gte=value) & Q(breadth__gte=value) & Q(height__gte=value)
        )

    def filter_by_volume_less_than(self, queryset, name, value):
        return queryset.filter(
            Q(length__lte=value) | Q(breadth__lte=value) | Q(height__lte=value)
        )


class MyBoxListView(generics.ListAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [CanViewMyBoxes]
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = MyBoxFilter

    def get_queryset(self):
        # Filter boxes created by the currently authenticated staff user
        return Box.objects.filter(creator=self.request.user)


class BoxDeleteView(generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [CanDeleteBox]

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        # Ensure that the user is the creator of the box
        if instance.creator != user:
            return Response({"error": "You do not have permission to delete this box"}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
