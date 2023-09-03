from django.db import models


class TestStepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=0)


class SetupStepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=1)


class TeardownStepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=2)
