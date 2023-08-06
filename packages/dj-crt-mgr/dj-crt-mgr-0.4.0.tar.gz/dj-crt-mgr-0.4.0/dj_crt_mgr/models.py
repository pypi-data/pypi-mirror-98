import logging
import ssl
import uuid
from urllib.parse import urlparse

import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from dj_smail.models import Certificate, CaCertificate
from ldap3 import Connection, Tls, Server
from ldap3.core.exceptions import LDAPBindError


logger = logging.getLogger(__name__)


class HttpCertBackend(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text='Unique ID for backend',
        verbose_name=_('id')
    )

    name = models.CharField(
        help_text=_('The name of this backend'),
        max_length=140,
        unique=True,
        verbose_name=_('name')
    )

    class Meta:
        verbose_name = _('HTTP Backend')
        verbose_name_plural = _('HTTP Backends')

    def __str__(self):
        return '%s' % self.name


class LdapCertBackend(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text='Unique ID for backend',
        verbose_name=_('id')
    )

    name = models.CharField(
        help_text=_('The name of this backend'),
        max_length=140,
        unique=True,
        verbose_name=_('name')
    )

    uri = models.CharField(
        help_text='URI (e.g. ldap://server1.example.com:389)',
        max_length=2100,
        verbose_name=_('uri')
    )

    ca_cert = models.ForeignKey(
        CaCertificate,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    use_starttls = models.BooleanField(
        default=False,
        help_text='Use STARTTLS after connection start',
        verbose_name=_('use_starttls')
    )

    username = models.CharField(
        blank=True,
        default="",
        help_text='Bind DN (leave empty for anonymous).',
        max_length=100,
        verbose_name=_('username')
    )

    password = models.CharField(
        blank=True,
        default="",
        help_text='Bind Password (hidden/masked).',
        max_length=100,
        verbose_name=_('password')
    )

    is_ad = models.BooleanField(
        default=False,
        help_text='Use NTLM auth for Microsoft Active Directory',
        verbose_name=_('is_ad')
    )

    base = models.CharField(
        blank=True,
        default="",
        help_text='Search Base',
        max_length=100,
        verbose_name=_('search base')
    )

    field = models.CharField(
        default='userCertificate;binary',
        help_text=_('LDAP field of certificate (default: userCertificate;binary)'),
        max_length=1000,
        verbose_name=_('field')
    )

    class Meta:
        verbose_name = _('LDAP Backend')
        verbose_name_plural = _('LDAP Backends')

    def __str__(self):
        if self.uri:
            return '%s (%s)' % (self.name, self.uri)
        return '%s (ldap://...)' % self.name

    @cached_property
    def parsed_uri(self):
        return urlparse(self.uri)

    @property
    def ldap_hostname(self):
        return self.parsed_uri.hostname

    @property
    def ldap_port(self):
        return self.parsed_uri.hostname

    @property
    def ldap_scheme(self):
        return self.parsed_uri.scheme

    def get_conn(self):
        """This will raise exceptions"""

        tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
        server = Server(self.uri, tls=tls_configuration)
        conn = Connection(server, self.username, self.password, auto_bind=False)

        if self.use_starttls:
            conn.start_tls()

        if not conn.bind():
            logger.error(f'error on ldap bind: {conn.result}')
            raise LDAPBindError(conn.result.get('message'))

        return conn

    def fetch(self, value=None, conn=None):
        if conn is None:
            conn = self.get_conn()

        if value is None:
            print('not specified what to fetch.. check DB and fetch all for backend')
            values = []
        else:
            values = [value]

        x509_certs = []
        for val in values:
            if conn.search(self.base, f'(mail={val})', attributes=[self.field]):
                for entry in conn.entries:
                    binary_cert = entry[self.field].values[0]
                    x509_cert = x509.load_der_x509_certificate(binary_cert, backend=default_backend())
                    x509_certs.append(x509_cert)

        conn.unbind()
        return x509_certs


class UserCertMgr(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text='Unique ID for this particular mgr',
        primary_key=True,
        verbose_name=_('id')
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    uploaded_certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
        null=True, blank=True  # optional
    )

    managed_http_certificates = models.ManyToManyField(
        Certificate,
        through='HttpUserCertMapper',
        related_name='user_mgr_http'
    )

    managed_ldap_certificates = models.ManyToManyField(
        Certificate,
        through='LdapUserCertMapper',
        related_name='user_mgr_ldap'
    )

    class Meta:
        verbose_name = _('User-Certificate Manager')
        verbose_name_plural = _('User-Certificate Managers')

    def __str__(self):
        if self.user:
            return '%s (%s)' % (self.__class__.__name__, self.user)
        return '%s (new user)' % self.__class__.__name__

    @property
    def user_email(self):
        return self.user.email  # noqa

    def all_certificates(self):
        certs = []
        if self.uploaded_certificate:
            certs.append(self.uploaded_certificate)

        for x in self.http_certificates.all():
            if x.certificate:
                certs.append(x.certificate)

        for x in self.ldap_certificates.all():
            if x.certificate:
                certs.append(x.certificate)

        return certs


class BaseUserCertMapper(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('date updated'), auto_now=True)

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.SET_NULL,
        null=True, blank=True  # optional
    )

    is_enabled = models.BooleanField(
        default=True,
        help_text='Enabled/Disable this mapper instance (default: enabled).',
        verbose_name=_('Is Enabled?')
    )

    extra_config = models.CharField(
        blank=True,
        default='',
        help_text=_('Optional additional configuration (JSON).'),
        max_length=1000,
        verbose_name=_('config (additional)')
    )

    def __str__(self):
        return '%s' % self.id


