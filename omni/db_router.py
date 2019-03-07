class NetworkresourceRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'networkresource':
            return 'cmdb'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'networkresource':
            return 'cmdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'networkresource' or \
           obj2._meta.app_label == 'networkresource':
           return True
        return None
    # allow_migrate 较为重要，注意条件的设置
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'cmdb'
        database.
        """
        if db == 'cmdb':
            return app_label == 'networkresource'
        elif app_label == 'networkresource':    # django api文档没有配置这一条，会导致所有表再两个数据库都会创建
            return False
        return None     # 与False不同，以上所有None代表未匹配，会按照router优先级继续往下匹配，最后匹配default

# 使用不同app对应不同数据库的情况下使用以下配置，并对应settings里面的DATABASE_APPS_MAPPING
# from .settings.base import DATABASE_APPS_MAPPING
# class NetworkresourceRouter:
#     """
#     A router to control all database operations on models in the
#     auth application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read auth models go to auth_db.
#         """
#         if model._meta.app_label in DATABASE_APPS_MAPPING:
#             return DATABASE_APPS_MAPPING[model._meta.app_label]
#         return None

#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write auth models go to auth_db.
#         """
#         if model._meta.app_label in DATABASE_APPS_MAPPING:
#             return DATABASE_APPS_MAPPING[model._meta.app_label]
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the auth app is involved.
#         """
#         db_obj1 = DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
#         db_obj2 = DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
#         if db_obj1 and db_obj2:
#             if db_obj1 == db_obj2:
#                 return True
#             else:
#                 return False
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth app only appears in the 'auth_db'
#         database.
#         """
#         # print(db, app_label, model_name, hints)
#         if db in DATABASE_APPS_MAPPING.values():
#             return DATABASE_APPS_MAPPING.get(app_label) == db
#         elif app_label in DATABASE_APPS_MAPPING:
#             return False
#         return None