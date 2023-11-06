from django.contrib import admin

from .models import (
    Equipment, Engine, Transmission, DrivingAxle, SteeringAxle, Client, ServiceCompany, MaintenanceCompany,
    TypeMaintenance, RefusalNode, RecoveryMethod, Machine, Maintenance, Claim, MaintenanceAdmin, ClaimAdmin
)

admin.site.register(Equipment)
admin.site.register(Engine)
admin.site.register(Transmission)
admin.site.register(DrivingAxle)
admin.site.register(SteeringAxle)
admin.site.register(Client)
admin.site.register(ServiceCompany)
admin.site.register(MaintenanceCompany)
admin.site.register(TypeMaintenance)
admin.site.register(RefusalNode)
admin.site.register(RecoveryMethod)
admin.site.register(Machine)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Claim, ClaimAdmin)