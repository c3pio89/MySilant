import django_filters
from django_filters import FilterSet, ModelChoiceFilter, CharFilter
# from django.forms import DateTimeInput

from .models import (
    Machine, Equipment, Engine, Transmission, DrivingAxle, SteeringAxle, TypeMaintenance, Maintenance, ServiceCompany,
    Claim, RefusalNode, RecoveryMethod
)


# Для фильтрации по таблице с машинами
class MachineFilter(FilterSet):
    # Для организации фильтрации по модели техники
    model_equipment = ModelChoiceFilter(
        field_name='model_equipment__title',
        queryset=Equipment.objects.all(),
        label='Модель техники',
    )

    # Для организации фильтрации по модели двигателя
    model_engine = ModelChoiceFilter(
        field_name='model_engine__title',
        queryset=Engine.objects.all(),
        label='Модель двигателя',
    )

    # Для организации фильтрации по модели трансмиссии
    model_transmission = ModelChoiceFilter(
        field_name='model_transmission__title',
        queryset=Transmission.objects.all(),
        label='Модель трансмиссии',
    )

    # Для организации фильтрации по модели ведущего моста
    model_driving_axle = ModelChoiceFilter(
        field_name='model_driving_axle__title',
        queryset=DrivingAxle.objects.all(),
        label='Модель вед. моста',
    )

    # Для организации фильтрации по модели управляемого моста
    model_steering_axle = ModelChoiceFilter(
        field_name='model_steering_axle__title',
        queryset=SteeringAxle.objects.all(),
        label='Модель упр. моста',
    )


# Для ограниченной фильтрации по таблице с машинами (для незарегистрированных пользователей)
class MachinePreviewFilter(FilterSet):
    # Для организации фильтрации по заводскому номеру машины
    number_machine = django_filters.CharFilter(
        field_name='number_machine',
        lookup_expr='icontains',
        label='Заводской № машины',
    )


# Для фильтрации по таблице с ТО
class MaintenanceFilter(FilterSet):
    # Для организации фильтрации по виду ТО
    type = ModelChoiceFilter(
        field_name='type__title',
        queryset=TypeMaintenance.objects.all(),
        label='Вид ТО',
    )

    # Для организации фильтрации по заводскому номеру машины
    machine = django_filters.CharFilter(
        field_name='machine__number_machine',
        lookup_expr='icontains',
        label='Заводской № машины',
    )

    # Для организации фильтрации по сервисной компании
    service_company = ModelChoiceFilter(
        field_name='service_company__title',
        queryset=ServiceCompany.objects.all(),
        label='Сервисная компания',
    )

# Для фильтрации по таблице с рекламациями
class ClaimFilter(FilterSet):
    # Для организации фильтрации по узлу отказа
    refusal_node = ModelChoiceFilter(
        field_name='refusal_node__title',
        queryset=RefusalNode.objects.all(),
        label='Узел отказа',
    )

    # Для организации фильтрации по способу восстановления
    recovery_method = ModelChoiceFilter(
        field_name='recovery_method__title',
        queryset=RecoveryMethod.objects.all(),
        label='Способ восстановления',
    )

    # Для организации фильтрации по сервисной компании
    service_company = ModelChoiceFilter(
        field_name='service_company__title',
        queryset=ServiceCompany.objects.all(),
        label='Сервисная компания',
    )
