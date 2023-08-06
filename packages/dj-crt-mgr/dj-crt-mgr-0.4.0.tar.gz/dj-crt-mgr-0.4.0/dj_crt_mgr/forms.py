from django.forms import ModelForm, PasswordInput

from dj_crt_mgr.models import LdapCertBackend


class LdapCertBackendForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = LdapCertBackend

        widgets = {
            'password': PasswordInput(render_value=True),
        }
