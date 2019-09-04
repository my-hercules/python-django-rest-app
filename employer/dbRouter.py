"""
class employerDBRouter(object):
    """
    A router to control employer db operations
    """
    def db_for_read(self, model, **hints):
        from django.conf import settings
        if 'employer' not in settings.DATABASES:
            return None
        if model._meta.app_label == 'employer':
            return 'employerdb'
        return None

    def db_for_write(self, model, **hints):
        from django.conf import settings
        if 'employer' not in settings.DATABASES:
            return None
        if model._meta.app_label == 'employer':
            return 'employerdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        from django.conf import settings
        if 'employer' not in settings.DATABASES:
            return None
        if obj1._meta.app_label == 'employer' or obj2._meta.app_label == 'employer':
            return True
        return None

    def allow_syncdb(self, db, model):
        from django.conf import settings
        if 'employer' not in settings.DATABASES:
            return None
        if db == 'employerdb':
            return model._meta.app_label == 'employer'
        elif model._meta.app_label == 'employer':
            return False
        return None