from django.contrib import messages
from django.core.serializers.python import Serializer
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from limited_paginator.limitpaging import LimitedPaginator
from .forms import ConvertForm
from .models import SystemSource, ReferenceConvert, ReferenceKeyValue
from .utils import LoginRequiredMixin


class ModelListSerialiser(Serializer):
    def end_object(self, obj):
        self._current["id"] = str(obj._get_pk_val())
        self.objects.append(self._current)


class ReferenceConvertList1(ListView):
    paginate_by = 5
    template_name = "converter/referenceconvert/step1.html"
    paginator_class = LimitedPaginator

    def get(self, request, *args, **kwargs):
        ss = SystemSource.objects.all()
        self.queryset = ss
        return super(ReferenceConvertList1, self).get(request, *args, **kwargs)


class ReferenceConvertList2(ListView):
    paginate_by = 5
    template_name = "converter/referenceconvert/step2.html"
    paginator_class = LimitedPaginator

    def get(self, request, *args, **kwargs):
        ss = SystemSource.objects.get(code=kwargs["sys_from"])
        self.queryset = ss.references.all()
        return super(ReferenceConvertList2, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertList2, self).get_context_data(**kwargs)
        result["sys_from"] = self.kwargs["sys_from"]
        return result


class ReferenceConvertList3(ListView):
    paginate_by = 5
    template_name = "converter/referenceconvert/step3.html"
    paginator_class = LimitedPaginator

    def get(self, request, *args, **kwargs):
        ss = SystemSource.objects.all()
        self.queryset = ss
        return super(ReferenceConvertList3, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertList3, self).get_context_data(**kwargs)
        result["sys_from"] = self.kwargs["sys_from"]
        result["ref_from"] = self.kwargs["ref_from"]
        return result


class ReferenceConvertList4(ListView):
    paginate_by = 5
    template_name = "converter/referenceconvert/step4.html"
    paginator_class = LimitedPaginator

    def get(self, request, *args, **kwargs):
        ss = SystemSource.objects.get(code=kwargs["sys_to"])
        self.queryset = ss.references.all()
        return super(ReferenceConvertList4, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertList4, self).get_context_data(**kwargs)
        result["sys_from"] = self.kwargs["sys_from"]
        result["ref_from"] = self.kwargs["ref_from"]
        result["sys_to"] = self.kwargs["sys_to"]
        return result


class ReferenceConvertList5(ListView):
    paginate_by = 5
    template_name = "converter/referenceconvert/list.html"
    paginator_class = LimitedPaginator

    def get(self, request, *args, **kwargs):
        ss1 = SystemSource.objects.get(code=kwargs["sys_from"])
        ref1 = ss1.references.get(code=kwargs["ref_from"])

        ss2 = SystemSource.objects.get(code=kwargs["sys_to"])
        ref2 = ss2.references.get(code=kwargs["ref_to"])

        kv = ReferenceConvert.objects.filter(key_value_id_from__reference_id=ref1.id,
                                             key_value_id_to__reference_id=ref2.id)

        self.queryset = kv
        return super(ReferenceConvertList5, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertList5, self).get_context_data(**kwargs)
        result.update(self.kwargs)
        return result


class ReferenceConvertCreate(LoginRequiredMixin, CreateView):
    model = ReferenceConvert
    form_class = ConvertForm
    template_name = "converter/referenceconvert/form.html"

    def get_form(self, form_class=None):
        ref_from = self.kwargs.get("ref_from", "")
        sys_from = self.kwargs.get("sys_from", "")

        ref_to = self.kwargs.get("ref_to", "")
        sys_to = self.kwargs.get("sys_to", "")

        ss1 = SystemSource.objects.get(code=sys_from)
        ref1 = ss1.references.get(code=ref_from)
        rkv1 = ReferenceKeyValue.objects.filter(reference_id=ref1)

        ss2 = SystemSource.objects.get(code=sys_to)
        ref2 = ss2.references.get(code=ref_to)
        rkv2 = ReferenceKeyValue.objects.filter(reference_id=ref2)

        return ConvertForm(rkv1=rkv1, rkv2=rkv2, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertCreate, self).get_context_data(**kwargs)
        result["caption"] = "Добавление"
        result.update(self.kwargs)
        return result

    def get_success_url(self):
        return reverse_lazy("ref_conv_list5", args=(
            self.kwargs['sys_from'],
            self.kwargs['ref_from'],
            self.kwargs['sys_to'],
            self.kwargs['ref_to'],
        ))


