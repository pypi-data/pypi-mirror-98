import logging

from dj_crt_mgr.models import HttpCertBackend, LdapCertBackend, UserCertMgr

log = logging.getLogger(__name__)


def create_default_backends(sender, **kwargs):
    obj, was_created = HttpCertBackend.objects.get_or_create(name="default")
    if was_created:
        log.info("created HttpCertBackend")

    obj, was_created = LdapCertBackend.objects.get_or_create(name="default", uri="ldap://127.0.0.1:389")
    if was_created:
        log.info("created LdapCertBackend")


def create_user_cert_mgr(sender, instance, created, **kwargs):
    if created:
        UserCertMgr.objects.create(user=instance)
