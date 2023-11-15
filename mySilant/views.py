from rest_framework import viewsets
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import (
    Machine, Maintenance, Claim, Client, ServiceCompany, Equipment, Engine, Transmission, DrivingAxle, SteeringAxle,
    MaintenanceCompany, TypeMaintenance, RefusalNode, RecoveryMethod
)
from .filters import MachineFilter, MaintenanceFilter, ClaimFilter, MachinePreviewFilter
from .forms import MachineForm, MaintenanceForm, ClaimForm
from .serializers import MachineSerializer, MaintenanceSerializer, ClaimSerializer


# Вывод списка машин
class MachineList(ListView):
    model = Machine  # выводим информацию о машинах
    ordering = 'shipment_date'  # сортировка по дате создания
    template_name = 'machines.html'  # шаблон для вывода
    context_object_name = 'machines'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 5  # количество машин на странице

    # Переопределяем функцию получения списка машин
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Если пользователь зарегистрирован
            clients = Client.objects.all()
            companies = ServiceCompany.objects.all()
            users_clients = []
            users_companies = []
            queryset = Machine.objects.none()
            for client in clients:
                users_clients.append(client.user_link)
            for company in companies:
                users_companies.append(company.user_link)
            if user.is_superuser == 1 or user.is_staff == 1:  # если админ или менеджер - доступны все машины
                queryset = super().get_queryset()
            elif user in users_clients:  # если клиент - доступны соответствующие машины
                queryset = Machine.objects.filter(client__user_link=user).order_by('shipment_date')
            elif user in users_companies:  # если сервисная компания - доступны соответствующие машины
                queryset = Machine.objects.filter(service_company__user_link=user).order_by('shipment_date')
            self.filterset = MachineFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        else:
            # Если пользователь не зарегистрирован - ограниченный фильтр по всем машинам
            if not self.request.GET.__contains__('number_machine'):
                queryset = super().get_queryset()
                queryset = Machine.objects.none()  # если в строке поиска пусто, то пустой queryset
            else:
                if self.request.GET.get('number_machine') != '':
                    queryset = super().get_queryset()  # если что-то есть в строке поиска, получаем обычный запрос
                else:
                    queryset = super().get_queryset()
                    queryset = Machine.objects.none()  # если отправлен пустой запрос, то пустой queryset
            self.filterset = MachinePreviewFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        return self.filterset.qs  # возвращаем отфильтрованный список машин

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # добавляем в контекст объект фильтрации
        return context