class HttpUserCertMapper(BaseUserCertMapper):
    class Meta:
        verbose_name = _('HTTP Certificate Mapper')
        verbose_name_plural = _('HTTP Certificate Mappers')

    user_cert_mgr = models.ForeignKey(
        UserCertMgr,
        on_delete=models.CASCADE,
        related_name='http_certificates'
    )

    http_backend = models.ForeignKey(
        HttpCertBackend,
        on_delete=models.PROTECT
    )

    url = models.CharField(
        help_text=_('URL to get certificate from.'),
        max_length=1000,
        verbose_name=_('url')
    )

    def fetch(self):
        print(f'Fetching from HTTP Backend: {self.http_backend}')
        try:
            response = requests.get(self.url)
        except Exception as err:
            raise err

        x509_cert = x509.load_pem_x509_certificate(response.content, backend=default_backend())
        new = Certificate.load_certificate(x509_cert)

        try:
            obj = Certificate.objects.get(certificate_txt=new.certificate_txt)
            print(f'CERT already known: {obj}')

            if not self.certificate_id == obj.id:
                self.certificate_id = obj.id
                self.save()
                print('Added to Mapper')

        except Certificate.DoesNotExist:
            new.save()
            self.certificate_id = new.id
            self.save()
            print(f'Added new CERT: {new}')


class LdapUserCertMapper(BaseUserCertMapper):
    class Meta:
        verbose_name = _('LDAP Certificate Mapper')
        verbose_name_plural = _('LDAP Certificate Mappers')

    user_cert_mgr = models.ForeignKey(
        UserCertMgr,
        on_delete=models.CASCADE,
        related_name='ldap_certificates'
    )

    ldap_backend = models.ForeignKey(
        LdapCertBackend,
        on_delete=models.PROTECT,
    )

    def fetch(self):
        print(f'Fetching from LDAP Backend: {self.ldap_backend}')
        x509_certs = self.ldap_backend.fetch(self.user_cert_mgr.user_email)

        for x509_cert in x509_certs:
            new = Certificate.load_certificate(x509_cert)

            try:
                Certificate.objects.get(certificate_txt=new.certificate_txt)
                print(f'Ignoring known CERT: {new}')
            except Certificate.DoesNotExist:
                new.save()
                self.certificate_id = new.id
                self.save()
                print(f'Added new CERT: {new}')
