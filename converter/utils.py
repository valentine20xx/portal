import csv
import os
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import models
from converter.exceptions import UploadException
from .models import SystemSource, Reference, ReferenceKeyValue
from django.db import transaction

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    . fields.
    updating ``created`` and ``modified``
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoginRequiredMixin:
    @method_decorator(login_required(login_url=reverse_lazy("auth:login")))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def ss_handle_uploaded_file(f):
    filename = f.name
    # filepath = os.path.join('/home/niko/' + filename)
    filepath = os.path.join('C:/Users/nmorozov/Desktop/1/' + filename)

    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with open(filepath, newline='') as csvfile:
        iterator = csv.reader(csvfile, delimiter=',', quotechar='|')
        with transaction.atomic():
            for obj in iterator:
                if safe_get(obj, 0) == "system":
                    ss = SystemSource(code=safe_get(obj, 1),
                                      fullname=safe_get(obj, 2))
                    ss.save()
                elif safe_get(obj, 0) == "reference":
                    reference = Reference(code=safe_get(obj, 1),
                                          fullname=safe_get(obj, 2),
                                          table_name=safe_get(obj, 3),
                                          table_charset=safe_get(obj, 4),
                                          jdbc_source=safe_get(obj, 5),
                                          replication_sql=safe_get(obj, 6),
                                          master_id=ss)
                    reference.save()
                elif safe_get(obj, 0) == "content":
                    content = ReferenceKeyValue(key=safe_get(obj, 1),
                                                value=safe_get(obj, 2),
                                                reference_id=reference)
                    content.save()
                else:
                    raise UploadException("Parse error")
                    # raise ValidationError('Invalid value', code='invalid')

    os.remove(filepath)


def safe_get(_list, _index, _default=""):
    try:
        return _list[_index]
    except IndexError:
        return _default