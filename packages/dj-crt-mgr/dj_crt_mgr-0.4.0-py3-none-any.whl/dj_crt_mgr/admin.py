from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from dj_crt_mgr.forms import LdapCertBackendForm
from dj_crt_mgr.models import LdapCertBackend, UserCertMgr, LdapUserCertMapper, HttpUserCertMapper


@admin.register(LdapCertBackend)
class LdapCertBackendAdmin(admin.ModelAdmin):
    form = LdapCertBackendForm
    model = LdapCertBackend
    list_display = ('name', 'uri', 'use_starttls', 'username', 'base')
    search_fields = ('name', 'uri')


class BaseManagedCertificatesInline(admin.StackedInline):
    extra = 0
    readonly_fields = ('certificate',)


class HttpBackendCertificatesInline(BaseManagedCertificatesInline):
    model = HttpUserCertMapper
    # fields = ('http_backend', 'url', 'extra_config', 'certificate')
    fields = ('http_backend', 'url', 'certificate')
    show_change_link = True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        # this doesn't work as obj is the parent (not the inline)
        # if obj:
        #     readonly_fields = readonly_fields + ('http_backend',)

        return readonly_fields


class LdapBackendCertificatesInline(BaseManagedCertificatesInline):
    model = LdapUserCertMapper
    # fields = ('ldap_backend', 'extra_config', 'certificate')
    fields = ('ldap_backend', 'certificate')
    show_change_link = True


@admin.register(UserCertMgr)
class UserCertMgrAdmin(admin.ModelAdmin):
    model = UserCertMgr

    inlines = [
        HttpBackendCertificatesInline,
        LdapBackendCertificatesInline
    ]

    list_display = ('user', 'user_email')
    list_filter = ('user',)
    readonly_fields = ('user_email',)
    search_fields = ('user__username', 'user__email')

    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = [
                ('', {'fields': ['user_link', 'user_email']}),
                (_('Uploaded Certificate'), {'fields': ['uploaded_certificate']}),
            ]
        else:
            fieldsets = [
                ('', {'fields': ['user', 'user_email']}),
            ]

        return fieldsets

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)

        if obj:
            return inline_instances
        else:
            return []

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        if obj:
            readonly_fields = readonly_fields + ('user_link',)

        return readonly_fields

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=(obj.user.id,),
                      current_app=self.admin_site.name)
        return format_html(f'<a href="{url}">{obj.user.username}</a>')

    user_link.short_description = _('user')


class BaseUserCertMapperAdmin(admin.ModelAdmin):
    exclude = ('id',)
    readonly_fields = ('certificate', 'created', 'updated')

    actions = ["fetch"]

    def fetch(self, request, queryset):
        for item in queryset.all():
            item.fetch()

        self.message_user(request, "fetched: %s item(s)" % queryset.count())

    fetch.short_description = _("Fetch certificate(s) for selected mapper(s)")

    def get_urls(self):
        urls = super().get_urls()

        _path = '<path:object_id>/fetch/'
        urls = [x for x in urls if not x.pattern == _path]

        my_urls = [
            path(_path,
                 self.admin_site.admin_view(self.fetch_button),
                 name=f'{self.opts.app_label}_{self.opts.model_name}_fetch')
        ]
        return my_urls + urls

    def fetch_button(self, request, object_id):
        obj = self.model.objects.get(id=object_id)
        try:
            obj.fetch()
        except Exception as err:
            self.message_user(request, f'Error: {err}', messages.ERROR)

        return redirect(
            reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_change', args=[object_id])
        )


@admin.register(HttpUserCertMapper)
class HttpUserCertMapperAdmin(BaseUserCertMapperAdmin):
    model = HttpUserCertMapper
    list_display = ('id', 'is_enabled', 'user_cert_mgr', 'url')
    list_filter = ('is_enabled',)

    fields = (
        'user_cert_mgr', 'http_backend', 'url',
        'is_enabled',
        'extra_config',
        'certificate',
        'created', 'updated'
    )


@admin.register(LdapUserCertMapper)
class LdapUserCertMapperAdmin(BaseUserCertMapperAdmin):
    model = LdapUserCertMapper
    list_display = ('id', 'is_enabled', 'user_cert_mgr', 'ldap_backend')
    list_filter = ('is_enabled', 'ldap_backend',)

    fields = (
        'user_cert_mgr', 'ldap_backend',
        'is_enabled',
        'extra_config',
        'certificate',
        'created', 'updated'
    )
