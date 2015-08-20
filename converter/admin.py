from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import SystemSource, Reference, ReferenceKeyValue, ReferenceConvert
from django.contrib.admin import AdminSite


class MyAdminSite2(AdminSite):
    site_header = "Converter administration"
    site_title = "Admin"
    index_title = "Объекты"


admin_site = MyAdminSite2(name="myadmin2")


class SystemSourceAdminView(admin.ModelAdmin):
    list_display = ("code", "fullname")


class ReferenceAdminView(admin.ModelAdmin):
    list_display = ("code", "fullname", "system_source")

    @staticmethod
    def system_source(obj):
        return "code: %s , fullname %s" % (obj.master_id.code, obj.master_id.fullname)

    system_source.short_description = "System source"


class ReferenceKeyValueAdminView(admin.ModelAdmin):
    list_display = ("key", "value")


admin_site.register(SystemSource, SystemSourceAdminView)
admin_site.register(Reference, ReferenceAdminView)
admin_site.register(ReferenceKeyValue, ReferenceKeyValueAdminView)
admin_site.register(ReferenceConvert)
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)


# @admin.register(SystemSource, Reference, ReferenceKeyValue, ReferenceConvert, User, Group, Permission,
# site=admin_site)


# admin.register(SystemSource, Reference, ReferenceKeyValue, ReferenceConvert, User, Group, Permission,
# site=MyAdminSite2(name="myadmin2"))

# admin.site.register(SystemSource, MyAdmin2)