class ReferenceConvertUpdate(LoginRequiredMixin, UpdateView):
    template_name = "converter/referenceconvert/form.html"
    form_class = ConvertForm

    def get_success_url(self):
        return reverse_lazy("ref_conv_list5", args=(
            self.kwargs['sys_from'],
            self.kwargs['ref_from'],
            self.kwargs['sys_to'],
            self.kwargs['ref_to'],
        ))

    def form_valid(self, form):
        messages.success(self.request,
                         self.kwargs.get("key_from", "") + " -> " + self.kwargs.get("key_to", "") + " update")
        return super(ReferenceConvertUpdate, self).form_valid(form)

    def get_form(self, form_class=None):
        ref_from = self.kwargs.get("ref_from", "")
        sys_from = self.kwargs.get("sys_from", "")

        ref_to = self.kwargs.get("ref_to", "")
        sys_to = self.kwargs.get("sys_to", "")

        ss1 = SystemSource.objects.get(code=sys_from)
        ref1 = ss1.references.get(code=ref_from)
        rkv1 = ReferenceKeyValue.objects.filter(reference_id=ref1)

        ss2 = SystemSource.objects.get(code=sys_to)
        ref2 = ss2.references.get(code=ref_to)
        rkv2 = ReferenceKeyValue.objects.filter(reference_id=ref2)

        return ConvertForm(rkv1=rkv1, rkv2=rkv2, **self.get_form_kwargs())

    def get_object(self, queryset=None):
        ss_from = SystemSource.objects.get(code=self.kwargs["sys_from"])
        ref_from = ss_from.references.get(code=self.kwargs["ref_from"])
        key_from = ref_from.kvs.get(key=self.kwargs["key_from"])

        ss_to = SystemSource.objects.get(code=self.kwargs["sys_to"])
        ref_to = ss_to.references.get(code=self.kwargs["ref_to"])
        key_to = ref_to.kvs.get(key=self.kwargs["key_to"])

        return ReferenceConvert.objects.get(key_value_id_from=key_from, key_value_id_to=key_to)

    def get_context_data(self, **kwargs):
        result = super(ReferenceConvertUpdate, self).get_context_data(**kwargs)
        result["caption"] = "Изменение"
        result.update(self.kwargs)
        return result


class ReferenceConvertDelete(LoginRequiredMixin, DeleteView):
    template_name = "converter/referenceconvert/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request,
                         self.kwargs.pop("key_from", "") + " -> " + self.kwargs.pop("key_to", "") + " deleted")
        return reverse_lazy("ref_conv_list5", kwargs=self.kwargs)

    def get_object(self, queryset=None):
        ss_from = SystemSource.objects.get(code=self.kwargs["sys_from"])
        ref_from = ss_from.references.get(code=self.kwargs["ref_from"])
        key_from = ref_from.kvs.get(key=self.kwargs["key_from"])

        ss_to = SystemSource.objects.get(code=self.kwargs["sys_to"])
        ref_to = ss_to.references.get(code=self.kwargs["ref_to"])
        key_to = ref_to.kvs.get(key=self.kwargs["key_to"])
        return ReferenceConvert.objects.get(key_value_id_from=key_from, key_value_id_to=key_to)

# def get(self, request, *args, **kwargs):
# template = loader.get_template("converter/step1.html")
# context = RequestContext(request, {
# "ss": ModelListSerialiser().serialize(ss),
# })
# return HttpResponse(template.render(context))

# def get_context_data(self, **kwargs):
# result = super(ReferenceConvertList, self).get_context_data(**kwargs)
#
# ss = SystemSource.objects.all()
#
# # ModelListSerialiser().serialize(ss)
# result["ss"] = ss
