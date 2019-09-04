"""
class SpotWrkAppDBRouter(object):
    """
    A router to control SpotWrkApp db operations
    """
    def db_for_read(self, model, **hints):
        from django.conf import settings
        if 'SpotWrkApp' not in model._meta.app_label:
            return None
        if model._meta.app_label == 'SpotWrkApp':
            return 'SpotWrkAppdb'
        return None

    def db_for_write(self, model, **hints):
        from django.conf import settings
        if 'SpotWrkApp' not in model._meta.app_label:
            return None
        if model._meta.app_label == 'SpotWrkApp':
            return 'SpotWrkAppdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        from django.conf import settings
        if 'SpotWrkApp' not in model._meta.app_label:
            return None
        if obj1._meta.app_label == 'SpotWrkApp' or obj2._meta.app_label == 'SpotWrkApp':
            return True
        return None

    def allow_syncdb(self, db, model):
        from django.conf import settings
        if 'SpotWrkApp' not in model._meta.app_label:
            return None
        if db == 'SpotWrkAppdb':
            return model._meta.app_label == 'SpotWrkApp'
        elif model._meta.app_label == 'SpotWrkApp':
            return False
        return None