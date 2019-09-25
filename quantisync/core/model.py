from peewee import CharField, DateTimeField

from quantisync.lib.db import BaseModel


class Settings:
    def __init__(self, nfsDir, userEmail, userOrg, lastSync):
        self.nfsDir = nfsDir
        self.userEmail = userEmail
        self.userOrg = userOrg
        self.lastSync = lastSync


class SettingsModel(BaseModel):
    class Meta:
        table_name = 'settings'

    nfs_dir = CharField(null=True)
    user_email = CharField(null=True)
    user_org = CharField(null=True)
    last_sync = DateTimeField(null=True)

    @classmethod
    def setLastSync(cls, dateTime):
        cls.createRecordIfEmpty()
        cls.update({'last_sync': dateTime}).execute()

    @classmethod
    def setNfsDir(cls, nfsDir):
        cls.createRecordIfEmpty()
        cls.update({'nfs_dir': nfsDir}).execute()

    @classmethod
    def setUser(cls, userEmail, userOrg):
        cls.createRecordIfEmpty()
        cls.update({'user_email': userEmail, 'user_org': userOrg}).execute()

    @classmethod
    def get(cls):
        settings = cls.select().execute()[0]
        return Settings(settings.nfs_dir, settings.user_email, settings.user_org, settings.last_sync)

    @classmethod
    def createRecordIfEmpty(cls):
        if not cls.table_exists():
            cls.create_table()

        settings = cls.select().execute()
        if not settings:
            cls.create()
