from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Модель техники
class Equipment(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Модель техники', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модель техники'

# Модель двигателя
class Engine(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Модель двигателя', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модель двигателей'

# Модeль трансмиссии
class Transmission(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Модель трансмиссии', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модель трансмиссий'

# Модeль ведущего моста
class DrivingAxle(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Модель ведущего моста', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модель ведущих мостов'

# Модель управляемого моста
class SteeringAxle(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Модель управляемого моста', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модель управляемых мостов'

# Клиент
class Client(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Клиент', max_length=255, verbose_name='Описание')
    user_link = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

# Сервисная компания
class ServiceCompany(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Сервисная компания', max_length=255, verbose_name='Описание')
    user_link = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

# Организация, проводившая ТО
class MaintenanceCompany(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Организация выполняющая ТО', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Организация, проводившая ТО'
        verbose_name_plural = 'Организации, проводившие ТО'


# Вид технического обслуживания
class TypeMaintenance(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Вид технического обслуживания', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Вид технического обслуживания'
        verbose_name_plural = 'Виды технических обслуживаний'


# Узел отказа
class RefusalNode(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Узел отказа', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказов'


# Способ восстановления
class RecoveryMethod(models.Model):
    title = models.CharField(default='noname', max_length=255, verbose_name='Название')
    description = models.CharField(default='Способ восстановления', max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановлений'

# Информация о характеристках и комплектации проданных машин, а также о месте эксплуатации
class Machine(models.Model):
    number_machine = models.CharField(unique=True, max_length=255, verbose_name='Заводский номер машины')
    model_equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Модель техники', related_name='machines_equipment')
    model_engine = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Модель двигателя', related_name='machines_engine')
    number_engine = models.CharField(max_length=255, verbose_name='Заводской номер двигателя')
    model_transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE, verbose_name='Модель трансмиссии')
    number_transmission = models.CharField(max_length=255, verbose_name='Заводской номер трансмиссии')
    model_driving_axle = models.ForeignKey(DrivingAxle, on_delete=models.CASCADE, verbose_name='Модель ведущего моста')
    number_driving_axle = models.CharField(max_length=255, verbose_name='Заводской номер ведущего моста')
    model_steering_axle = models.ForeignKey(SteeringAxle, on_delete=models.CASCADE, verbose_name='Модель управляемого моста')
    number_steering_axle = models.CharField(max_length=255, verbose_name='Заводской номер управляемого моста')
    supply_contract = models.CharField(max_length=255, verbose_name='Договор поставки (номер, дата)')
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    end_consumer = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    shipping_address = models.CharField(max_length=255, verbose_name='Адрес поставки (эксплуатации)')
    options = models.TextField(default='Стандарт', max_length=1000, verbose_name='Комплектация (дополнительные опции)')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def __str__(self):
            return f'{self.number_machine}'

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

# Информация об истории проведения технического обслуживания (ТО)
class Maintenance(models.Model):
    type = models.ForeignKey(TypeMaintenance, on_delete=models.CASCADE, verbose_name='Вид ТО')
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=255, verbose_name='Номер заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    maintenance_company = models.ForeignKey(MaintenanceCompany, on_delete=models.CASCADE, verbose_name='Организация, проводившая ТО')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Машина')
    # Задается в save по машине
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def save(self, *args, **kwargs):
        self.service_company = self.machine.service_company   # сервисная компания закреплена за каждой машиной
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.machine} - {self.type} - {self.maintenance_date}'

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'

# Информация о заявленных клиентами рекламациях и сроках их устранения
class Claim(models.Model):
    refusal_date = models.DateField(verbose_name='Дата отказа')
    operating_time = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    refusal_node = models.ForeignKey(RefusalNode, on_delete=models.CASCADE, verbose_name='Узел отказа')
    refusal_description = models.TextField(max_length=1000, verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    repair_parts = models.TextField(blank=True, max_length=1000, verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.IntegerField(default=0, verbose_name='Время простоя техники')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def save(self, *args, **kwargs):
        self.downtime = (self.recovery_date - self.refusal_date).days   # время простоя техники в днях
        self.service_company = self.machine.service_company  # сервисная компания закреплена за каждой машиной
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.machine} - {self.refusal_date} - {self.refusal_node}'

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'


# Исключаем из админки поля модели Maintenance, которые вычисляются автоматически или задаются в других моделях
class MaintenanceAdmin(admin.ModelAdmin):
    exclude = ['service_company']


# Исключаем из админки поля модели Claim, которые вычисляются автоматически или задаются в других моделях
class ClaimAdmin(admin.ModelAdmin):
    exclude = ['downtime', 'service_company']
