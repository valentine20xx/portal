import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from . import constants

regexValidator = RegexValidator(
    regex=r"^" + constants.code + "$",
    message='Letters, Numbers and Underscores allowed only',
    code='validation_error'
)


class SystemSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("code", max_length=255, unique=True, validators=[regexValidator], db_index=True)
    fullname = models.CharField("full name", max_length=255, blank=True)

    def __str__(self):
        return "System Source (" + self.code + "/" + self.fullname + ")"

    class Meta:
        # app_label
        db_table = "system_source"
        verbose_name = "System source"
        verbose_name_plural = "System sources"

    @models.permalink
    def get_absolute_url(self):
        return "ss_detail", [self.code]

    @models.permalink
    def get_update_url(self):
        return "ss_update", [self.code]

    @models.permalink
    def get_delete_url(self):
        return "ss_delete", [self.code]


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master_id = models.ForeignKey(SystemSource, related_name="references", verbose_name="system source", null=False)
    code = models.CharField("code", max_length=255, validators=[regexValidator], db_index=True)
    fullname = models.CharField("full name", max_length=255, blank=True)
    table_name = models.CharField("table name", max_length=255, blank=True)
    table_charset = models.CharField("table charset", max_length=255, blank=True)
    jdbc_source = models.CharField("jdbc source", max_length=255, blank=True)
    replication_sql = models.CharField("replication sql", max_length=255, blank=True)
    last_update_time = models.DateTimeField("last update time", null=True, blank=True)

    def __str__(self):
        return "Reference (" + self.code + "/" + self.fullname + ")"

    class Meta:
        db_table = "reference"
        verbose_name = "Reference"
        verbose_name_plural = "References"
        # unique_together = (("master_id", "code"),)

    def validate_unique(self, *args, **kwargs):
        # if self._state.adding:
        # TODO: change it
        try:
            if not str(self.master_id.references.get(code=self.code).id) == str(self.id):
                raise ValidationError({"code": "Reference with this Code already exists."})
        except ObjectDoesNotExist as e:
            super(Reference, self).validate_unique(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return "ref_detail", [self.master_id.code, self.code]

    @models.permalink
    def get_update_url(self):
        return "ref_update", [self.master_id.code, self.code]

    @models.permalink
    def get_delete_url(self):
        return "ref_delete", [self.master_id.code, self.code]


class ReferenceKeyValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_id = models.ForeignKey(Reference, related_name="kvs", verbose_name="reference", null=False)
    key = models.CharField("key", max_length=255, blank=False, validators=[regexValidator], db_index=True)
    value = models.CharField("value", max_length=255, blank=True)

    class Meta:
        db_table = "reference_key_value"
        verbose_name = "Reference Key Value"
        verbose_name_plural = "References Key Value"

    def __str__(self):
        return "Reference Key Value (" + self.reference_id.code + "/" + self.key + "/" + self.value + ")"

    def validate_unique(self, *args, **kwargs):
        # if self._state.adding:
        # TODO: change it
        try:
            if not str(self.reference_id.kvs.get(key=self.key).id) == str(self.id):
                raise ValidationError({"key": "This Key already exists."})
        except ObjectDoesNotExist as e:
            super(ReferenceKeyValue, self).validate_unique(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return "ref_kvp_detail", [self.reference_id.master_id.code, self.reference_id.code, self.key]

    @models.permalink
    def get_update_url(self):
        return "ref_kvp_update", [self.reference_id.master_id.code, self.reference_id.code, self.key]

    @models.permalink
    def get_delete_url(self):
        return "ref_kvp_delete", [self.reference_id.master_id.code, self.reference_id.code, self.key]


class ReferenceConvert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_value_id_from = models.ForeignKey(ReferenceKeyValue, related_name="key_from", verbose_name="key from", null=False)
    key_value_id_to = models.ForeignKey(ReferenceKeyValue, related_name="key_to", verbose_name="key to", null=False)

    def __str__(self):
        return "Reference Convert (" + self.key_value_id_from.reference_id.code + " - > " + self.key_value_id_to.reference_id.code + "/" + self.key_value_id_from.key + " - > " + self.key_value_id_to.key + ")"

    def validate_unique(self, *args, **kwargs):
        def val_raise():
            raise ValidationError({"key_value_id_from": "Relation already exists",
                                   "key_value_id_to": "Relation already exists"})

        if self.key_value_id_from_id is not None and self.key_value_id_to_id is not None and self.key_value_id_from_id == self.key_value_id_to_id:
            val_raise()
        try:
            r = ReferenceConvert.objects.get(key_value_id_from=self.key_value_id_from_id,
                                             key_value_id_to=self.key_value_id_to_id)

            if self._state.adding:
                val_raise()
            else:
                if r.id != self.id:
                    val_raise()
        except ObjectDoesNotExist as e:
            super(ReferenceConvert, self).validate_unique(*args, **kwargs)

    class Meta:
        db_table = "reference_convert"
        verbose_name = "Reference Convert"
        verbose_name_plural = "References Convert"
        # unique_together = (("key_value_id_from", "key_value_id_to"),)

    @models.permalink
    def get_delete_url(self):
        return "ref_conv_delete", [
            self.key_value_id_from.reference_id.master_id.code, self.key_value_id_from.reference_id.code,
            self.key_value_id_to.reference_id.master_id.code, self.key_value_id_to.reference_id.code,
            self.key_value_id_from.key,
            self.key_value_id_to.key]

    @models.permalink
    def get_update_url(self):
        return "ref_conv_update", [
            self.key_value_id_from.reference_id.master_id.code, self.key_value_id_from.reference_id.code,
            self.key_value_id_to.reference_id.master_id.code, self.key_value_id_to.reference_id.code,
            self.key_value_id_from.key,
            self.key_value_id_to.key]