# Подробности по каждой машине
class MachineDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_machine'  # должны быть права на просмотр
    model = Machine  # выводим машины
    template_name = 'machine.html'  # шаблон для вывода
    context_object_name = 'machine'  # имя списка, по которому будет обращение из html-шаблона

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Machine.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все машины
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны соответствующие машины
            queryset = Machine.objects.filter(client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие машины
            queryset = Machine.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новой машине с проверкой прав
class MachineCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'mySilant.add_machine'  # должны быть права на добавление записи
    form_class = MachineForm
    model = Machine
    template_name = 'machine_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('machine_list')  # после создания записи возвращаемя на страницу с перечнем


# Редактирование записи о машине с проверкой прав
class MachineEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'mySilant.change_machine'  # должны быть права на редактипрование записи
    form_class = MachineForm
    model = Machine
    template_name = 'machine_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('machine_list')  # после редактирования записи возвращаемся на страницу с перечнем


# Удаление записи о машине с проверкой прав
class MachineDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'mySilant.delete_machine'  # должны быть права на удаление записи
    model = Machine
    template_name = 'machine_delete.html'  # шаблон для вывода
    success_url = reverse_lazy('machine_list')  # после удаления записи возвращаемся на страницу с перечнем


# Вывод списка ТО с проверкой прав
class MaintenanceList(PermissionRequiredMixin, ListView):
    permission_required = 'mySilant.view_maintenance'  # должны быть права на просмотр
    model = Maintenance  # выводим информацию о ТО
    ordering = 'maintenance_date'  # сортировка по дате создания
    template_name = 'maintenances.html'  # шаблон для вывода
    context_object_name = 'maintenances'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 15  # количество ТО на странице

    # Переопределяем функцию получения списка ТО
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все ТО
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(machine__client__user_link=user).order_by('maintenance_date')
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(service_company__user_link=user).order_by('maintenance_date')
        self.filterset = MaintenanceFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        return self.filterset.qs  # возвращаем отфильтрованный список машин

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # добавляем в контекст объект фильтрации
        return context


# Подробности по каждому ТО с проверкой прав
class MaintenanceDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_maintenance'  # должны быть права на просмотр
    model = Maintenance  # выводим ТО
    template_name = 'maintenance.html'  # шаблон для вывода
    context_object_name = 'maintenance'  # имя списка, по которому будет обращение из html-шаблона

    # Переопределяем функцию получения данных о ТО
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все ТО
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новом ТО с проверкой прав
class MaintenanceCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'mySilant.add_maintenance'  # должны быть права на добавление записи
    form_class = MaintenanceForm
    model = Maintenance
    template_name = 'maintenance_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('maintenance_list')  # после создания записи возвращаемся на страницу с перечнем

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем текущего пользователя, чтобы в init класса формы выводить только машины этого пользователя
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Редактирование записи о ТО с проверкой прав
class MaintenanceEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'mySilant.change_maintenance'  # должны быть права на редактирование записи
    form_class = MaintenanceForm
    model = Maintenance
    template_name = 'maintenance_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('maintenance_list')  # после редактирования записи возвращаемся на страницу с перечнем

    # Переопределяем функцию получения данных о ТО
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все ТО
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем текущего пользователя, чтобы в init класса формы выводить только машины этого пользователя
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Удаление записи о ТО с проверкой прав
class MaintenanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'mySilant.delete_maintenance'  # должны быть права на удаление записи
    model = Maintenance
    template_name = 'maintenance_delete.html'  # шаблон для вывода
    success_url = reverse_lazy('maintenance_list')  # после удаления записи возвращаемся на страницу с перечнем

    # Переопределяем функцию получения данных о ТО
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все ТО
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие ТО
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset


# Вывод списка рекламаций с проверкой прав
class ClaimList(PermissionRequiredMixin, ListView):
    permission_required = 'mySilant.view_claim'  # должны быть права на просмотр
    model = Claim  # выводим информацию о рекламациях
    ordering = 'refusal_date'  # сортировка по дате отказа
    template_name = 'claims.html'  # шаблон для вывода
    context_object_name = 'claims'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 10  # количество рекламаций на странице

    # Переопределяем функцию получения списка рекламаций
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все рекламации
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны рекламации на машины этого клиента
            queryset = Claim.objects.filter(machine__client__user_link=user).order_by('refusal_date')
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие рекламации
            queryset = Claim.objects.filter(service_company__user_link=user).order_by('refusal_date')
        self.filterset = ClaimFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        return self.filterset.qs  # возвращаем отфильтрованный список рекламаций

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # добавляем в контекст объект фильтрации
        return context


# Подробности по каждой рекламации
class ClaimDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_claim'  # должны быть права на просмотр
    model = Claim  # выводим рекламации
    template_name = 'claim.html'  # шаблон для вывода
    context_object_name = 'claim'  # имя списка, по которому будет обращение из html-шаблона

    # Переопределяем функцию получения данных о рекламации
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все рекламации
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны рекламации на машины этого клиента
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие рекламации
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новой рекламации с проверкой прав
class ClaimCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'mySilant.add_claim'  # должны быть права на добавление записи
    form_class = ClaimForm
    model = Claim
    template_name = 'claim_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('claim_list')  # после создания записи возвращаемся на страницу с перечнем

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем текущего пользователя, чтобы в init класса формы выводить только машины этого пользователя
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Редактирование записи о рекламации с проверкой прав
class ClaimEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'mySilant.change_claim'  # должны быть права на редактирование записи
    form_class = ClaimForm
    model = Claim
    template_name = 'claim_edit.html'  # шаблон для вывода
    success_url = reverse_lazy('claim_list')  # после редактирования записи возвращаемся на страницу с перечнем

    # Переопределяем функцию получения данных о рекламации
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все рекламации
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны рекламации на машины этого клиента
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие рекламации
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем текущего пользователя, чтобы в init класса формы выводить только машины этого пользователя
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Удаление записи о рекламации с проверкой прав
class ClaimDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'mySilant.delete_claim'  # должны быть права на удаление записи
    model = Claim
    template_name = 'claim_delete.html'  # шаблон для вывода
    success_url = reverse_lazy('claim_list')  # после удаления записи возвращаемся на страницу с перечнем

    # Переопределяем функцию получения данных о рекламации
    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            # Если админ или менеджер - доступны все рекламации
            queryset = super().get_queryset()
        elif user in users_clients:
            # Если клиент - доступны рекламации на машины этого клиента
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            # Если сервисная компания - доступны соответствующие рекламации
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset


# Справочное описание модели техники
class EquipmentDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_equipment'  # должны быть права на просмотр
    model = Equipment  # выводим модель техники
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание модели двигателя
class EngineDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_engine'  # должны быть права на просмотр
    model = Engine  # выводим модель техники
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание модели трансмиссии
class TransmissionDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_transmission'  # должны быть права на просмотр
    model = Transmission  # выводим модель трансмиссии
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание модели ведущего моста
class DrivingAxleDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_drivingaxle'  # должны быть права на просмотр
    model = DrivingAxle  # выводим ведущего моста
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание модели управляемого моста
class SteeringAxleDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_steeringaxle'  # должны быть права на просмотр
    model = SteeringAxle  # выводим модель управляемого моста
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание клиента
class ClientDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_steeringaxle'  # должны быть права на просмотр
    model = Client  # выводим клиента
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание сервисной компании
class ServiceCompanyDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_servicecompany'  # должны быть права на просмотр
    model = ServiceCompany  # выводим сервисную компанию
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание организации, проводившей ТО
class MaintenanceCompanyDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_maintenancecompany'  # должны быть права на просмотр
    model = MaintenanceCompany  # выводим организацию, проводившую ТО
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание типа ТО
class TypeMaintenanceDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_typemaintenance'  # должны быть права на просмотр
    model = TypeMaintenance  # выводим тип ТО
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание узла отказа
class RefusalNodeDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_refusalnode'  # должны быть права на просмотр
    model = RefusalNode  # выводим узел отказа
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


# Справочное описание способа восстановления
class RecoveryMethodDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'mySilant.view_recoverymethod'  # должны быть права на просмотр
    model = RecoveryMethod  # выводим способ восстановления
    template_name = 'reference.html'  # шаблон для вывода
    context_object_name = 'reference'  # имя списка, по которому будет обращение из html-шаблона


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
