from django import forms
from django.core.exceptions import ValidationError

from .models import Machine, Maintenance, Claim, Client, ServiceCompany


# Форма для создания/редактирования записи о машине
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'number_machine',
            'model_equipment',
            'model_engine',
            'number_engine',
            'model_transmission',
            'number_transmission',
            'model_driving_axle',
            'number_driving_axle',
            'model_steering_axle',
            'number_steering_axle',
            'supply_contract',
            'shipment_date',
            'end_consumer',
            'shipping_address',
            'options',
            'client',
            'service_company'
        ]

        labels = {
            'number_machine': 'Заводской номер машины',
            'model_equipment': 'Модель техники',
            'model_engine': 'Модель двигателя',
            'number_engine': 'Заводской номер двигателя',
            'model_transmission': 'Модель трансмиссии',
            'number_transmission': 'Заводской номер трансмиссии',
            'model_driving_axle': 'Модель ведущего моста',
            'number_driving_axle': 'Заводской номер ведущего моста',
            'model_steering_axle': 'Модель управляемого моста',
            'number_steering_axle': 'Заводской номер управляемого моста',
            'supply_contract': 'Договор поставки (номер, дата)',
            'shipment_date': 'Дата отгрузки с завода в формате ГГГГ-ММ-ЧЧ',
            'end_consumer': 'Грузополучатель (конечный потребитель)',
            'shipping_address': 'Адрес поставки (эксплуатации)',
            'options': 'Комплектация (дополнительные опции)',
            'client': 'Клиент',
            'service_company': 'Сервисная компания'
        }


# Форма для создания/редактирования записи о ТО
class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        # Поле service_company не выводится, так как задается автоматически при создании объекта
        fields = [
            'machine',
            'type',
            'maintenance_date',
            'operating_time',
            'order_number',
            'order_date',
            'maintenance_company',
        ]

        labels = {
            'machine': 'Машина',
            'type': 'Вид ТО',
            'maintenance_date': 'Дата проведения ТО',
            'operating_time': 'Наработка, м/час',
            'order_number': 'Номер заказ-наряда',
            'order_date': 'Дата заказ-наряда',
            'maintenance_company': 'Организация, проводившая ТО',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # В поле 'машина' нужно выводить только машины соответствующие пользователю
        user = kwargs['initial']['user']
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user in users_clients:
            # Если клиент - доступны только его машины
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(client__user_link=user)
            )
        elif user in users_companies:
            # Если сервисная компания - доступны только ее машины
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(service_company__user_link=user)
            )

    def clean(self):
        cleaned_data = super().clean()
        operating_time = cleaned_data.get("operating_time")
        # Проверка корректности наработки
        if operating_time < 0:
            raise ValidationError({
                "operating_time": "Наработка должна быть положительным числом"
            })
        return cleaned_data


# Форма для создания/редактирования записи о рекламации
class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        # Поле downtime не выводится, так как вычисляется автоматически при создании объекта
        # Поле service_company не выводится, так как задается автоматически при создании объекта
        fields = [
            'machine',
            'refusal_date',
            'operating_time',
            'refusal_node',
            'refusal_description',
            'recovery_method',
            'repair_parts',
            'recovery_date',
        ]

        labels = {
            'machine': 'Машина',
            'refusal_date': 'Дата отказа',
            'operating_time': 'Наработка, м/час',
            'refusal_node': 'Узел отказа',
            'refusal_description': 'Описание отказа',
            'recovery_method': 'Способ восстановления',
            'repair_parts': 'Используемые запасные части',
            'recovery_date': 'Дата восстановления',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # В поле 'машина' нужно выводить только машины соответствующие пользователю
        user = kwargs['initial']['user']
        companies = ServiceCompany.objects.all()
        users_companies = []
        for company in companies:
            users_companies.append(company.user_link)
        if user in users_companies:
            # Если сервисная компания - доступны только ее машины
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(service_company__user_link=user)
            )

    def clean(self):
        cleaned_data = super().clean()
        refusal_date = cleaned_data.get("refusal_date")
        recovery_date = cleaned_data.get("recovery_date")
        operating_time = cleaned_data.get("operating_time")
        # Проверка корректности дат
        if self.is_valid():
            if recovery_date < refusal_date:
                raise ValidationError({
                    "recovery_date": "Дата восстановления должна быть не раньше даты отказа"
                })
            # Проверка корректности наработки
            if operating_time < 0:
                raise ValidationError({
                    "operating_time": "Наработка должна быть положительным числом"
                })
        return cleaned_data
