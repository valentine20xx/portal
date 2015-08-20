from django import forms
from django.forms import ModelChoiceField

from .models import SystemSource, Reference, ReferenceKeyValue, ReferenceConvert


class SystemSourceForm(forms.ModelForm):
    class Meta:
        model = SystemSource
        fields = ("code", "fullname")

    def __init__(self, *args, **kwargs):
        super(SystemSourceForm, self).__init__(*args, **kwargs)
        self.fields["code"].widget.attrs["class"] = "form-control"
        self.fields["fullname"].widget.attrs["class"] = "form-control"

        self.fields["code"].widget.attrs["autocomplete"] = "off"
        self.fields["fullname"].widget.attrs["autocomplete"] = "off"

        # self.fields["fullname"].widget = BsInput()


class SystemSourceFilterForm(forms.Form):
    code = forms.CharField(label="Code", required=False)
    fullname = forms.CharField(label="Full name", required=False)

    def __init__(self, *args, **kwargs):
        super(SystemSourceFilterForm, self).__init__(*args, **kwargs)
        self.fields["code"].widget.attrs["class"] = "form-control"
        self.fields["fullname"].widget.attrs["class"] = "form-control"


class SystemSourceUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(SystemSourceUploadForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs["class"] = "upload"
        # self.fields["fullname"].widget.attrs["class"] = "form-control"


class SystemSourceDownloadForm(forms.Form):
    pass


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ("master_id", "code", "fullname", "table_name", "table_charset",
                  "jdbc_source", "replication_sql", "last_update_time")

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.fields["code"].widget.attrs["class"] = "form-control"
        self.fields["fullname"].widget.attrs["class"] = "form-control"
        self.fields["table_name"].widget.attrs["class"] = "form-control"
        self.fields["table_charset"].widget.attrs["class"] = "form-control"
        self.fields["jdbc_source"].widget.attrs["class"] = "form-control"
        self.fields["replication_sql"].widget.attrs["class"] = "form-control"
        self.fields["last_update_time"].widget.attrs["class"] = "form-control"

        self.fields["code"].widget.attrs["autocomplete"] = "off"
        self.fields["fullname"].widget.attrs["autocomplete"] = "off"
        self.fields["table_name"].widget.attrs["autocomplete"] = "off"
        self.fields["table_charset"].widget.attrs["autocomplete"] = "off"
        self.fields["jdbc_source"].widget.attrs["autocomplete"] = "off"
        self.fields["replication_sql"].widget.attrs["autocomplete"] = "off"
        self.fields["last_update_time"].widget.attrs["autocomplete"] = "off"
        self.fields["last_update_time"].widget.attrs["placeholder"] = "yyyy-mm-dd hh:mm:ss"

        self.fields["master_id"].widget = forms.HiddenInput()


class ReferenceKeyValueForm(forms.ModelForm):
    class Meta:
        model = ReferenceKeyValue
        fields = ("reference_id", "key", "value")

    def __init__(self, *args, **kwargs):
        super(ReferenceKeyValueForm, self).__init__(*args, **kwargs)
        self.fields["key"].widget.attrs["class"] = "form-control"
        self.fields["value"].widget.attrs["class"] = "form-control"

        self.fields["key"].widget.attrs["autocomplete"] = "off"
        self.fields["value"].widget.attrs["autocomplete"] = "off"

        self.fields["reference_id"].widget = forms.HiddenInput()


class ValueChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.value


class ValueChoiceField2(ModelChoiceField):
    def __init__(self, queryset, empty_label="---------", cache_choices=None,
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 *args, **kwargs):
        super(ValueChoiceField2, self).__init__(queryset, empty_label, cache_choices,
                                                required, widget, label, initial,
                                                help_text, to_field_name, limit_choices_to,
                                                *args, **kwargs)

    def label_from_instance(self, obj):
        return obj.value

    def get_limit_choices_to(self):
        return ReferenceKeyValue.objects.all()

        # return super(ValueChoiceField2, self).get_limit_choices_to()


class ConvertForm(forms.ModelForm):
    key_value_id_from = ValueChoiceField(queryset=None)
    key_value_id_to = ValueChoiceField(queryset=None)

    class Meta:
        model = ReferenceConvert
        fields = ("key_value_id_from", "key_value_id_to")

    def __init__(self, rkv1=None, rkv2=None, *args, **kwargs):
        super(ConvertForm, self).__init__(*args, **kwargs)

        if rkv1 is not None:
            self.fields["key_value_id_from"].queryset = rkv1

            # self.fields["key_value_id_from"].choices = [
            # (x.id, x.value) for x in rkv1
            # ]

        if rkv2 is not None:
            self.fields["key_value_id_to"].queryset = rkv2

        self.fields["key_value_id_from"].widget.attrs["class"] = "form-control"
        self.fields["key_value_id_to"].widget.attrs["class"] = "form-control"
