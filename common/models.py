from django.db import models


class BaseTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseCreatedByUpdatedBy(models.Model):
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='%(class)s_created_by', null=True, blank=True)
    modified_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='%(class)s_modified_by', null=True, blank=True)

    class Meta:
        abstract = True


class BaseModel(BaseTimeStamp, BaseCreatedByUpdatedBy):

    class Meta:
        abstract = True