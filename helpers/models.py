from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError


class TimedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimedModel):

    class Meta:
        abstract = True

    @staticmethod
    def validate_on_save():
        """
        Validate model before save. Returns dictionary {field_name: error_str, ...} or error_str.
        Override this method if need.
        """
        return {}

    def actions_on_save(self):
        """
        Set model fields or update other models before save.
        Override this method if need.
        """
        pass

    def prepare_on_save(self):
        """
        Validate model and set model fields or update other models before save.
        Returns dictionary {field_name: error_str, ...} or error_str.
        Override this method in complex situations, for example if validation
        need after actions.
        """
        errors = self.validate_on_save()
        if errors:
            return errors
        self.actions_on_save()
        return {}

    def full_clean(self, exclude=None, validate_unique=True):
        def raise_exception(errors):
            validation_error = DRFValidationError if self.is_save_from_api else DjangoValidationError
            raise validation_error(errors)

        self.is_save_from_api = getattr(self, 'is_save_from_api', False)
        errors = self.prepare_on_save()
        if errors:
            raise_exception(errors)

        try:
            super().full_clean(exclude=exclude, validate_unique=validate_unique)
        except DjangoValidationError as e:
            raise_exception(e.error_dict)

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.is_save_from_api = getattr(self, 'is_save_from_api', True)
        if self.is_save_from_api:
            self.full_clean()
        return super().save(*args, **kwargs)
