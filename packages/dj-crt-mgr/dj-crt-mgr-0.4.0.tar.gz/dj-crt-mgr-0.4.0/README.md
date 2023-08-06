# Django Certificate Manager

This

## Requirements

* Python 3.5+

Make sure that an instance of UserCrtMgr is created for every user::

    class YourAppConfig(AppConfig):
        def ready(self):
            from dj_crt_mgr.signals import create_user_cert_mgr
            post_save.connect(create_user_cert_mgr, sender=settings.AUTH_USER_MODEL)

## Install

Using pip

```
pip install dj-crt-mgr
```
