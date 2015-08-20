from django.core.serializers.python import Serializer
from django.db.models.query import QuerySet
from django.template import Library
from django.template.loader_tags import register
from django.utils.safestring import mark_safe

register = Library()


class QuerySetSerialiser(Serializer):
    def end_object(self, obj):
        self._current["pk"] = str(obj._get_pk_val())
        self._current["absolute_url"] = str(obj.get_absolute_url())
        self._current["update_url"] = str(obj.get_update_url())
        self._current["delete_url"] = str(obj.get_delete_url())

        self.objects.append(self._current)


class NotQuerySetException(Exception):
    pass


@register.filter
def queryset2json(obj):
    if isinstance(obj, QuerySet):
        serialized_queryset = QuerySetSerialiser().serialize(obj)
        x = [dict(y.items()) for y in serialized_queryset]
        return mark_safe(x)
    raise NotQuerySetException
