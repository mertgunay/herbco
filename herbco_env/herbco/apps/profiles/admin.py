from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models import User, Distributor

class MyUserAdmin(UserAdmin):
    list_display = ('username',
                    'user_type'
                    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'adress',
                'postcode',
                'country',
                'user_type',
            )
        }),
    )

class DistributorModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'brand',
        'ceo_name',
        'average_earnings',
        'company_created_At',
        'is_approveled',
    )
    list_editable = ('is_approveled',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Distributor, DistributorModelAdmin)
